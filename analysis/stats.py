# Let's import data from the Yelp Database as a Data Frame:

import pandas as pd
import sqlite3 as sqlite
import os
import locale

try:
  locale.setlocale(locale.LC_ALL, 'en_US')
except:
  locale.setlocale(locale.LC_ALL, 'en_US.utf8')

def findCategoryPairs():
  categoryCityPairs = {}

  conn = sqlite.connect('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpdb.sqlite')
  conn.text_factory = str
  cur = conn.cursor()

  cur.execute('''SELECT city FROM Business''')
  cities = cur.fetchall()
  citySet = set(cities)

  cur.execute('''SELECT query_category, city, zip_code, price, rating FROM Business''')
  rows = cur.fetchall()

  print(len(rows))

  for category in ["restaurants", "bars", "coffee", "beautysvc", "food", "giftshops"]:
    for city in citySet:
      count = 0
      for row in rows:
        if row[1] == city[0]:
          if category == row[0]:
            count += 1
        keyPair = category + city[0]
      categoryCityPairs[keyPair] = [count, category, city[0]]
  # print(categoryCityPairs)
  l = 0
  for key, value in categoryCityPairs.items():
    if value[0] > 1860:
      # print(key, value[0])
      l += 1
  # print(l)

def findSFRegions():
  categoryZipPairsDowntown = {}
  categoryZipPairsOuter = {}

  conn = sqlite.connect('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpdb.sqlite')
  conn.text_factory = str
  cur = conn.cursor()

  cur.execute('''SELECT query_category, zip_code FROM Business WHERE city = ?''', ('San Francisco', ))
  zips = cur.fetchall()
  for category in ["restaurants", "bars", "coffee", "beautysvc", "food", "giftshops"]:
    downtown = 0
    outer = 0
    for zip_ in zips:
      if category == zip_[0]:
        if zip_[1] in ['94109','94102','94103','94107','94158','94108','94105','94111','94133']:
          downtown += 1
        else:
          outer += 1
    keyPair = category + zip_[1]
    categoryZipPairsDowntown[keyPair] = [downtown, category, zip_[1]]
    categoryZipPairsOuter[keyPair] = [outer, category, zip_[1]]

  # for k in categoryZipPairsDowntown.items():
  #   print('downtown', k)
  # for m in categoryZipPairsOuter.items():
  #   print('outer', m)

# if you exclude zip: '94110' in downtown
# ('downtown', ('coffee94132', [130, 'coffee', '94132']))
# ('downtown', ('food94132', [522, 'food', '94132']))
# ('downtown', ('beautysvc94132', [743, 'beautysvc', '94132']))
# ('downtown', ('bars94132', [407, 'bars', '94132']))
# ('downtown', ('restaurants94132', [1403, 'restaurants', '94132']))
# ('downtown', ('giftshops94132', [48, 'giftshops', '94132']))
# ('outer', ('coffee94132', [147, 'coffee', '94132']))
# ('outer', ('food94132', [922, 'food', '94132']))
# ('outer', ('beautysvc94132', [1375, 'beautysvc', '94132']))
# ('outer', ('bars94132', [276, 'bars', '94132']))
# ('outer', ('restaurants94132', [1739, 'restaurants', '94132']))
# ('outer', ('giftshops94132', [51, 'giftshops', '94132']))

# if you include zip: '94110'
# ('downtown', ('coffee94132', [149, 'coffee', '94132']))
# ('downtown', ('food94132', [723, 'food', '94132']))
# ('downtown', ('beautysvc94132', [948, 'beautysvc', '94132']))
# ('downtown', ('bars94132', [467, 'bars', '94132']))
# ('downtown', ('restaurants94132', [1775, 'restaurants', '94132']))
# ('downtown', ('giftshops94132', [54, 'giftshops', '94132']))
# ('outer', ('coffee94132', [128, 'coffee', '94132']))
# ('outer', ('food94132', [721, 'food', '94132']))
# ('outer', ('beautysvc94132', [1170, 'beautysvc', '94132']))
# ('outer', ('bars94132', [216, 'bars', '94132']))
# ('outer', ('restaurants94132', [1367, 'restaurants', '94132']))
# ('outer', ('giftshops94132', [45, 'giftshops', '94132']))

def numberOfBusinesses(business, region):
  conn = sqlite.connect('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite')
  conn.text_factory = str
  cur = conn.cursor()
  print(business, region)

  if region == 'Bay Area':
    cur.execute('''SELECT id FROM CleanBusinessData WHERE query_category = ? AND city != ?''', (business, 'San Francisco'))
  elif region == 'Peninsula':
    cur.execute('''SELECT id FROM CleanBusinessData WHERE query_category = ? AND city != ? AND city != ? AND city != ?''', (business, 'San Francisco', 'San Francisco - Downtown', 'San Francisco - Outer'))
  elif region == 'San Francisco':
    cur.execute('''SELECT id FROM CleanBusinessData WHERE query_category = ? AND city = ?''', (business, 'San Francisco'))
  elif region == 'Downtown SF':
    cur.execute('''SELECT id FROM CleanBusinessData WHERE query_category = ? AND city = ?''', (business, 'San Francisco - Downtown'))
  elif region == 'Outer SF':
    cur.execute('''SELECT id FROM CleanBusinessData WHERE query_category = ? AND city = ?''', (business, 'San Francisco - Outer'))
  elif region == 'East Bay':
    cur.execute('''SELECT id FROM CleanBusinessData WHERE query_category = ? AND region = ?''', (business, 'eastBay'))
  elif region == 'North Bay':
    cur.execute('''SELECT id FROM CleanBusinessData WHERE query_category = ? AND region = ?''', (business, 'northBay'))

# if region in [, 'North Bay']

  businesses = cur.fetchall()
  numberOfBusinessesFormatted = locale.format("%d", len(businesses), grouping=True)

  return numberOfBusinessesFormatted


def numberOfBusinessesForRegions():
  categoryRegionPairs = {}

  conn = sqlite.connect('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite')
  conn.text_factory = str
  cur = conn.cursor()

  categoryCount = {}
  cur.execute('''SELECT query_category, region FROM cleanBusinessData''')
  rows = cur.fetchall()

  for category in ["restaurants", "bars", "coffee", "beautysvc", "food", "giftshops"]:
    for region in ['eastBay', 'northBay', 'peninsula', '']:
      count = 0
      for row in rows:
        if category == row[0]:
          if region == row[1]:
            count += 1
      keyPair = category + ' ' + region
      categoryRegionPairs[keyPair] = [category, region, count]

  for key, value in categoryRegionPairs.items():
    print(key, value)




('bars eastBay', ['bars', 'eastBay', 234])
('coffee eastBay', ['coffee', 'eastBay', 154])
('restaurants northBay', ['restaurants', 'northBay', 141])
('coffee northBay', ['coffee', 'northBay', 11])

('food northBay', ['food', 'northBay', 62])
('beautysvc northBay', ['beautysvc', 'northBay', 178])
('giftshops northBay', ['giftshops', 'northBay', 12])

('beautysvc eastBay', ['beautysvc', 'eastBay', 1899])
('food eastBay', ['food', 'eastBay', 1075])
('beautysvc ', ['beautysvc', '', 0])
('bars ', ['bars', '', 0])
('bars peninsula', ['bars', 'peninsula', 1539])
('food ', ['food', '', 0])
('bars northBay', ['bars', 'northBay', 17])
('giftshops peninsula', ['giftshops', 'peninsula', 257])
('giftshops ', ['giftshops', '', 0])
('giftshops eastBay', ['giftshops', 'eastBay', 57])
('coffee ', ['coffee', '', 0])
('restaurants ', ['restaurants', '', 0])
('coffee peninsula', ['coffee', 'peninsula', 717])


('restaurants eastBay', ['restaurants', 'eastBay', 2628])
('food peninsula', ['food', 'peninsula', 3992])
('restaurants peninsula', ['restaurants', 'peninsula', 8057])
('beautysvc peninsula', ['beautysvc', 'peninsula', 5815])



  # st = set(cities)
  # lst = list(st)
  # print(sorted(lst))

# numberOfBusinessesForRegions()


('bars', 1107)
('beautysvc', 5780)
('food', 3698)
('coffee', 605)
('giftshops', 226)
('restaurants', 7687)
