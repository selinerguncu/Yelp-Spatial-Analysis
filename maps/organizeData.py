import folium
from folium import plugins
import numpy as np

import sqlite3 as sqlite
import os
import sys

import pandas as pd

#extract data from yelp DB and clean it:
DB_PATH = "/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpdb.sqlite"

conn = sqlite.connect(DB_PATH)

def dataForMaps(mapParameters):
  business = str(mapParameters['business'])
  city = str(mapParameters['city'])
  price = str(mapParameters['price'])
  rating = float(mapParameters['rating'])

  if 'zipcode' in mapParameters.keys():
    zipcode = str(mapParameters['zipcode'])
    sql = "SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zip_code, price, rating, review_count FROM Business WHERE query_category = '%s' AND city = '%s' AND zip_code = '%s' AND price = '%s' AND rating = '%r'" % (business, city, zipcode, price, rating)
    coordinates = pd.read_sql_query(sql, conn)
  else:
    sql = "SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zip_code, price, rating, review_count FROM Business WHERE query_category = '%s' AND city = '%s' AND price = '%s' AND rating = '%r'" % (business, city, price, rating)
    coordinates = pd.read_sql_query(sql, conn)
    print('here')


  if len(coordinates) <= 1860:
    for i in range(len(coordinates)):
        if coordinates["longitude"][i] == None:
            coordinates["longitude"][i] = coordinates["query_longitude"][i]
        if coordinates["latitude"][i] == None:
            coordinates["latitude"][i] = coordinates["query_latitude"][i]

  #   coordinates = []

  #   for i in range(len(coords)): #max ~1860 coordinates
  #       coordinate = []
  #       coordinate.append(coords["latitude"][i])
  #       coordinate.append(coords["longitude"][i])
  #       coordinates.append(coordinate)

  #   # convert list of lists to list of tuples
  #   coordinates = [tuple([i[0],i[1]]) for i in coordinates]
  #   # print(coordinates[0:10])
    return coordinates
  # else:
  #   print("Too many data points; cannot be mapped!")
