#assume price and category are given:

from PIL import Image
import sys
import math
import numpy
import json

import sys
import os
import web
import sqlite3 as sqlite

# set boundaries in query_padmapper
# from query_padmapper import MAX_LAT, MAX_LON, MIN_LAT, MIN_LON
APP_PATH = os.getcwd()

MIN_LAT = 37.3
MAX_LAT = 37.89
MIN_LON = -122.55
MAX_LON = -121.85

# change these to change how detailed the generated image is
# (1000x1000 is good, but very slow)
MAX_X=1000
MAX_Y=1000

DRAW_DOTS=True

# at what distance should we stop making predictions?
IGNORE_DIST=0.01

def pixel_to_ll(x,y):
  delta_lat = MAX_LAT-MIN_LAT
  delta_lon = MAX_LON-MIN_LON

  # x is lon, y is lat
  # 0,0 is MIN_LON, MAX_LAT

  x_frac = float(x)/MAX_X
  y_frac = float(y)/MAX_Y

  lon = MIN_LON + x_frac*delta_lon
  lat = MAX_LAT - y_frac*delta_lat


  calc_x, calc_y = ll_to_pixel(lat, lon)

  if abs(calc_x-x) > 1 or abs(calc_y-y) > 1:
    print "Mismatch: %s, %s => %s %s" % (
      x,y, calc_x, calc_y)

  return lat, lon

def ll_to_pixel(lat,lon):
  adj_lat = lat-MIN_LAT
  adj_lon = lon-MIN_LON

  delta_lat = MAX_LAT-MIN_LAT
  delta_lon = MAX_LON-MIN_LON

  # x is lon, y is lat
  # 0,0 is MIN_LON, MAX_LAT

  lon_frac = adj_lon/delta_lon
  lat_frac = adj_lat/delta_lat

  x = int(lon_frac*MAX_X)
  y = int((1-lat_frac)*MAX_Y)

  return x,y

def load_prices(rawInputCategory): # her row u bir list olarak cekebiliyorum zaten = rawData each line = line query = rating, Query_price, bus_id, lat, lon
  #con.commit yzman lazim
  #her line data olacak sekilde cek
  #verdigin kriter raw inputla aldigin olsun where category = rawInputCategory
  category = rawInputCategory

  conn = sqlite.connect(APP_PATH + '/data/yelpdb.sqlite')
  cur = conn.cursor()
  cur.execute('''SELECT rating, query_price, id, latitude, longitude FROM Business WHERE query_category = ?''', ('bars',))
  rawData = cur.fetchall()

  raw_ratings = []
  seen = set()
  for line in rawData:
    # if not line[0].isdigit(): #rating yoksa
    #   continue

    rating = line[0]
    price = line[1]
    business_id = line[2]
    lat = line[3]
    lon = line[4]

    if business_id in seen:
      continue
    else:
      seen.add(business_id)

    rating, price = int(rating), int(price)

    raw_ratings.append((price, rating, float(lat), float(lon)))

  slope, y_intercept = linear_regression([(price, rating) for (price, rating, lat, lon) in raw_ratings])
  print "slope =", slope
  print "y intercept =", y_intercept
  x_intercept = -(y_intercept)/slope
  print "x intercept =", x_intercept
  num_phantom_price = -x_intercept # positive now

  ratings = [(rating / (price + num_phantom_price), lat, lon, price) for (price, rating, lat, lon) in raw_ratings]
  return ratings, num_phantom_price

def linear_regression(pairs):
  xs = [x for (x,y) in pairs]
  ys = [y for (x,y) in pairs]

  A = numpy.array([xs, numpy.ones(len(xs))])
  w = numpy.linalg.lstsq(A.T,ys)[0]
  return w[0], w[1]

def distance_squared(x1,y1,x2,y2):
    return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)

def distance(x1,y1,x2,y2):
    return math.sqrt(distance_squared(x1,y1,x2,y2))

# def greyscale(price):
#     grey = int(256*float(price)/3000)
#     return grey, grey, grey

def color(val, buckets):
    if val is None:
        return (255,255,255,0)

    colors = [(255, 0, 0),   #burda 18 renk elemani var o yuzden bucket imiz 18 oluyor
              (255, 91, 0),
              (255, 127, 0),
              (255, 171, 0),
              (255, 208, 0),
              (255, 240, 0),
              (255, 255, 0),
              (218, 255, 0),
              (176, 255, 0),
              (128, 255, 0),
              (0, 255, 0),
              (0, 255, 255),
              (0, 240, 255),
              (0, 213, 255),
              (0, 171, 255),
              (0, 127, 255),
              (0, 86, 255),
              (0, 0, 255),
              ]

    for rating, color in zip(buckets, colors):
        if val > rating:
            return color
    return colors[-1]

gaussian_variance = IGNORE_DIST/2
gaussian_a = 1 / (gaussian_variance * math.sqrt(2 * math.pi))
gaussian_negative_inverse_twice_variance_squared = -1 / (2 * gaussian_variance * gaussian_variance)


def gaussian(ratings, lat, lon, ignore=None):
    num = 0
    dnm = 0
    c = 0

    for rating, plat, plon, _ in ratings:
        if ignore:
            ilat, ilon = ignore
            if distance_squared(plat, plon, ilat, ilon) < 0.0001:
                continue

        weight = gaussian_a * math.exp(distance_squared(lat,lon,plat,plon) *
                                       gaussian_negative_inverse_twice_variance_squared)

        num += rating * weight
        dnm += weight

        if weight > 2:
            c += 1

    # don't display any averages that don't take into account at least five data points with significant weight
    if c < 5:
        return None

    return num/dnm

def start(rawInputCategory): #burda raw datadan aldiklarini ver = categor ve belki de sehir
    print "loading data..."
    rated_points, num_phantom_price = load_prices([rawInputCategory])

    print "computing #price adjustments..."

    # compute what the error would be at each data point if we priced it without being able to take it into account
    # do this on a per-bedroom basis, so that we can compute correction factors
    price_categories = list(sorted(set(price for _, _, _, price in rated_points)))
    adjustments = {}
    for price_category in price_categories:
        print "  price %s ..." % (price_category)
        total_actual = 0
        total_predicted = 0

        for i, (rating, plat, plon, price) in enumerate(rated_points):
            if price != price_category:
                continue

            x, y = ll_to_pixel(plat, plon)
            predicted_price = gaussian(rated_points, plat, plon, ignore=(plat, plon))

            if predicted_price:
                total_actual += price
                total_predicted += predicted_price

        if total_predicted == 0:
            # we might not make any predictions, if we don't have enough data
            adjustment = 1.0
        else:
            adjustment = total_actual / total_predicted

        adjustments[price_category] = adjustment

    print "rating all the points..."
    ratings = {}
    for x in range(MAX_X):
        print "  %s/%s" % (x, MAX_X)
        for y in range(MAX_Y):
            lat, lon = pixel_to_ll(x,y)
            ratings[x,y] = gaussian(rated_points, lat, lon)

    # determine buckets
    # we want 18 buckets (17 divisions) of equal area
    all_rated_areas = [x for x in sorted(ratings.values()) if x is not None]
    total_rated_area = len(all_rated_areas)

    buckets = []
    divisions = 17.0
    stride = total_rated_area / (divisions + 1)
    next_i = int(stride)
    error_i = stride - next_i
    for i, val in enumerate(all_rated_areas):
      if i == next_i:
        buckets.append(val)
        delta_i = stride + error_i
        next_i += int(delta_i)
        error_i = delta_i - int(delta_i)

    buckets.reverse()

    print "buckets: ", buckets

    # color regions by price
    I = Image.new('RGBA', (MAX_X, MAX_Y)) # modes: http://pillow.readthedocs.io/en/3.4.x/handbook/concepts.html#concept-modes
    IM = I.load()
    for x in range(MAX_X):
        for y in range(MAX_Y):
            IM[x,y] = color(ratings[x,y], buckets)

    if DRAW_DOTS:
        for _, lat, lon, _ in rated_points:
            x, y = ll_to_pixel(lat, lon)
            if 0 <= x < MAX_X and 0 <= y < MAX_Y:
                IM[x,y] = (0,0,0) #that is color - probably black for dots

    out_rawInputCategory = rawInputCategory + ".phantom." + str(MAX_X)
    I.save(out_rawInputCategory + ".png", "PNG")

    with open(out_rawInputCategory + ".metadata.json", "w") as outf:
      outf.write(json.dumps({
          "num_phantom_price": num_phantom_price,
          "buckets": buckets,
          "n": len(rated_points),
          "adjustments": adjustments}))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: python draw_heatmap.py apts.txt"
    else:
        rawInputCategory = sys.argv[1]
        start(rawInputCategory)
