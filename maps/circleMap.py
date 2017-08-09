import pygmaps
import sqlite3 as sqlite
import os
import pandas as pd
import numpy as np


#### CONSTRUCTOR: pygmaps.maps(latitude, longitude, zoom)
# mymap = pygmaps.maps(37.7, -122.2, 11)

def makeCircleMapRating(coordinates):
  meanLat = np.mean(coordinates["latitude"])
  meanLon = np.mean(coordinates["longitude"])
  # circleMapRating = pygmaps.maps(meanLat, meanLon, 8)
  circleMapRating = pygmaps.maps(38.231761, -122.896364, 9)
  i = 0
  k = 0
  j = 0
  l = 0
  for business in range(len(coordinates)):
    if coordinates["rating"][business] == 0.5 or coordinates["rating"][business] == 1: #yellow
      # if i < 100:
      circleMapRating.addradpoint(coordinates["latitude"][business], coordinates["longitude"][business], 200, '#F8E71C')
        # i += 1

  for business in range(len(coordinates)):
    if coordinates["rating"][business] == 1.5 or coordinates["rating"][business] == 2: #green
      # if k < 100:
      circleMapRating.addradpoint(coordinates["latitude"][business], coordinates["longitude"][business], 200, '#50E3C2')
        # k += 1

  for business in range(len(coordinates)):
    if coordinates["rating"][business] == 2.5 or coordinates["rating"][business] == 3: #red
      # if j < 100:
      circleMapRating.addradpoint(coordinates["latitude"][business], coordinates["longitude"][business], 200, '#FF0000')
        # j += 1

  for business in range(len(coordinates)):
    if coordinates["rating"][business] == 3.5 or coordinates["rating"][business] == 4: #blue
      # if l < 100:
      circleMapRating.addradpoint(coordinates["latitude"][business], coordinates["longitude"][business], 200, '#1015E0')
        # l += 1

  for business in range(len(coordinates)):
    if coordinates["rating"][business] == 4.5 or coordinates["rating"][business] == 5: #purple
      # if l < 100:
      circleMapRating.addradpoint(coordinates["latitude"][business], coordinates["longitude"][business], 200, '#BD10E0')
        # l += 1

  return circleMapRating.draw('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/circleMapRating.html')


def makeCircleMapPrice(coordinates):
  meanLat = np.mean(coordinates["latitude"])
  meanLon = np.mean(coordinates["longitude"])
  # circleMapPrice = pygmaps.maps(meanLat, meanLon, 8)
  circleMapPrice = pygmaps.maps(38.231761, -122.896364, 9)
  i = 0
  k = 0
  j = 0
  l = 0
  for business in range(len(coordinates)):
    if int(coordinates["query_price"][business]) == 1: #yellow
      # if i < 100:
      circleMapPrice.addradpoint(coordinates["latitude"][business], coordinates["longitude"][business], 200, '#FFFF00')
        # i += 1

  for business in range(len(coordinates)):
    if int(coordinates["query_price"][business]) == 2: #green
      # if k < 100:
      circleMapPrice.addradpoint(coordinates["latitude"][business], coordinates["longitude"][business], 200, '#008000')
        # k += 1

  for business in range(len(coordinates)):
    if int(coordinates["query_price"][business]) == 3: #red
      # if j < 100:
      circleMapPrice.addradpoint(coordinates["latitude"][business], coordinates["longitude"][business], 200, '#FF0000')
        # j += 1

  for business in range(len(coordinates)):
    if int(coordinates["query_price"][business]) == 4: #blue
      # if l < 100:
      circleMapPrice.addradpoint(coordinates["latitude"][business], coordinates["longitude"][business], 200, '#1015E0')
        # l += 1

  return circleMapPrice.draw('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/circleMapPrice.html')
# DB_PATH = "/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpdb.sqlite"

# conn = sqlite.connect(DB_PATH)

# coords = pd.read_sql_query('''SELECT longitude, latitude,
#   query_latitude, query_latitude, price, rating, review_count, name, query_category
#   FROM Business WHERE city = "San Mateo";''', conn)

# coords_rest = pd.read_sql_query('''SELECT longitude, latitude,
#   query_latitude, query_latitude, price, rating, review_count, name, query_category
#   FROM Business WHERE query_category = "restaurants";''', conn)

# coords_bars = pd.read_sql_query('''SELECT longitude, latitude,
#   query_latitude, query_latitude, price, rating, review_count, name, query_category
#   FROM Business WHERE query_category = "bars";''', conn)

# coords_coffee = pd.read_sql_query('''SELECT longitude, latitude,
#   query_latitude, query_latitude, price, rating, review_count, name, query_category
#   FROM Business WHERE query_category = "coffee";''', conn)

# coords_beauty = pd.read_sql_query('''SELECT longitude, latitude,
#   query_latitude, query_latitude, price, rating, review_count, name, query_category
#   FROM Business WHERE query_category = "beautysvc";''', conn)

# coords_gift = pd.read_sql_query('''SELECT longitude, latitude,
#   query_latitude, query_latitude, price, rating, review_count, name, query_category
#   FROM Business WHERE query_category = "giftshops";''', conn)

# for i in range(len(coords)):
#   if coords["longitude"][i] == None:
#     coords["longitude"][i] = coords["query_longitude"][i]
#   if coords["latitude"][i] == None:
#     coords["latitude"][i] = coords["query_latitude"][i]

# for i in range(len(coords_coffee)):
#   if coords_coffee["longitude"][i] == None:
#     coords_coffee["longitude"][i] = coords_coffee["query_longitude"][i]
#   if coords_coffee["latitude"][i] == None:
#     coords_coffee["latitude"][i] = coords_coffee["query_latitude"][i]



#### FUNCTION: setgrids(start-Lat, end-Lat, Lat-interval, start-Lng, end-Lng, Lng-interval)
# mymap.setgrids(36.5, 37.5, 1, -123, -121, 1)

# ### FUNCTION: addpoint(latitude, longitude, [color])

# i = 0
# k = 0
# j = 0
# l = 0
# for business in range(len(coords)):
#   if coords["price"][business] == '$': #yellow
#     if i < 100:
#       i += 1
#       mymap.addpoint(coords["latitude"][business], coords["longitude"][business], "#FFFF00")
#   if coords["price"][business] == '$$': #green
#     if j < 100:
#       j += 1
#       mymap.addpoint(coords["latitude"][business], coords["longitude"][business], "#008000")
#   if coords["price"][business] == '$$$': #blue
#     if k < 100:
#       k += 1
#       mymap.addpoint(coords["latitude"][business], coords["longitude"][business], "#0000FF")
#   if coords["price"][business] == '$$$$': #red
#     if l < 100:
#       l += 1
#       mymap.addpoint(coords["latitude"][business], coords["longitude"][business], "#FF0000")
# i = 0
# k = 0
# j = 0
# l = 0
# for business in range(len(coords_coffee)):
#   if coords_coffee["price"][business] == '$': #yellow
#     if i < 100:
#       i += 1
#       mymap.addpoint(coords_coffee["latitude"][business], coords_coffee["longitude"][business], "#FFFF00")
#   if coords_coffee["price"][business] == '$$': #green
#     if j < 100:
#       j += 1
#       mymap.addpoint(coords_coffee["latitude"][business], coords_coffee["longitude"][business], "#008000")
#   if coords_coffee["price"][business] == '$$$': #blue
#     if k < 100:
#       k += 1
#       mymap.addpoint(coords_coffee["latitude"][business], coords_coffee["longitude"][business], "#0000FF")
#   if coords_coffee["price"][business] == '$$$$': #red
#     if l < 100:
#       l += 1
#       mymap.addpoint(coords_coffee["latitude"][business], coords_coffee["longitude"][business], "#FF0000")

#### FUNCTION: addradpoint(latitude, longitude, radius, [color], title)



# print(i, k, j, l)
#### FUNCTION: addpath(path,[color])
# path = [(37.429, -122.145),(37.428, -122.145),(37.427, -122.145),(37.427, -122.146),(37.427, -122.146)]
# mymap.addpath(path,"#00FF00")

# p = 0
# prices = []
# #### FUNCTION: addradpoint(latitude, longitude, radius, [color], title)
# for i in range(len(coords)):
#   prices.append(coords["price"][i])
#   p += 1

# print(p)
# prices = set(prices)
# print(prices)

#### FUNCTION: draw(file)

# import os
# import time
# from selenium import webdriver

# delay=5
# fn='mymap.html'
# tmpurl='file:///Users/selinerguncu/Desktop/PythonProjects/Fun%20Projects/Yelp%20Project/Simulation/mymap.html'.format(path=os.getcwd(),mapfile=fn)
# mymap.save(fn)

# browser = webdriver.Firefox()
# browser.get(tmpurl)
# #Give the map tiles some time to load
# time.sleep(delay)
# browser.save_screenshot('mynewmap.png')
# browser.quit()
