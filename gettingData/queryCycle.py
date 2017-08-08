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
import areaCoordinates

global conn
global cur
# global appPath
global json_contents

# appPath = os.getcwd()

coordinates = areaCoordinates.area

categories = ["bars", "coffee", "beautysvc", "food", "giftshops"]
# categories = ["restaurants", "bars", "nightlife", "coffee", "beautysvc", "food", "giftshops"]
prices = ["1", "2", "3", "4"]
# categories = ["restaurants"]
# prices = ["1"]

# LATT_INCREMENT = 0.005
# LONG_INCREMENT = 0.005

#mainland coordinates:
LATT_WEST = 44.81314
LATT_EAST = 25.11735
LATT_NORTH = 49.2666656
LATT_SOUTH = 48.16590

LONG_WEST = -66.96276
LONG_EAST = -81.08813
LONG_NORTH = -95.0499998
LONG_SOUTH = -124.73246

def checkIfValidCoordinate(latOrLong, coordinate):
  isValid = False
  for coordinateSet in coordinates:
    if latOrLong == 'lat':
      if coordinateSet["lat"][0] > coordinate > coordinateSet["lat"][1]:
        isValid = True
        break
    else:
      if coordinateSet["lng"][1] > coordinate > coordinateSet["lng"][0]:
        isValid = True
        break

  return isValid


#Bay area coordinates:
BORDERS = {
  'NW': (37.95077976072001, -122.74698257446289),
  'NE': (38.04601261075696, -122.07544326782227),
  'SE': (37.16149648300589, -121.47668838500977),
  'SW': (37.0421100532159, -122.42425918579102)
}

input_values = {}

i = 0
j = 0
for price in prices:
  input_values["price"] = price

  for category in categories:
    input_values["category"] = category

    latitude = BORDERS["NW"][0]

    while BORDERS["NW"][0] >= latitude >= BORDERS["SW"][0]:
      longitude = BORDERS["NW"][1]
      latValid = checkIfValidCoordinate('lat', latitude)
#707 for 500 radius
      newPoint = VincentyDistance(kilometers=0.707).destination(Point(latitude, longitude), 180)

      if latValid:
        input_values["latitude"] = latitude
        latitude = newPoint.latitude
      else:
        latitude = newPoint.latitude
        continue


      while BORDERS["NE"][1] >= longitude >= BORDERS["NW"][1]:
        j += 1
        longValid = checkIfValidCoordinate('lng', longitude)
        newPoint = VincentyDistance(kilometers=0.707).destination(Point(latitude, longitude), 90)
        if longValid:
          input_values["longitude"] = longitude
          longitude = newPoint.longitude
          i = i + 1
          if 150000 < i < 175000:
            time.sleep(0.1)
            print i
            area = RawDataHandler(input_values)
            area.getRawJSON()
            area.writeSearchTable()
            area.writeBusinessTable()
            area.writeReviewsTable()
          elif i >= 175000:
            print '---'
            print i
            sys.exit()
        else:
          longitude = newPoint.longitude
          continue


print '---'
print i
# def checkIfValidCoordinate1(latOrLong, coordinate):
#   isValid = False
#   for coordinateSet in areas:
#     if coordinateSet[latOrLong][0] >= coordinate >= coordinateSet[latOrLong][1]:
#       isValid = True
#       break

#   return isValid

# BORDERS = {
#   'NW': (10, -10),
#   'NE': (10, 0),
#   'SE': (0, 0),
#   'SW': (0, -10)
# }

# areas = [
#   # { "lat":(3, 4), "lng": (-3, -4)},
#   { "lat":(6, 8), "lng": (-3, -4)},
# ]

# latitude = BORDERS["NW"][0]
# i = 0
# j = 0

# while BORDERS["NW"][0] >= latitude >= BORDERS["SW"][0]:
#   print 'girdim'
#   # isValidLat = checkIfValidCoordinate1('lat',latitude)
#   latitude = latitude - 1
#   longitude = BORDERS["NW"][1]

#   while BORDERS["NE"][1] >= longitude >= BORDERS["NW"][1]:
#     print 'daha iceri girdim'
#     j += 1
#     # isValidLong = checkIfValidCoordinate1('lng',longitude)
#     longitude = longitude + 1
#     # if isValidLong:
#     #   i = i + 1

# print i, j
