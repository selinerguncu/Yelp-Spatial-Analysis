import folium
from folium import plugins
import numpy as np

import sqlite3 as sqlite
import os
import sys

import pandas as pd

#extract data from yelp DB and clean it:
DB_PATH = "/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite"

conn = sqlite.connect(DB_PATH)

def dataForFoliumMaps(mapParameters):
  business = str(mapParameters['business'])
  region = str(mapParameters['region'])
  price = str(mapParameters['price'])
  rating = float(mapParameters['rating'])

  # print('mapParameters', mapParameters)

  # if 'zipcode' in mapParameters.keys():
  #   zipcode = str(mapParameters['zipcode'])
  #   sql = "SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zip_code, price, rating, review_count FROM Business WHERE query_category = '%s' AND city = '%s' AND zip_code = '%s' AND price = '%s' AND rating = '%r'" % (business, city, zipcode, price, rating)
  #   coordinates = pd.read_sql_query(sql, conn)
  # else:
  #   sql = "SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zip_code, price, rating, review_count FROM Business WHERE query_category = '%s' AND city = '%s' AND price = '%s' AND rating = '%r'" % (business, city, price, rating)
  #   coordinates = pd.read_sql_query(sql, conn)
  #   print('here')

  sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
  FROM CleanBusinessData
  WHERE query_category = '%s' AND price = '%s' AND rating = '%r' AND region = '%r''' % (business, price, rating, region)


  # if region == 'Bay Area':
  #   sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
  #     FROM CleanBusinessData
  #     WHERE query_category = '%s' AND price = '%s' AND rating = '%r' AND city != '%s' ''' % (business, price, rating, 'San Francisco')
  # elif region == 'Peninsula':
  #   sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
  #     FROM CleanBusinessData
  #     WHERE query_category = '%s' AND price = '%s' AND rating = '%r' AND city != '%s' AND city != '%s' AND city != '%s' ''' % (business, price, rating, 'San Francisco', 'San Francisco - Downtown', 'San Francisco - Outer')
  # elif region == 'San Francisco':
  #   sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
  #     FROM CleanBusinessData
  #     WHERE query_category = '%s' AND price = '%s' AND rating = '%r' AND city = ?''' % (business, price, rating, 'San Francisco')
  # elif region == 'Downtown SF':
  #   sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
  #     FROM CleanBusinessData
  #     WHERE query_category = '%s' AND price = '%s' AND rating = '%r' AND city = '%s' ''' % (business, price, rating, 'San Francisco - Downtown')
  # elif region == 'Outer SF':
  #   sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
  #     FROM CleanBusinessData
  #     WHERE query_category = '%s' AND price = '%s' AND rating = '%r' AND city = '%s' ''' % (business, price, rating, 'San Francisco - Outer')
  # elif region == 'East Bay':
  #   sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
  #     FROM CleanBusinessData
  #     WHERE query_category = '%s' AND price = '%s' AND rating = '%r' AND region = '%s' ''' % (business, price, rating, 'eastBay')
  # elif region == 'North Bay':
  #   sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
  #     FROM CleanBusinessData
  #     WHERE query_category = '%s' AND price = '%s' AND rating = '%r' AND region = '%s' ''' % (business, price, rating, 'northBay')


  if region == 'Bay Area':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND city != '%s' ''' % (business, 'San Francisco')
  elif region == 'Peninsula':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND city != '%s' AND city != '%s' AND city != '%s' ''' % (business, 'San Francisco', 'San Francisco - Downtown', 'San Francisco - Outer')
  elif region == 'San Francisco':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND city = ?''' % (business, 'San Francisco')
  elif region == 'Downtown SF':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND city = '%s' ''' % (business, 'San Francisco - Downtown')
  elif region == 'Outer SF':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND city = '%s' ''' % (business, 'San Francisco - Outer')
  elif region == 'East Bay':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND region = '%s' ''' % (business, 'eastBay')
  elif region == 'North Bay':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND region = '%s' ''' % (business, 'northBay')


  coordinatesForFoliumMaps = pd.read_sql_query(sql, conn)
  print('coordinatesForFoliumMaps', len(coordinatesForFoliumMaps))

  # if len(coordinatesForFoliumMaps) <= 1860:
  for i in range(len(coordinatesForFoliumMaps)):
      if coordinatesForFoliumMaps["longitude"][i] == None:
          coordinatesForFoliumMaps["longitude"][i] = coordinatesForFoliumMaps["query_longitude"][i]
      if coordinatesForFoliumMaps["latitude"][i] == None:
          coordinatesForFoliumMaps["latitude"][i] = coordinatesForFoliumMaps["query_latitude"][i]
  return coordinatesForFoliumMaps


def dataForCircleMapsRating(mapParameters):
  business = str(mapParameters['business'])
  region = str(mapParameters['region'])
  price = str(mapParameters['price'])
  rating = float(mapParameters['rating'])

  print('mapParameters', mapParameters)

  # sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
  # FROM CleanBusinessData
  # WHERE query_category = '%s' AND price = '%s' AND rating = '%r' AND region = '%r''' % (business, price, rating, region)

  if region == 'Bay Area':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND price = '%s' AND city != '%s' ''' % (business, price, 'San Francisco')
  elif region == 'Peninsula':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND price = '%s' AND city != '%s' AND city != '%s' AND city != '%s' ''' % (business, price, 'San Francisco', 'San Francisco - Downtown', 'San Francisco - Outer')
  elif region == 'San Francisco':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND price = '%s' AND city = ?''' % (business, price, 'San Francisco')
  elif region == 'Downtown SF':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND price = '%s' AND city = '%s' ''' % (business, price, 'San Francisco - Downtown')
  elif region == 'Outer SF':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND price = '%s' AND city = '%s' ''' % (business, price, 'San Francisco - Outer')
  elif region == 'East Bay':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND price = '%s' AND region = '%s' ''' % (business, price, 'eastBay')
  elif region == 'North Bay':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND price = '%s' AND region = '%s' ''' % (business, price, 'northBay')

  coordinatesForCircleMapsRating = pd.read_sql_query(sql, conn)

  # if len(coordinatesForCircleMapsRating) <= 1860:
  for i in range(len(coordinatesForCircleMapsRating)):
      if coordinatesForCircleMapsRating["longitude"][i] == None:
          coordinatesForCircleMapsRating["longitude"][i] = coordinatesForCircleMapsRating["query_longitude"][i]
      if coordinatesForCircleMapsRating["latitude"][i] == None:
          coordinatesForCircleMapsRating["latitude"][i] = coordinatesForCircleMapsRating["query_latitude"][i]
  return coordinatesForCircleMapsRating

def dataForCircleMapsPrice(mapParameters):
  business = str(mapParameters['business'])
  region = str(mapParameters['region'])
  price = str(mapParameters['price'])
  rating = float(mapParameters['rating'])

  print('mapParameters', mapParameters)

  # sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
  # FROM CleanBusinessData
  # WHERE query_category = '%s' AND price = '%s' AND rating = '%r' AND region = '%r''' % (business, price, rating, region)

  if region == 'Bay Area':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND rating = '%r' AND city != '%s' ''' % (business, rating, 'San Francisco')
  elif region == 'Peninsula':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND rating = '%r' AND city != '%s' AND city != '%s' AND city != '%s' ''' % (business, rating, 'San Francisco', 'San Francisco - Downtown', 'San Francisco - Outer')
  elif region == 'San Francisco':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND rating = '%r' AND city = ?''' % (business, rating, 'San Francisco')
  elif region == 'Downtown SF':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND rating = '%r' AND city = '%s' ''' % (business, rating, 'San Francisco - Downtown')
  elif region == 'Outer SF':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND rating = '%r' AND city = '%s' ''' % (business, rating, 'San Francisco - Outer')
  elif region == 'East Bay':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND rating = '%r' AND region = '%s' ''' % (business, rating, 'eastBay')
  elif region == 'North Bay':
    sql = '''SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zipcode, price, rating, review_count, region
      FROM CleanBusinessData
      WHERE query_category = '%s' AND rating = '%r' AND region = '%s' ''' % (business, rating, 'northBay')

  coordinatesForCircleMapsPrice = pd.read_sql_query(sql, conn)

  # if len(coordinatesForCircleMapsPrice) <= 1860:
  for i in range(len(coordinatesForCircleMapsPrice)):
      if coordinatesForCircleMapsPrice["longitude"][i] == None:
          coordinatesForCircleMapsPrice["longitude"][i] = coordinatesForCircleMapsPrice["query_longitude"][i]
      if coordinatesForCircleMapsPrice["latitude"][i] == None:
          coordinatesForCircleMapsPrice["latitude"][i] = coordinatesForCircleMapsPrice["query_latitude"][i]
  return coordinatesForCircleMapsPrice


  #   coordinates = []

  #   for i in range(len(coords)): #max ~1860 coordinates
  #       coordinate = []
  #       coordinate.append(coords["latitude"][i])
  #       coordinate.append(coords["longitude"][i])
  #       coordinates.append(coordinate)

  #   # convert list of lists to list of tuples
  #   coordinates = [tuple([i[0],i[1]]) for i in coordinates]
  #   # print(coordinates[0:10])
  # else:
  #   print("Too many data points; cannot be mapped!")
