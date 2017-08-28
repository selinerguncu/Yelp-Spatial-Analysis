import pandas as pd
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
  zipcodes = data['zipcode'].unique():
  categories = data['query_category'].unique():
  for category in categories:
    for zipcode in zipcodes:
      distanceAllBusinesses = pd.DataFrame(columns = ['distance', 'id', 'price', 'rating'])
      regionalData = data[data['zipcode'] == zipcode & data['query_category'] == category]
      for row in regionalData.itertuples():
      # for row_id, row in enumerate(data.values):
        for i in regionalData.itertuples():
          temp = pd.DataFrame()
          coordinate1 = (row['latitude'], row['longitude'])
          coordinate2 = (i['latitude'], i['longitude'])
          temp['distance'] = great_circle(coordinate1, coordinate1).miles
          temp['id'] = row['id']
          temp['price'] = i['price']
          temp['rating'] = i['rating']
          distanceAllBusinesses.append(temp)



  # print(type(data))
  # closest1 = {}
  # closest5 = {}
  # closest10 = {}
  # closest15 = {}


distanceFromTheClosest(getCleanData())

# number of competitors in: zipcode/city





# avg price of all in: zipcode/city




# avg rating of all in: zipcode/city





# weighted price of competitors closes: 2-5-10-15






# weighted rating of competitors closes: 2-5-10-15
