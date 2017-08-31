import sqlite3 as sqlite
# import cleanData

import os

global appPath
appPath = os.getcwd()

conn = sqlite.connect(appPath + '/data/yelpCleanDB.sqlite')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS CleanBusinessData;
DROP TABLE IF EXISTS DistanceAllBusinesses;
DROP TABLE IF EXISTS DistanceSelectedBusinesses;
DROP TABLE IF EXISTS DataDistanceAdded;
DROP TABLE IF EXISTS CompetitionZipcode;
DROP TABLE IF EXISTS DataCompetitionZipcodeAdded;
DROP TABLE IF EXISTS CompetitionCity;
DROP TABLE IF EXISTS DataCompetitionCityAdded;


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
  query_price INTEGER,
  region TEXT
);

CREATE TABLE DistanceAllBusinesses (
  id TEXT,
  rating INTEGER,
  price TEXT,
  distance INTEGER
);

CREATE TABLE DistanceSelectedBusinesses (
  id TEXT,
  closest2Distance INTEGER,
  closest2Price INTEGER,
  closest2Rating INTEGER,
  closest5Distance INTEGER,
  closest5Price INTEGER,
  closest5Rating INTEGER,
  closest10Distance INTEGER,
  closest10Price INTEGER,
  closest10Rating INTEGER,
  closest15Distance INTEGER,
  closest15Price INTEGER,
  closest15Rating INTEGER
);

CREATE TABLE CompetitionZipcode (
  zipcode TEXT,
  numberOfCompetitorsZipcode INTEGER,
  avgPriceZipcode INTEGER,
  avgRatingZipcode INTEGER
);



CREATE TABLE CompetitionCity (
  city TEXT,
  numberOfCompetitorsCity INTEGER,
  avgPriceCity INTEGER,
  avgRatingCity INTEGER
);


''')

conn.commit()
conn.close()

# cleanData.writeFinalDataToDB()
