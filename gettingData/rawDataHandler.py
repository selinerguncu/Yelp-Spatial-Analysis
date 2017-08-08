from urllib import quote
from urllib import urlencode
from urllib2 import HTTPError

import sqlite3 as sqlite
import argparse
import yelpQuery
import os
import json
import pprint
import ast
import requests


global conn
global cur
global APP_PATH
global json_contents

APP_PATH = os.getcwd()

# DEFAULT_TERM = 'dinner'
# DEFAULT_LOCATION = 'San Francisco, CA'


class RawDataHandler(object):
  def __init__(self, input_values):
    self.SEARCH_LIMIT = 50 #max is 50
    self.RADIUS = 500

    self.latitude = input_values["latitude"]
    self.longitude = input_values["longitude"]
    self.category = input_values["category"]
    self.price = input_values["price"]

    try:
        self.json_contents = yelpQuery.query_api(self.latitude, self.longitude, self.category, self.price)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )

  def getRawJSON(self):
    conn = sqlite.connect(APP_PATH + '/data/yelpdb.sqlite')
    cur = conn.cursor()
    if self.json_contents == None:
      return

    cur.execute('''INSERT INTO JSON(SearchJson, ReviewsJson)
    VALUES (?, ?)''', (self.json_contents["searchJson"], self.json_contents["reviewsJson"]))

    conn.commit()

  def writeSearchTable(self):
    conn = sqlite.connect(APP_PATH + '/data/yelpdb.sqlite')
    cur = conn.cursor()

    if self.json_contents == None:
      return

    # convert string on the JSON db to dict with: dictionary = ast.literal_eval(string)
    searchJson = ast.literal_eval(self.json_contents["searchJson"])

    business_count = self.json_contents["total"]

    print len(searchJson["businesses"]), business_count

    businessIDs = []
    for i in range(len(searchJson["businesses"])): #will be range(business_count)
      businessID = searchJson["businesses"][i]["id"]
      cur.execute('''INSERT OR IGNORE INTO Search(query_latitude, query_longitude, query_category, query_price,
        business_count, businessID)
        VALUES (?, ?, ?, ?, ?, ?)''', (self.latitude, self.longitude, self.category, self.price,
          business_count, businessID))
      conn.commit()

      businessIDs.append(businessID)

    return businessIDs

  def writeBusinessTable(self):
    conn = sqlite.connect(APP_PATH + '/data/yelpdb.sqlite')
    cur = conn.cursor()

    if self.json_contents == None:
      return

    # convert string on the JSON db to dict with: dictionary = ast.literal_eval(string)
    searchJson = ast.literal_eval(self.json_contents["searchJson"])
    business_count = self.json_contents["total"]

    businessIDs = []
    for i in range(len(searchJson["businesses"])): #will be range(business_count)
      businessID = searchJson["businesses"][i]["id"]
      name = searchJson["businesses"][i]["name"]
      address = searchJson["businesses"][i]["location"]["address1"]
      city = searchJson["businesses"][i]["location"]["city"]
      country = searchJson["businesses"][i]["location"]["country"]
      zip_code = searchJson["businesses"][i]["location"]["zip_code"]
      url = searchJson["businesses"][i]["url"]
      price = searchJson["businesses"][i]["price"]
      rating = searchJson["businesses"][i]["rating"]
      review_count = searchJson["businesses"][i]["review_count"]
      alias = searchJson["businesses"][i]["categories"][0]["alias"]
      latitude = searchJson["businesses"][i]["coordinates"]["latitude"]
      longitude = searchJson["businesses"][i]["coordinates"]["longitude"]

      cur.execute('''INSERT OR IGNORE INTO Business(id, name, address, city, country, zip_code, url, price,
        rating, review_count, alias, latitude, longitude, query_latitude, query_longitude, query_category, query_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (businessID, name, address, city,
          country, zip_code, url, price, rating, review_count, alias, latitude, longitude,
          self.latitude, self.longitude, self.category, self.price))

      conn.commit()

  def writeReviewsTable(self):
    conn = sqlite.connect(APP_PATH + '/data/yelpdb.sqlite')
    cur = conn.cursor()

    if self.json_contents == None:
      return

    cur.execute('''SELECT id FROM Business WHERE query_latitude = ? AND query_longitude = ? AND
      query_category = ? AND query_price = ?''',
      (self.latitude, self.longitude, self.category, self.price))
    IDs = cur.fetchall()

    API_HOST = 'https://api.yelp.com'
    BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
    TOKEN_PATH = '/oauth2/token'

    bearer_token = yelpQuery.obtain_bearer_token(API_HOST, TOKEN_PATH)

    url_params = {
    'latitude': self.latitude,
    'longitude': self.longitude,
    'categories': self.category,
    'price': self.price,
    'limit': self.SEARCH_LIMIT,
    'radius': self.RADIUS
    }
    print "len", len(IDs)
    for i in range(len(IDs)):
      business_id = IDs[i][0]
      print "business_id", business_id
      review_path = BUSINESS_PATH + business_id + '/reviews'
      response = yelpQuery.request(API_HOST, review_path, bearer_token, url_params)
      if not "reviews" in response.keys():
        print response
        return
      reviewsPerBusiness = response["reviews"]
      for review in range(3):
        try: #take care of the error if rewiews are less than 3
          rating = reviewsPerBusiness[review]["rating"]
          content = reviewsPerBusiness[review]["text"]
          time_created = reviewsPerBusiness[review]["time_created"]
          cur.execute('''INSERT OR IGNORE INTO Reviews(business_id, rating, content, time_created)
          VALUES (?, ?, ?, ?)''', (business_id, rating, content, time_created))
          conn.commit()
        except:
          pass
    return

