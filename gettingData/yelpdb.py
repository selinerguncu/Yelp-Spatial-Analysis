import sqlite3

import os

global appPath
appPath = os.getcwd()

conn = sqlite3.connect(appPath + '/data/yelpdb.sqlite')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS JSON;
DROP TABLE IF EXISTS Search;
DROP TABLE IF EXISTS Business;
DROP TABLE IF EXISTS Reviews;


CREATE TABLE JSON (
    id              INTEGER PRIMARY KEY,
    SearchJson   TEXT,
    ReviewsJson   TEXT
);

CREATE TABLE Search (
  id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  business_count INTEGER,
  businessID TEXT UNIQUE,
  query_latitude INTEGER,
  query_longitude INTEGER,
  query_category TEXT,
  query_price TEXT
);

CREATE TABLE Business (
  id  TEXT NOT NULL PRIMARY KEY UNIQUE,
  name TEXT,
  address TEXT,
  city TEXT,
  country TEXT,
  zip_code TEXT,
  url TEXT,
  price TEXT,
  rating INTEGER,
  review_count INTEGER,
  alias TEXT,
  latitude INTEGER,
  longitude INTEGER,
  query_latitude INTEGER,
  query_longitude INTEGER,
  query_category TEXT,
  query_price TEXT
);

CREATE TABLE Reviews (
  id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  rating INTEGER,
  content TEXT,
  time_created TEXT,
  business_id TEXT,
  FOREIGN KEY(business_id) REFERENCES Business(id)
)

''')

conn.commit()
conn.close()
