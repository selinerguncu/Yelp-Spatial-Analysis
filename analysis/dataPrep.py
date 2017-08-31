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
  conn = sqlite.connect("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite")
  cur = conn.cursor()
  # distanceAllBusinesses = pd.read_sql_query("SELECT * FROM DistanceAllBusinesses", conn)
  # distanceAllBusinesses = pd.DataFrame(columns = ['distance', 'id', 'price', 'rating'])
  for category in categories:
    print(category)
    for zipcode in zipcodes:
      print(zipcode)
      regionalData = data[(data['zipcode'] == zipcode) & (data['query_category'] == category)]
      # for row in regionalData.itertuples():
      for index, row in regionalData.iterrows():
        coordinate1 = (row['latitude'], row['longitude'])
        # coordinate1 = (row[14], row[12])
        # print('row', row)
        # sys.exit()
      # for row_id, row in enumerate(data.values):
        # for i in regionalData.itertuples():
        for index, i in regionalData.iterrows():
          if row['id'] != i['id']:
          # if row != i:
            coordinate2 = (i['latitude'], i['longitude'])
            # coordinate2 = (i[14], i[12])
            # distance = great_circle(coordinate1, coordinate2).miles
            # businessID = row[1]
            # price = int(i[15])
            # rating = i[2]
            distance = great_circle(coordinate1, coordinate2).miles
            businessID = row['id']
            price = int(i['query_price'])
            rating = i['rating']
            # temp.extend([distance, businessID, price, rating])
            # distanceAllBusinesses.append(temp)
            cur.execute('''INSERT INTO DistanceAllBusinesses(distance, id, price, rating)
              VALUES (?, ?, ?, ?)''', (distance, businessID, price, rating))
            # cur.execute('''UPDATE DistanceAllBusinesses SET distance = ?
            #   WHERE id = ? AND price = ? AND rating = ?''', (distance, businessID, price, rating))
  conn.commit()
            # distanceAllBusinesses.loc[len(distanceAllBusinesses)] = [distance, businessID, price, rating]
            # print('i', distanceAllBusinesses)
  # sys.exit()

  # columns = ['id', 'closest2Distance','closest2Price','closest2Rating',
  #                    'closest5Distance','closest5Price','closest5Rating',
  #                    'closest10Distance','closest10Price','closest10Rating',
  #                    'closest15Distance','closest15Price','closest15Rating']
  # distanceSelectedBusinesses = pd.DataFrame(columns = columns)
  businesses = data['id'].unique()
  distanceAllBusinesses = pd.read_sql_query("SELECT * FROM DistanceAllBusinesses", conn)
  for business in businesses[0:100]:
    businessID = business
    closest2 = distanceAllBusinesses[distanceAllBusinesses['id'] == business].nsmallest(2, 'distance')
    # print(closest2.head())
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

    cur.execute('''INSERT INTO DistanceSelectedBusinesses(closest2Distance, closest2Price, closest2Rating,
      closest5Distance, closest5Price, closest5Rating,
      closest10Distance, closest10Price, closest10Rating,
      closest15Distance, closest15Price, closest15Rating, id)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
      (closest2Distance, closest2Price, closest2Rating,
        closest5Distance, closest5Price, closest5Rating,
        closest10Distance, closest10Price, closest10Rating,
        closest15Distance, closest15Price, closest15Rating, businessID))
  conn.commit()

    # distanceSelectedBusinesses.loc[len(distanceSelectedBusinesses)] = [businessID, closest2Distance, closest2Price, closest2Rating, closest5Distance, closest5Price, closest5Rating, closest10Distance, closest10Price, closest10Rating, closest15Distance, closest15Price, closest15Rating]

  # merge data with distanceSelectedBusiness:
  distanceSelectedBusinesses = pd.read_sql_query("SELECT * FROM DistanceSelectedBusinesses", conn)

  dataDistanceAdded = pd.merge(data, distanceSelectedBusinesses, how='inner', on='id',
    left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=False)

  dataDistanceAdded.to_sql('DataDistanceAdded', conn)
  conn.commit()
  print('step 2 finished')
  return dataDistanceAdded


def addCompetitionZipcode(data):
  # columns = ['zipcode', 'numberOfCompetitorsZipcode','avgPriceZipcode','avgRatingZipcode']
  # dataCompetitionZipcode = pd.DataFrame(columns = columns)
  conn = sqlite.connect("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite")
  cur = conn.cursor()
  zipcodes = data['zipcode'].unique()
  categories = data['query_category'].unique()

  for category in categories:
    for zipcode in zipcodes:
      regionalData = data[(data['zipcode'] == zipcode) & (data['query_category'] == category)]

      zipcode = zipcode
      numberOfCompetitorsZipcode = len(regionalData.index)
      avgPriceZipcode = regionalData['query_price'].mean()
      avgRatingZipcode = regionalData['rating'].mean()

      cur.execute('''INSERT INTO CompetitionZipcode(numberOfCompetitorsZipcode,
        avgPriceZipcode, avgRatingZipcode, zipcode) VALUES (?, ?, ?, ?)''',
        (numberOfCompetitorsZipcode, avgPriceZipcode, avgRatingZipcode, zipcode))
  conn.commit()
      # dataCompetitionZipcode.loc[len(dataCompetitionZipcode)] = [zipcode, numberOfCompetitorsZipcode, avgPriceZipcode, avgRatingZipcode]

  competitionZipcode = pd.read_sql_query("SELECT * FROM CompetitionZipcode", conn)
  dataCompetitionZipcodeAdded = pd.merge(data, competitionZipcode, how='inner', on='zipcode',
    left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=False)


  dataCompetitionZipcodeAdded.to_sql('DataCompetitionZipcodeAdded', conn)
  conn.commit()
  # print(dataCompetitionZipcodeAdded.head())
  print('step 3 finished')

  return dataCompetitionZipcodeAdded
# addCompetitionZipcode(distanceFromTheClosest(getCleanData()))
# sys.exit()


def addCompetitionCity(data):
  # columns = ['city', 'numberOfCompetitorsCity','avgPriceCity','avgRatingCity']
  # dataCompetitionCity = pd.DataFrame(columns = columns)
  conn = sqlite.connect("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite")
  cur = conn.cursor()
  cities = data['city'].unique()
  categories = data['query_category'].unique()

  for category in categories:
    for city in cities:
      regionalData = data[(data['city'] == city) & (data['query_category'] == category)]

      city = city
      numberOfCompetitorsCity = len(regionalData.index)
      avgPriceCity = regionalData['query_price'].mean()
      avgRatingCity = regionalData['rating'].mean()

      cur.execute('''INSERT INTO CompetitionCity(numberOfCompetitorsCity,
        avgPriceCity, avgRatingCity, city) VALUES (?, ?, ?, ?)''',
        (numberOfCompetitorsCity, avgPriceCity, avgRatingCity, city))
  conn.commit()
      # dataCompetitionCity.loc[len(dataCompetitionCity)] = [city, numberOfCompetitorsCity, avgPriceCity, avgRatingCity]

  competitionCity = pd.read_sql_query("SELECT * FROM CompetitionCity", conn)
  dataCompetitionCityAdded = pd.merge(data, competitionCity, how='inner', on='city',
    left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=False)

  dataCompetitionCityAdded.to_sql('DataCompetitionCityAdded', conn)
  print('step 4 finished')
  conn.commit()
  return dataCompetitionCityAdded


dataCompetitionCityAdded = addCompetitionCity(addCompetitionZipcode(distanceFromTheClosest(getCleanData())))

print(dataCompetitionCityAdded.head())

#### OLD CODE ##### doesn't work for merging - 0 or None values come for the newly added cells

# def addCompetitionCity(data):
#   columns = ['numberOfCompetitorsCity','avgPriceCity','avgRatingCity']

#   temp = pd.DataFrame([[0,0,0]], index=data.index, columns = columns)

#   dataCompetitionCityAdded = data.join(temp, how='outer')

#   cities = data['city'].unique()
#   categories = data['query_category'].unique()

#   for category in categories:
#     for city in cities[0:1]:
#       regionalData = dataCompetitionCityAdded[(dataCompetitionCityAdded['city'] == city) & (dataCompetitionCityAdded['query_category'] == category)]
#       numberOfCompetitorsCity = len(regionalData.index)
#       avgPriceCity = regionalData['query_price'].mean()
#       avgRatingCity = regionalData['rating'].mean()

#       for index, row in dataCompetitionCityAdded.iterrows():
#         if row['city'] == city and row['query_category'] == category:
#           row['numberOfCompetitorsCity'] = numberOfCompetitorsCity
#           row['avgPriceCity'] = avgPriceCity
#           row['avgRatingCity'] = avgRatingCity
#         if row['numberOfCompetitorsCity'] != 0 and row['numberOfCompetitorsCity'] != 0 and row['closest10Price'] != np.nan:
#           print(row)

#   # data = dataCompetitionCityAdded
#   print(dataCompetitionCityAdded.columns)
#   return dataCompetitionCityAdded

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


# CREATE TABLE DataDistanceAdded (
#   id TEXT,
#   rating INTEGER,
#   price TEXT,
#   county TEXT,
#   query_latitude INTEGER,
#   query_longitude INTEGER,
#   population INTEGER,
#   city TEXT,
#   review_count INTEGER,
#   area INTEGER,
#   zipcode TEXT,
#   longitude INTEGER,
#   query_category TEXT,
#   latitude INTEGER,
#   query_price INTEGER,
#   region TEXT,
#   distance INTEGER,
#   closest2Distance INTEGER,
#   closest2Price INTEGER,
#   closest2Rating INTEGER,
#   closest5Distance INTEGER,
#   closest5Price INTEGER,
#   closest5Rating INTEGER,
#   closest10Distance INTEGER,
#   closest10Price INTEGER,
#   closest10Rating INTEGER,
#   closest15Distance INTEGER,
#   closest15Price INTEGER,
#   closest15Rating INTEGER
# );

# CREATE TABLE DataCompetitionZipcodeAdded (
#   id TEXT,
#   rating INTEGER,
#   price TEXT,
#   county TEXT,
#   query_latitude INTEGER,
#   query_longitude INTEGER,
#   population INTEGER,
#   city TEXT,
#   review_count INTEGER,
#   area INTEGER,
#   zipcode TEXT,
#   longitude INTEGER,
#   query_category TEXT,
#   latitude INTEGER,
#   query_price INTEGER,
#   region TEXT,
#   distance INTEGER
#   closest2Distance INTEGER,
#   closest2Price INTEGER,
#   closest2Rating INTEGER,
#   closest5Distance INTEGER,
#   closest5Price INTEGER,
#   closest5Rating INTEGER,
#   closest10Distance INTEGER,
#   closest10Price INTEGER,
#   closest10Rating INTEGER,
#   closest15Distance INTEGER,
#   closest15Price INTEGER,
#   closest15Rating INTEGER,
#   numberOfCompetitorsZipcode INTEGER,
#   avgPriceZipcode INTEGER,
#   avgRatingZipcode INTEGER
# );


# CREATE TABLE DataCompetitionCityAdded (
#   id TEXT,
#   rating INTEGER,
#   price TEXT,
#   county TEXT,
#   query_latitude INTEGER,
#   query_longitude INTEGER,
#   population INTEGER,
#   city TEXT,
#   review_count INTEGER,
#   area INTEGER,
#   zipcode TEXT,
#   longitude INTEGER,
#   query_category TEXT,
#   latitude INTEGER,
#   query_price INTEGER,
#   region TEXT,
#   distance INTEGER
#   closest2Distance INTEGER,
#   closest2Price INTEGER,
#   closest2Rating INTEGER,
#   closest5Distance INTEGER,
#   closest5Price INTEGER,
#   closest5Rating INTEGER,
#   closest10Distance INTEGER,
#   closest10Price INTEGER,
#   closest10Rating INTEGER,
#   closest15Distance INTEGER,
#   closest15Price INTEGER,
#   closest15Rating INTEGER,
#   numberOfCompetitorsZipcode INTEGER,
#   avgPriceZipcode INTEGER,
#   avgRatingZipcode INTEGER,
#   numberOfCompetitorsCity INTEGER,
#   avgPriceCity INTEGER,
#   avgRatingCity INTEGER
# );
