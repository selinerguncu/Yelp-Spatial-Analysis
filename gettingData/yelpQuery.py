# from __future__ import print_function

import argparse
import json
# import pprint
import requests
import sys
import urllib

from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode

import sqlite3 as sqlite
import os
import ast


appPath = os.getcwd()

if "YELP_CLIENT_ID" in os.environ.keys():
  CLIENT_ID = os.environ["YELP_CLIENT_ID"]
else:
  print "YELP_CLIENT_ID env var should be exported!"
  sys.exit()

if "YELP_CLIENT_SECRET" in os.environ.keys():
  CLIENT_SECRET = os.environ["YELP_CLIENT_SECRET"]
else:
  print "YELP_CLIENT_SECRET env var should be exported!"
  sys.exit()

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

# Defaults for our simple example.
# DEFAULT_TERM = 'dinner'
# DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 50 #max is 50
RADIUS = 500


def obtain_bearer_token(host, path):
  url = '{0}{1}'.format(host, quote(path.encode('utf8')))
  assert CLIENT_ID, "Please supply your client_id."
  assert CLIENT_SECRET, "Please supply your client_secret."
  data = urlencode({
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': GRANT_TYPE,
  })
  headers = {
    'content-type': 'application/x-www-form-urlencoded',
  }
  response = requests.request('POST', url, data=data, headers=headers)
  bearer_token = response.json()['access_token']

  return bearer_token


def request(host, path, bearer_token, url_params):
  url = '{0}{1}'.format(host, quote(path.encode('utf8')))
  headers = {
    'Authorization': 'Bearer %s' % bearer_token,
  }

  response = requests.request('GET', url, headers=headers, params=url_params)
  # print response
  return response.json()


def search(bearer_token, latitude, longitude, categories, price):
# def search(bearer_token, term, location):
#     url_params = {
#         'term': term.replace(' ', '+'),
#         'location': location.replace(' ', '+'),
#         'limit': SEARCH_LIMIT
#     }

  url_params = {
    'latitude': latitude,
    'longitude': longitude,
    'categories': categories,
    'price': price,
    'limit': SEARCH_LIMIT,
    'radius': RADIUS
  }

  return request(API_HOST, SEARCH_PATH, bearer_token, url_params)


# def get_business(bearer_token, business_id):

#   business_path = BUSINESS_PATH + business_id
#   allBusinesses = request(API_HOST, business_path, bearer_token)
#   # print(type(allBusinesses))
#   return allBusinesses


# def get_reviews(bearer_token, business_id):

#   review_path = BUSINESS_PATH + business_id + '/reviews'
#   allReviews = request(API_HOST, review_path, bearer_token)
#   return allReviews


def query_api(latitude, longitude, categories, price):
# def query_api(term, location):
  bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

  response = search(bearer_token, latitude, longitude, categories, price)

  businesses = response.get('businesses')
  total = response.get('total')

  if not businesses:
    # print(u'No businesses for {0} in {1} found.'.format(term, location))
    return

  business_id = businesses[0]['id'] # bu sadece ilk restoranin review ini yaziyor JSON DB ye

  # responseReviews = get_reviews(bearer_token, business_id)
  responseReviews = {}

  # reviews = responseReviews.get('reviews')

  json_contents = {}
  json_contents["searchJson"] = str(response)
  json_contents["reviewsJson"] = str(responseReviews)
  # json_contents["term"] = term
  # json_contents["location"] = location
  json_contents["total"] = total
  json_contents["latitude"] = latitude
  json_contents["longitude"] = longitude
  json_contents["category"] = categories
  json_contents["price"] = price

  return json_contents

# def main():
#   parser = argparse.ArgumentParser()

#   parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
#             type=str, help='Search term (default: %(default)s)')
#   parser.add_argument('-l', '--location', dest='location',
#             default=DEFAULT_LOCATION, type=str,
#             help='Search location (default: %(default)s)')

#   input_values = parser.parse_args()

#   try:
#     json_contents = query_api(input_values.term, input_values.location)
#   except HTTPError as error:
#     sys.exit(
#       'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
#         error.code,
#         error.url,
#         error.read(),
#       )
#     )

  # return json_contents

if __name__ == '__main__':
  main()
