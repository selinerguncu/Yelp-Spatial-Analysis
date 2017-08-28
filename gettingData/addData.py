import sqlite3 as sqlite
import urllib
import sys
import os

global conn
global cur
global json_contents

from urllib import quote
from urllib import urlencode
from rawDataHandler import RawDataHandler
from geopy import Point
from geopy.distance import distance, VincentyDistance

import sqlite3 as sqlite
import yelpQuery
import os
import json
import pprint
import time
import sys
import ast
import requests
# import areaCoordinates


APP_PATH = os.getcwd()

print APP_PATH

conn = sqlite.connect(APP_PATH + '/data/yelpdb.sqlite')
conn.text_factory = str #text will be returned as string not unicode (default for sqlite3)
cur = conn.cursor()

cur.execute('''SELECT query_latitude, query_longitude FROM Search
  WHERE business_count > 50
  ORDER BY query_latitude''')
additionalQueries = set(cur.fetchall())

def defineBorders(coordinate):
  latitude = coordinate[0]
  longitude = coordinate[1]
  #Sqare around the big circle coordinates: 45 degree jump is 1 km for r = 0.707km
  BORDERS = {}

  BORDERS['NE'] = VincentyDistance(kilometers=1).destination(Point(latitude, longitude), 45)
  BORDERS['SE'] = VincentyDistance(kilometers=1).destination(Point(latitude, longitude), 135)
  BORDERS['SW'] = VincentyDistance(kilometers=1).destination(Point(latitude, longitude), 225)
  BORDERS['NW'] = VincentyDistance(kilometers=1).destination(Point(latitude, longitude), 315)
  return BORDERS

categories = ["restaurants", "bars", "nightlife", "coffee", "beautysvc", "food", "giftshops"]
prices = ["1", "2", "3", "4"]

input_values = {}
i = 0
j = 0
q = 0

for additionalQuery in additionalQueries:
  BORDERS = defineBorders(additionalQuery)
  q += 1
  print 'query', q
  # print "BORDERS", BORDERS

  for price in prices:
    input_values["price"] = price

    for category in categories:
      input_values["category"] = category

      latitude = BORDERS["NW"][0]

      while BORDERS["NW"][0] >= latitude >= BORDERS["SW"][0]:
        longitude = BORDERS["NW"][1]
        # 0.14142 for 100 radius
        newPoint = VincentyDistance(kilometers=0.141).destination(Point(latitude, longitude), 180)

        input_values["latitude"] = latitude
        latitude = newPoint.latitude
        # print latitude

        while BORDERS["NW"][1] <= longitude <= BORDERS["NE"][1]:
          j += 1
          newPoint = VincentyDistance(kilometers=0.141).destination(Point(latitude, longitude), 90)
          input_values["longitude"] = longitude
          longitude = newPoint.longitude
          i = i + 1
          # print 'here', category, price, latitude, longitude
          if 8963 < i < 25000:
            time.sleep(0.1)
            print i
            area = RawDataHandler(input_values)
            area.getRawJSON()
            area.writeSearchTable()
            area.writeBusinessTable()
            area.writeReviewsTable()
          elif i >= 25000:
            print '---'
            print i
            sys.exit()
          else:
            longitude = newPoint.longitude
            continue


print '---'
print i
