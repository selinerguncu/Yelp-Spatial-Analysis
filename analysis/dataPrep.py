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
  print(type(data))

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
          # print('i', i)
          if row != i:
            coordinate2 = (i[14], i[12])
            distance = great_circle(coordinate1, coordinate2).miles
            businessID = row[1]
            price = i[15]
            rating = i[2]
            # temp.extend([distance, businessID, price, rating])
            # distanceAllBusinesses.append(temp)
            distanceAllBusinesses.loc[len(distanceAllBusinesses)] = [distance, businessID, price, rating]
            # for index, row in dataDistanceAdded.iterrows():
            #   if row['id'] == business:
            #     row['distance'] = distance
            #     row['id'] = businessID
            #     row['price'] = price
            #     row['rating'] = rating

            # print(distanceAllBusinesses.head())
  print(distanceAllBusinesses.head())
  # sys.exit()

  businesses = data['id'].unique()
  for business in businesses:
    closest2 = distanceAllBusinesses[distanceAllBusinesses['id'] == business].nsmallest(2, 'distance')
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

    dataDistanceAdded = distanceAllBusinesses.join(temp, how='outer')

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

  print(dataDistanceAdded.head())
  return dataDistanceAdded

distanceFromTheClosest(getCleanData())

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
    for zipcode in zipcodes:
      regionalData = dataCompetitionZipcodeAdded[(dataCompetitionZipcodeAdded['zipcode'] == zipcode) & (dataCompetitionZipcodeAdded['query_category'] == category)]
      numberOfCompetitorsZipcode = len(regionalData.index)
      avgPriceZipcode = regionalData['price'].mean()
      avgRatingZipcode = regionalData['rating'].mean()

      for index, row in dataCompetitionZipcodeAdded.iterrows():
        if row['zipcode'] == zipcode and row['query_category'] == category:
          row['numberOfCompetitorsZipcode'] = numberOfCompetitorsZipcode
          row['avgPriceZipcode'] = avgPriceZipcode
          row['avgRatingZipcode'] = avgRatingZipcode

  # data = dataCompetitionZipcodeAdded

  return dataCompetitionZipcodeAdded

