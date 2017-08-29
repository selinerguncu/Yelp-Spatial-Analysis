import pandas as pd
import numpy as np
import sqlite3 as sqlite
import os
from collections import defaultdict # to handle missing values while writing to the DB
import sys
from geopy.distance import great_circle


#import data
def getCleanData():
  # Read sqlite query results into a pandas DataFrame
  conn = sqlite.connect("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite")
  data = pd.read_sql_query("SELECT * FROM CleanBusinessData", conn)

  # verify that result of SQL query is stored in the dataframe
  # high = df[df['review_count']>500]['city']
  print(data.head())

  conn.close()
  return data

##############################################
########## Competition Variables #############
##############################################


# distance from the closest: 2-5-10-15 competitors (MOD)

def distanceFromTheClosest(data):
  zipcodes = data['zipcode'].unique()
  categories = data['query_category'].unique()
  # print(zipcodes)
  distanceAllBusinesses = pd.DataFrame(columns = ['distance', 'id', 'price', 'rating'])
  for category in categories:
    print(category)
    for zipcode in zipcodes[0:5]:
      print(zipcode)
      regionalData = data[(data['zipcode'] == zipcode) & (data['query_category'] == category)]
      for row in regionalData.itertuples():
        coordinate1 = (row[14], row[12])
        # print('row', row)
        # sys.exit()
      # for row_id, row in enumerate(data.values):
        for i in regionalData.itertuples():
          if row != i:
            coordinate2 = (i[14], i[12])
            distance = great_circle(coordinate1, coordinate2).miles
            businessID = row[1]
            price = int(i[15])
            rating = i[2]
            # temp.extend([distance, businessID, price, rating])
            # distanceAllBusinesses.append(temp)
            distanceAllBusinesses.loc[len(distanceAllBusinesses)] = [distance, businessID, price, rating]
            # print('i', distanceAllBusinesses)
            # sys.exit()

  # sys.exit()

  businesses = data['id'].unique()
  for business in businesses[0:10]:
    closest2 = distanceAllBusinesses[distanceAllBusinesses['id'] == business].nsmallest(2, 'distance')
    print(closest2.head())
    closest2Distance = closest2['distance'].mean()
    closest2Price = closest2['price'].mean()
    closest2Rating = closest2['rating'].mean()

    closest5 = distanceAllBusinesses[distanceAllBusinesses['id'] == business].nsmallest(5, 'distance')
    closest5Distance = closest5['distance'].mean()
    closest5Price = closest5['price'].mean()
    closest5Rating = closest5['rating'].mean()

    closest10 = distanceAllBusinesses[distanceAllBusinesses['id'] == business].nsmallest(10, 'distance')
    closest10Distance = closest10['distance'].mean()
    closest10Price = closest10['price'].mean()
    closest10Rating = closest10['rating'].mean()

    closest15 = distanceAllBusinesses[distanceAllBusinesses['id'] == business].nsmallest(15, 'distance')
    closest15Distance = closest15['distance'].mean()
    closest15Price = closest15['price'].mean()
    closest15Rating = closest15['rating'].mean()

    columns = ['closest2Distance','closest2Price','closest2Rating',
               'closest5Distance','closest5Price','closest5Rating',
               'closest10Distance','closest10Price','closest10Rating',
               'closest15Distance','closest15Price','closest15Rating']

    # dataDistanceAdded = pd.concat([distanceAllBusinesses, pd.DataFrame(columns = columns)])

    temp = pd.DataFrame([[0,0,0,0,0,0,0,0,0,0,0,0]],
      index=distanceAllBusinesses.index, columns = columns)

    dataDistanceAdded = data.join(temp, how='outer')
    print(dataDistanceAdded.head())

    for index, row in dataDistanceAdded.iterrows():
      if row['id'] == business:
        row['closest2Distance'] = closest2Distance
        row['closest2Price'] = closest2Price
        row['closest2Rating'] = closest2Rating
        row['closest5Distance'] = closest5Distance
        row['closest5Price'] = closest5Price
        row['closest5Rating'] = closest5Rating
        row['closest10Distance'] = closest10Distance
        row['closest10Price'] = closest10Price
        row['closest10Rating'] = closest10Rating
        row['closest15Distance'] = closest15Distance
        row['closest15Price'] = closest15Price
        row['closest15Rating'] = closest15Rating

        # row['query_price'] = int(row['query_price'])
        # print(row)

  return dataDistanceAdded


def addCompetitionZipcode(data):
  # data['numberOfCompetitorsZipcode'] = 0
  # data['avgPriceZipcode'] = 0
  # data['avgRatingZipcode'] = 0

  columns = ['numberOfCompetitorsZipcode','avgPriceZipcode','avgRatingZipcode']

  # dataCompetitionZipcodeAdded = pd.concat([data, pd.DataFrame(columns = columns)])

  temp = pd.DataFrame([[0,0,0]], index=data.index, columns = columns)

  dataCompetitionZipcodeAdded = data.join(temp, how='outer')

  zipcodes = data['zipcode'].unique()
  categories = data['query_category'].unique()

  for category in categories:
    for zipcode in zipcodes[0:1]:
      regionalData = dataCompetitionZipcodeAdded[(dataCompetitionZipcodeAdded['zipcode'] == zipcode) & (dataCompetitionZipcodeAdded['query_category'] == category)]
      numberOfCompetitorsZipcode = len(regionalData.index)
      avgPriceZipcode = regionalData['query_price'].mean()
      avgRatingZipcode = regionalData['rating'].mean()

      for index, row in dataCompetitionZipcodeAdded.iterrows():
        if row['zipcode'] == zipcode and row['query_category'] == category:
          row['numberOfCompetitorsZipcode'] = numberOfCompetitorsZipcode
          row['avgPriceZipcode'] = avgPriceZipcode
          row['avgRatingZipcode'] = avgRatingZipcode
        if row['numberOfCompetitorsZipcode'] != 0 and row['closest10Price'] != 0 and row['closest10Price'] != np.nan:
          print(row)
  # data = dataCompetitionZipcodeAdded
  print(dataCompetitionZipcodeAdded.head())
  return dataCompetitionZipcodeAdded
# addCompetitionZipcode(distanceFromTheClosest(getCleanData()))
# sys.exit()

def addCompetitionCity(data):
  columns = ['numberOfCompetitorsCity','avgPriceCity','avgRatingCity']

  temp = pd.DataFrame([[0,0,0]], index=data.index, columns = columns)

  dataCompetitionCityAdded = data.join(temp, how='outer')

  cities = data['city'].unique()
  categories = data['query_category'].unique()

  for category in categories:
    for city in cities[0:1]:
      regionalData = dataCompetitionCityAdded[(dataCompetitionCityAdded['city'] == city) & (dataCompetitionCityAdded['query_category'] == category)]
      numberOfCompetitorsCity = len(regionalData.index)
      avgPriceCity = regionalData['query_price'].mean()
      avgRatingCity = regionalData['rating'].mean()

      for index, row in dataCompetitionCityAdded.iterrows():
        if row['city'] == city and row['query_category'] == category:
          row['numberOfCompetitorsCity'] = numberOfCompetitorsCity
          row['avgPriceCity'] = avgPriceCity
          row['avgRatingCity'] = avgRatingCity
        if row['numberOfCompetitorsCity'] != 0 and row['numberOfCompetitorsCity'] != 0 and row['closest10Price'] != np.nan:
          print(row)

  # data = dataCompetitionCityAdded
  print(dataCompetitionCityAdded.columns)
  return dataCompetitionCityAdded

addCompetitionCity(addCompetitionZipcode(distanceFromTheClosest(getCleanData())))


# id  rating price        county
# query_latitude  query_longitude  population          city  review_count
# area                closest5Rating  closest10Distance closest10Price


# Index(['id', 'rating', 'price', 'county', 'query_latitude', 'query_longitude',
#        'population', 'city', 'review_count', 'area', 'zipcode', 'longitude',
#        'query_category', 'latitude', 'query_price', 'region',
#        'closest2Distance', 'closest2Price', 'closest2Rating',
#        'closest5Distance', 'closest5Price', 'closest5Rating',
#        'closest10Distance', 'closest10Price', 'closest10Rating',
#        'closest15Distance', 'closest15Price', 'closest15Rating',
#        'numberOfCompetitorsZipcode', 'avgPriceZipcode', 'avgRatingZipcode',
#        'numberOfCompetitorsCity', 'avgPriceCity', 'avgRatingCity'],
#       dtype='object')
