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
  data = pd.read_sql_query("SELECT * FROM CleanBusinessData WHERE city != 'San Francisco - Downtown' AND city != 'San Francisco - Outer' ", conn)

  # verify that result of SQL query is stored in the dataframe
  # high = df[df['review_count']>500]['city']
  data = data[data['city'] != 'San Francisco - Downtown']
  data = data[data['city'] != 'San Francisco - Outer']
  print(len(data))
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
  i = 0
  for business in businesses:
    closest2 = distanceAllBusinesses[distanceAllBusinesses['id'] == business].nsmallest(3, 'distance')
    # print(closest2.head())
    closest2Distance = closest2['distance'].mean()
    print('distance mean')
    closest2Price = (closest2['price'].sum() - business['price']) / 2
    # print('price mean')
    closest2Rating = (closest2['rating'].sum() - business['rating']) / 2
    # print('rating mean')

    closest5 = distanceAllBusinesses[distanceAllBusinesses['id'] == business].nsmallest(6, 'distance')
    closest5Distance = closest5['distance'].mean()
    closest5Price = (closest5['price'].sum() - business['price']) / 5
    closest5Rating = (closest5['rating'].sum() - business['rating']) / 5
    # print('closest5')

    closest10 = distanceAllBusinesses[distanceAllBusinesses['id'] == business].nsmallest(11, 'distance')
    closest10Distance = closest10['distance'].mean()
    closest10Price = (closest10['price'].sum() - business['price']) / 10
    closest10Rating = (closest10['rating'].sum() - business['rating']) / 10
    # print('closest10')

    closest15 = distanceAllBusinesses[distanceAllBusinesses['id'] == business].nsmallest(16, 'distance')
    closest15Distance = closest15['distance'].mean()
    closest15Price = (closest15['price'].sum() - business['price']) / 15
    closest15Rating = (closest15['rating'].sum() - business['rating']) / 15
    # print('closest15')

    # print('insert into')
    cur.execute('''INSERT INTO DistanceSelectedBusinesses(closest2Distance, closest2Price, closest2Rating,
      closest5Distance, closest5Price, closest5Rating,
      closest10Distance, closest10Price, closest10Rating,
      closest15Distance, closest15Price, closest15Rating, id)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
      (closest2Distance, closest2Price, closest2Rating,
        closest5Distance, closest5Price, closest5Rating,
        closest10Distance, closest10Price, closest10Rating,
        closest15Distance, closest15Price, closest15Rating, business))
    i += 1
    print(i)
    conn.commit()

    # distanceSelectedBusinesses.loc[len(distanceSelectedBusinesses)] = [businessID, closest2Distance, closest2Price, closest2Rating, closest5Distance, closest5Price, closest5Rating, closest10Distance, closest10Price, closest10Rating, closest15Distance, closest15Price, closest15Rating]

  #merge Tables:

  print('will create DataDistanceAdded')
  cur.execute('''INSERT INTO DataDistanceAdded (id, rating, price, county, query_latitude, query_longitude, population,
    city, review_count, area, zipcode, longitude, category, latitude,
    query_price, region, closest2Distance, closest2Price, closest2Rating,
    closest5Distance, closest5Price, closest5Rating, closest10Distance, closest10Price,
    closest10Rating, closest15Distance, closest15Price, closest15Rating)
    SELECT CleanBusinessData.*,
    distanceSelectedBusinesses.closest2Distance, distanceSelectedBusinesses.closest2Price, distanceSelectedBusinesses.closest2Rating,
    distanceSelectedBusinesses.closest5Distance, distanceSelectedBusinesses.closest5Price, distanceSelectedBusinesses.closest5Rating,
    distanceSelectedBusinesses.closest10Distance, distanceSelectedBusinesses.closest10Price, distanceSelectedBusinesses.closest10Rating,
    distanceSelectedBusinesses.closest15Distance, distanceSelectedBusinesses.closest15Price, distanceSelectedBusinesses.closest15Rating
    FROM CleanBusinessData LEFT JOIN distanceSelectedBusinesses USING(id)''')
  print('DataDistanceAdded created')
  # merge data with distanceSelectedBusiness:
  # distanceSelectedBusinesses = pd.read_sql_query("SELECT * FROM DistanceSelectedBusinesses", conn)

  # id, CleanBusinessData.rating, CleanBusinessData.price,
  #   CleanBusinessData.county, CleanBusinessData.query_latitude, CleanBusinessData.query_longitude,
  #   CleanBusinessData.population, CleanBusinessData.city, CleanBusinessData.review_count, CleanBusinessData.area,
  #   CleanBusinessData.zipcode, CleanBusinessData.longitude, CleanBusinessData.category,
  #   CleanBusinessData.latitude, CleanBusinessData.query_price, CleanBusinessData.region

  # dataDistanceAdded = pd.merge(data, distanceSelectedBusinesses, how='inner', on='id',
  #   left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=False)

  # dataDistanceAdded.to_sql('DataDistanceAdded', conn)
  conn.commit()
  print('step 2 finished')
  # return dataDistanceAdded


def addCompetitionZipcode():
  conn = sqlite.connect("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite")
  cur = conn.cursor()
  dataDistanceAdded = pd.read_sql_query("SELECT * FROM DataDistanceAdded", conn)
  zipcodes = dataDistanceAdded['zipcode'].unique()
  categories = dataDistanceAdded['category'].unique()
  i = 0
  for category in categories:
    for zipcode in zipcodes:
      print(zipcode, 'competition')
      regionalData = dataDistanceAdded[(dataDistanceAdded['zipcode'] == zipcode) & (dataDistanceAdded['category'] == category)]

      # zipcode = regionalData['zipcode']
      numberOfCompetitorsZipcode = len(regionalData.index)
      avgPriceZipcode = regionalData['query_price'].mean()
      avgRatingZipcode = regionalData['rating'].mean()

      if avgRatingZipcode is not None:
        cur.execute('''INSERT INTO CompetitionZipcode(numberOfCompetitorsZipcode,
          avgPriceZipcode, avgRatingZipcode, zipcode, category) VALUES (?, ?, ?, ?, ?)''',
          (numberOfCompetitorsZipcode, avgPriceZipcode, avgRatingZipcode, zipcode, category))
      conn.commit()
      i += 1
      print(i, 'zipcode added')
      # dataCompetitionZipcode.loc[len(dataCompetitionZipcode)] = [zipcode, numberOfCompetitorsZipcode, avgPriceZipcode, avgRatingZipcode]

  print('DataCompetitionZipcodeAdded will create')
  cur.execute('''INSERT INTO DataCompetitionZipcodeAdded (id, rating, price, county, query_latitude, query_longitude, population,
    city, review_count, area, zipcode, longitude, category, latitude,
    query_price, region, closest2Distance, closest2Price, closest2Rating,
    closest5Distance, closest5Price, closest5Rating, closest10Distance, closest10Price,
    closest10Rating, closest15Distance, closest15Price, closest15Rating,
    numberOfCompetitorsZipcode, avgPriceZipcode, avgRatingZipcode)
    SELECT DataDistanceAdded.*,
    CompetitionZipcode.numberOfCompetitorsZipcode, CompetitionZipcode.avgPriceZipcode, CompetitionZipcode.avgRatingZipcode
    FROM DataDistanceAdded LEFT JOIN CompetitionZipcode USING(zipcode, category)''')
  # competitionZipcode = pd.read_sql_query("SELECT * FROM CompetitionZipcode", conn)
  # dataCompetitionZipcodeAdded = pd.merge(data, competitionZipcode, how='inner', on='zipcode',
  #   left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=False)

  # SELECT DataDistanceAdded.id, DataDistanceAdded.rating, DataDistanceAdded.price,
  #   DataDistanceAdded.county, DataDistanceAdded.query_latitude, DataDistanceAdded.query_longitude,
  #   DataDistanceAdded.population, DataDistanceAdded.city, DataDistanceAdded.review_count, DataDistanceAdded.area,
  #   DataDistanceAdded.zipcode, DataDistanceAdded.longitude, DataDistanceAdded.query_category,
  #   DataDistanceAdded.latitude, DataDistanceAdded.query_price, DataDistanceAdded.region,
  #   DataDistanceAdded.closest5Distance, DataDistanceAdded.closest5Price, DataDistanceAdded.closest5Rating, DataDistanceAdded.closest10Distance, DataDistanceAdded.closest10Price,
  #   DataDistanceAdded.closest10Rating, DataDistanceAdded.closest15Distance, DataDistanceAdded.closest15Price, DataDistanceAdded.closest15Rating,
  #   CompetitionZipcode.numberOfCompetitorsZipcode, CompetitionZipcode.avgPriceZipcode, CompetitionZipcode.avgRatingZipcode


  # dataCompetitionZipcodeAdded.to_sql('DataCompetitionZipcodeAdded', conn)
  conn.commit()
  # print(dataCompetitionZipcodeAdded.head())
  print('step 3 finished')

  # return dataCompetitionZipcodeAdded
# addCompetitionZipcode(distanceFromTheClosest(getCleanData()))
# sys.exit()


def addCompetitionCity():
  conn = sqlite.connect("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite")
  cur = conn.cursor()
  dataCompetitionZipcodeAdded = pd.read_sql_query("SELECT * FROM DataCompetitionZipcodeAdded", conn)
  cities = dataCompetitionZipcodeAdded['city'].unique()
  categories = dataCompetitionZipcodeAdded['category'].unique()
  i = 0
  for category in categories:
    for city in cities:
      print('city', city)
      regionalData = dataCompetitionZipcodeAdded[(dataCompetitionZipcodeAdded['city'] == city) & (dataCompetitionZipcodeAdded['category'] == category)]

      numberOfCompetitorsCity = len(regionalData.index)
      avgPriceCity = regionalData['query_price'].mean()
      avgRatingCity = regionalData['rating'].mean()

      if avgRatingCity is not None:
        cur.execute('''INSERT INTO CompetitionCity(numberOfCompetitorsCity,
          avgPriceCity, avgRatingCity, city, category) VALUES (?, ?, ?, ?, ?)''',
          (numberOfCompetitorsCity, avgPriceCity, avgRatingCity, city, category))
      conn.commit()
      i += 1
      print(i, 'city added')
      # dataCompetitionCity.loc[len(dataCompetitionCity)] = [city, numberOfCompetitorsCity, avgPriceCity, avgRatingCity]

  # competitionCity = pd.read_sql_query("SELECT * FROM CompetitionCity", conn)
  # dataCompetitionCityAdded = pd.merge(data, competitionCity, how='inner', on='city',
  #   left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=False)
  print('dataCompetitionCityAdded will create')
  # dataCompetitionCityAdded.to_sql('DataCompetitionCityAdded', conn)
  cur.execute('''INSERT INTO DataCompetitionCityAdded (id, rating, price, county, query_latitude, query_longitude, population,
    city, review_count, area, zipcode, longitude, category, latitude,
    query_price, region, closest2Distance, closest2Price, closest2Rating,
    closest5Distance, closest5Price, closest5Rating, closest10Distance, closest10Price,
    closest10Rating, closest15Distance, closest15Price, closest15Rating,
    numberOfCompetitorsZipcode, avgPriceZipcode, avgRatingZipcode,
    numberOfCompetitorsCity, avgPriceCity, avgRatingCity)
    SELECT DataCompetitionZipcodeAdded.*,
    CompetitionCity.numberOfCompetitorsCity, CompetitionCity.avgPriceCity, CompetitionCity.avgRatingCity
    FROM DataCompetitionZipcodeAdded LEFT JOIN CompetitionCity USING(city, category)''')
  print('step 4 finished')
  conn.commit()
  # return dataCompetitionCityAdded


# id, DataCompetitionZipcodeAdded.rating, DataCompetitionZipcodeAdded.price,
#     DataCompetitionZipcodeAdded.county, DataCompetitionZipcodeAdded.query_latitude, DataCompetitionZipcodeAdded.query_longitude,
#     DataCompetitionZipcodeAdded.population, DataCompetitionZipcodeAdded.city, DataCompetitionZipcodeAdded.review_count, DataCompetitionZipcodeAdded.area,
#     DataCompetitionZipcodeAdded.zipcode, DataCompetitionZipcodeAdded.longitude, DataCompetitionZipcodeAdded.query_category,
#     DataCompetitionZipcodeAdded.latitude, DataCompetitionZipcodeAdded.query_price, DataCompetitionZipcodeAdded.region,
#     DataCompetitionZipcodeAdded.closest2Distance, DataCompetitionZipcodeAdded.closest2Price, DataCompetitionZipcodeAdded.closest2Rating,
#     DataCompetitionZipcodeAdded.closest5Distance, DataCompetitionZipcodeAdded.closest5Price, DataCompetitionZipcodeAdded.closest5Rating,
#     DataCompetitionZipcodeAdded.closest10Distance, DataCompetitionZipcodeAdded.closest10Price, DataCompetitionZipcodeAdded.closest10Rating,
#     DataCompetitionZipcodeAdded.closest15Distance, DataCompetitionZipcodeAdded.closest15Price, DataCompetitionZipcodeAdded.closest15Rating,
#     DataCompetitionZipcodeAdded.numberOfCompetitorsZipcode, DataCompetitionZipcodeAdded.avgPriceZipcode, DataCompetitionZipcodeAdded.avgRatingZipcode,
distanceFromTheClosest(getCleanData())
addCompetitionZipcode()
addCompetitionCity()

# print(dataCompetitionCityAdded.head())

# Index(['id', 'rating', 'price', 'county', 'query_latitude', 'query_longitude',
#        'population', 'city', 'review_count', 'area', 'zipcode', 'longitude',
#        'query_category', 'latitude', 'query_price', 'region',
#        'closest2Distance', 'closest2Price', 'closest2Rating',
#        'closest5Distance', 'closest5Price', 'closest5Rating',
#        'closest10Distance', 'closest10Price', 'closest10Rating',
#        'closest15Distance', 'closest15Price', 'closest15Rating',
#        'numberOfCompetitorsZipcode', 'avgPriceZipcode', 'avgRatingZipcode',
#        'numberOfCompetitorsCity', 'avgPriceCity', 'avgRatingCity'],
#       dtype='
