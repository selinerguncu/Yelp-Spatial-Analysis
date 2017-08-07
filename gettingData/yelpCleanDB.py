import sqlite3 as sqlite

import os

global appPath
appPath = os.getcwd()

conn = sqlite.connect(appPath + '/data/yelpCleanDB.sqlite')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS CleanBusinessData;


CREATE TABLE CleanBusinessData (
  id TEXT,
  rating INTEGER,
  price TEXT,
  county TEXT,
  query_latitude INTEGER,
  query_longitude INTEGER,
  population INTEGER,
  city TEXT,
  review_count INTEGER,
  area INTEGER,
  zipcode TEXT,
  longitude INTEGER,
  query_category TEXT,
  latitude INTEGER,
  query_price TEXT,
  region TEXT
)

''')

conn.commit()
conn.close()
