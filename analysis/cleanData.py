import pandas as pd
import sqlite3 as sqlite
import os
from collections import defaultdict # to handle missing values while writing to the DB


# class cleanData():
def importRawData():
  conn = sqlite.connect('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpdb.sqlite')
  conn.text_factory = str
  cur = conn.cursor()

  cur.execute('''SELECT city, zip_code, price, rating, review_count, latitude, longitude,
    query_latitude, query_longitude, query_category, query_price, id FROM Business''')
  rawData = cur.fetchall()

  rawDataDict = []
  for row in rawData:
    tempDict = {}
    tempDict['city'] = row[0]
    tempDict['zipcode'] = row[1]
    tempDict['price'] = row[2]
    tempDict['rating'] = row[3]
    tempDict['review_count'] = row[4]
    tempDict['latitude'] = row[5]
    tempDict['longitude'] = row[6]
    tempDict['query_latitude'] = row[7]
    tempDict['query_longitude'] = row[8]
    tempDict['query_category'] = row[9]
    tempDict['query_price'] = row[10]
    tempDict['id'] = row[11]
    rawDataDict.append(tempDict)

  return rawDataDict

def cleanCityNames(rawDataDict):
  # print(listOfCityTuples)
  dictOfCities = {'Bay Area': 'Castro Valley',
                  'Bay Area San Francisco': 'San Francisco',
                  'Belvedere Tiburon': 'Belvedere',
                  'Berkeley Ca': 'Berkeley',
                  'CA': 'Corte Madera',
                  'Emerald Hills': 'Redwood City',
                  'Emerald  Hills' : 'Redwood City',
                  'Golden Gate Park': 'San Francisco',
                  'Marin County': 'Marin City',
                  'Haywood': 'Hayward',
                  'Marin': 'Marin City',
                  'Menlo  Park': 'Menlo Park',
                  'Oakland Ca': 'Oakland',
                  'Mountain view': 'Mountain View',
                  'Mountain  View': 'Mountain View',
                  'North Oakland': 'Oakland',
                  'North Richmond': 'Richmond',
                  'Pillar Point Harbor': 'El Granada',
                  'Pleasant hill': 'Pleasant Hill',
                  'Portalo  Valley': 'Portola Valley',
                  'Point Richmond': 'Richmond',
                  'Princeton By the Sea': 'Half Moon Bay',
                  'Rockridge': 'Oakland',
                  'Redwood': 'Redwood City',
                  'Redwood Shores': 'Redwood City',
                  'S  San Francisco': 'South San Francisco',
                  'S. San Francisco': 'South San Francisco',
                  'So San Francisco': 'South San Francisco',
                  'South  San Francisco': 'South San Francisco',
                  'South SF': 'South San Francisco',
                  'San  Francisco': 'San Francisco',
                  'San  Mateo': 'San Mateo',
                  'San Francisc': 'San Francisco',
                  'San Francisco Bay Area': 'San Francisco',
                  'San Francisco,': 'San Francisco',
                  'San Francsico': 'San Francisco',
                  'San Fransico': 'San Francisco',
                  'San Fransisco': 'San Francisco',
                  'San Leandro California': 'San Leandro',
                  'San  Leandro': 'San Leandro',
                  'San  Carlos': 'San Carlos',
                  'Stanford': 'Palo Alto',
                  'Ladera': 'Portalo Valley',
                  'Stinson Beach': 'Marin City',
                  'West Sacramento': 'Sacramento',
                  'emeryville': 'Emeryville',
                  'fremont': 'Fremont'}

  cleanData = []
  for business in rawDataDict:
    if business['city'] in dictOfCities.keys():
      for wrongCity, correctCity in dictOfCities.items():
        if business['city'] == wrongCity:
          # print(correctCity)
          business['city'] = correctCity
          cleanData.append(business)
    else:
      # change city with city and zipcode
      if business['city'] == 'Mountain House':
        pass
      elif business['city'] == 'Peninsula':
        if business['zipcode'] == '94062':
          business['city'] == 'Redwood City'
          cleanData.append(business)
        elif business['zipcode'] == '94070':
          business['city'] == 'San Carlos'
          cleanData.append(business)
      cleanData.append(business)
    #remove cities
    # if business['city'] == 'Mountain House':
    #   del

  return cleanData

# def removeCities(lisOfCityTuples):
#   for cityTuples in lisOfCityTuples:
#     if cityTuples[0] == 'Mountain House':
#       lisOfCityTuples.remove(('Mountain House', '95391'))
#   return lisOfCityTuples

# San Francisco -- 2 tane ayni
# Menlo Park iki tane ayni

def addNeigbirhoodSF(cleanData):
  neighborhoodsInSF = [{'zipcode': '94102', 'neighborhood': 'Hayes Valley/Tenderloin/North of Market', 'population': 28991},
                      {'zipcode': '94103', 'neighborhood': 'South of Market', 'population': 23016},
                      {'zipcode': '94107', 'neighborhood': 'Potrero Hill ', 'population': 17368},
                      {'zipcode': '94108', 'neighborhood': 'Chinatown', 'population': 13716},
                      {'zipcode': '94109', 'neighborhood': 'Polk/Russian Hill (Nob Hill) ', 'population': 56322},
                      {'zipcode': '94110', 'neighborhood': 'Inner Mission/Bernal Heights ', 'population': 74633},
                      {'zipcode': '94112', 'neighborhood': 'Ingelside-Excelsior/Crocker-Amazon ', 'population': 73104},
                      {'zipcode': '94114', 'neighborhood': 'Castro/Noe Valley', 'population': 30574},
                      {'zipcode': '94115', 'neighborhood': 'Western Addition/Japantown ', 'population': 33115},
                      {'zipcode': '94116', 'neighborhood': 'Parkside/Forest Hill ', 'population': 42958},
                      {'zipcode': '94117', 'neighborhood': 'Haight-Ashbury ', 'population': 38738},
                      {'zipcode': '94118', 'neighborhood': 'Inner Richmond ', 'population': 38939},
                      {'zipcode': '94121', 'neighborhood': 'Outer Richmond ', 'population': 42473},
                      {'zipcode': '94122', 'neighborhood': 'Sunset ', 'population': 55492},
                      {'zipcode': '94123', 'neighborhood': 'Marina ', 'population': 22903},
                      {'zipcode': '94124', 'neighborhood': 'Bayview-Hunters Point', 'population': 33170},
                      {'zipcode': '94127', 'neighborhood': 'St. Francis Wood/Miraloma/West Portal', 'population': 20624},
                      {'zipcode': '94131', 'neighborhood': 'Twin Peaks-Glen Park ', 'population': 27897},
                      {'zipcode': '94132', 'neighborhood': 'Lake Merced', 'population': 26291},
                      {'zipcode': '94133', 'neighborhood': 'North Beach/Chinatown', 'population': 26827},
                      {'zipcode': '94134', 'neighborhood': 'Visitacion Valley/Sunnydale', 'population': 40134}]
  for row in cleanData:
    for neighborhood in neighborhoodsInSF:
      if row['zipcode'] == neighborhood['zipcode']:
        row['neighborhood'] = neighborhood['neighborhood']
      # else:
      #   print('no neighborhood info for', neighborhood)
  return cleanData

def addCensusData(cleanData):
  citiesInCounties = [{'city': 'Alameda', 'typ': 'City', 'county': 'Alameda', 'population': 73812, 'land area km3': 27.5},
                      {'city': 'Albany', 'typ': 'City', 'county': 'Alameda', 'population': 18539, 'land area km3': 4.6},
                      {'city': 'Berkeley', 'typ': 'City', 'county': 'Alameda', 'population': 112580, 'land area km3': 27.1},
                      {'city': 'Dublin', 'typ': 'City', 'county': 'Alameda', 'population': 46036, 'land area km3': 38.6},
                      {'city': 'Emeryville', 'typ': 'City', 'county': 'Alameda', 'population': 10080, 'land area km3': 3.2},
                      {'city': 'Fremont', 'typ': 'City', 'county': 'Alameda', 'population': 214089, 'land area km3': 200.6},
                      {'city': 'Hayward', 'typ': 'City', 'county': 'Alameda', 'population': 144186, 'land area km3': 117.4},
                      {'city': 'Livermore', 'typ': 'City', 'county': 'Alameda', 'population': 80968, 'land area km3': 65.2},
                      {'city': 'Newark', 'typ': 'City', 'county': 'Alameda', 'population': 42573, 'land area km3': 35.9},
                      {'city': 'Oakland', 'typ': 'City', 'county': 'Alameda', 'population': 390724, 'land area km3': 144.5},
                      {'city': 'Piedmont', 'typ': 'City', 'county': 'Alameda', 'population': 10667, 'land area km3': 4.4},
                      {'city': 'Pleasanton', 'typ': 'City', 'county': 'Alameda', 'population': 70285, 'land area km3': 62.4},
                      {'city': 'San Leandro', 'typ': 'City', 'county': 'Alameda', 'population': 84950, 'land area km3': 34.6},
                      {'city': 'Union City', 'typ': 'City', 'county': 'Alameda', 'population': 69516, 'land area km3': 50.4},
                      {'city': 'Antioch', 'typ': 'City', 'county': 'Contra Costa', 'population': 102372, 'land area km3': 73.4},
                      {'city': 'Brentwood', 'typ': 'City', 'county': 'Contra Costa', 'population': 51481, 'land area km3': 38.3},
                      {'city': 'Clayton', 'typ': 'City', 'county': 'Contra Costa', 'population': 10897, 'land area km3': 9.9},
                      {'city': 'Concord', 'typ': 'City', 'county': 'Contra Costa', 'population': 122067, 'land area km3': 79.1},
                      {'city': 'Danville', 'typ': 'Town', 'county': 'Contra Costa', 'population': 42039, 'land area km3': 46.7},
                      {'city': 'El Cerrito', 'typ': 'City', 'county': 'Contra Costa', 'population': 23549, 'land area km3': 9.6},
                      {'city': 'Hercules', 'typ': 'City', 'county': 'Contra Costa', 'population': 24060, 'land area km3': 16.1},
                      {'city': 'Lafayette', 'typ': 'City', 'county': 'Contra Costa', 'population': 23893, 'land area km3': 39.4},
                      {'city': 'Martinez', 'typ': 'City', 'county': 'Contra Costa', 'population': 35824, 'land area km3': 31.4},
                      {'city': 'Moraga', 'typ': 'Town', 'county': 'Contra Costa', 'population': 16016, 'land area km3': 24.4},
                      {'city': 'Oakley', 'typ': 'City', 'county': 'Contra Costa', 'population': 35432, 'land area km3': 41.1},
                      {'city': 'Orinda', 'typ': 'City', 'county': 'Contra Costa', 'population': 17643, 'land area km3': 32.8},
                      {'city': 'Pinole', 'typ': 'City', 'county': 'Contra Costa', 'population': 18390, 'land area km3': 13.8},
                      {'city': 'Pittsburg', 'typ': 'City', 'county': 'Contra Costa', 'population': 63264, 'land area km3': 44.6},
                      {'city': 'Pleasant Hill', 'typ': 'City', 'county': 'Contra Costa', 'population': 33152, 'land area km3': 18.3},
                      {'city': 'Richmond', 'typ': 'City', 'county': 'Contra Costa', 'population': 103701, 'land area km3': 77.9},
                      {'city': 'San Pablo', 'typ': 'City', 'county': 'Contra Costa', 'population': 29139, 'land area km3': 6.8},
                      {'city': 'San Ramon', 'typ': 'City', 'county': 'Contra Costa', 'population': 72148, 'land area km3': 46.8},
                      {'city': 'Walnut Creek', 'typ': 'City', 'county': 'Contra Costa', 'population': 64173, 'land area km3': 51.2},
                      {'city': 'Belvedere', 'typ': 'City', 'county': 'Marin', 'population': 2068, 'land area km3': 1.3},
                      {'city': 'Corte Madera', 'typ': 'Town', 'county': 'Marin', 'population': 9253, 'land area km3': 8.2},
                      {'city': 'Fairfax', 'typ': 'Town', 'county': 'Marin', 'population': 7441, 'land area km3': 5.7},
                      {'city': 'Larkspur', 'typ': 'City', 'county': 'Marin', 'population': 11926, 'land area km3': 7.8},
                      {'city': 'Mill Valley', 'typ': 'City', 'county': 'Marin', 'population': 13903, 'land area km3': 12.3},
                      {'city': 'Novato', 'typ': 'City', 'county': 'Marin', 'population': 51904, 'land area km3': 71.1},
                      {'city': 'Ross', 'typ': 'Town', 'county': 'Marin', 'population': 2415, 'land area km3': 4},
                      {'city': 'San Anselmo', 'typ': 'Town', 'county': 'Marin', 'population': 12336, 'land area km3': 6.9},
                      {'city': 'San Rafael', 'typ': 'City', 'county': 'Marin', 'population': 57713, 'land area km3': 42.7},
                      {'city': 'Sausalito', 'typ': 'City', 'county': 'Marin', 'population': 7061, 'land area km3': 4.6},
                      {'city': 'Tiburon', 'typ': 'Town', 'county': 'Marin', 'population': 8962, 'land area km3': 11.5},
                      {'city': 'American Canyon', 'typ': 'City', 'county': 'Napa', 'population': 19454, 'land area km3': 12.5},
                      {'city': 'Calistoga', 'typ': 'City', 'county': 'Napa', 'population': 5155, 'land area km3': 6.7},
                      {'city': 'Napa', 'typ': 'City', 'county': 'Napa', 'population': 76915, 'land area km3': 46.2},
                      {'city': 'St. Helena', 'typ': 'City', 'county': 'Napa', 'population': 5814, 'land area km3': 12.9},
                      {'city': 'Yountville', 'typ': 'Town', 'county': 'Napa', 'population': 2933, 'land area km3': 4},
                      {'city': 'San Francisco', 'typ': 'City and county', 'county': 'San Francisco', 'population': 805235, 'land area km3': 121.4},
                      {'city': 'Atherton', 'typ': 'Town', 'county': 'San Mateo', 'population': 6914, 'land area km3': 13},
                      {'city': 'Belmont', 'typ': 'City', 'county': 'San Mateo', 'population': 25835, 'land area km3': 12},
                      {'city': 'Brisbane', 'typ': 'City', 'county': 'San Mateo', 'population': 4282, 'land area km3': 8},
                      {'city': 'Burlingame', 'typ': 'City', 'county': 'San Mateo', 'population': 28806, 'land area km3': 11.4},
                      {'city': 'Colma', 'typ': 'Town', 'county': 'San Mateo', 'population': 1792, 'land area km3': 4.9},
                      {'city': 'Daly City', 'typ': 'City', 'county': 'San Mateo', 'population': 101123, 'land area km3': 19.8},
                      {'city': 'East Palo Alto', 'typ': 'City', 'county': 'San Mateo', 'population': 28155, 'land area km3': 6.5},
                      {'city': 'Foster City', 'typ': 'City', 'county': 'San Mateo', 'population': 30567, 'land area km3': 9.7},
                      {'city': 'Half Moon Bay', 'typ': 'City', 'county': 'San Mateo', 'population': 11324, 'land area km3': 16.6},
                      {'city': 'Hillsborough', 'typ': 'Town', 'county': 'San Mateo', 'population': 10825, 'land area km3': 16},
                      {'city': 'Menlo Park', 'typ': 'City', 'county': 'San Mateo', 'population': 32026, 'land area km3': 25.4},
                      {'city': 'Millbrae', 'typ': 'City', 'county': 'San Mateo', 'population': 21532, 'land area km3': 8.4},
                      {'city': 'Pacifica', 'typ': 'City', 'county': 'San Mateo', 'population': 37234, 'land area km3': 32.8},
                      {'city': 'Portola Valley', 'typ': 'Town', 'county': 'San Mateo', 'population': 4353, 'land area km3': 23.5},
                      {'city': 'Redwood City', 'typ': 'City', 'county': 'San Mateo', 'population': 76815, 'land area km3': 50.3},
                      {'city': 'San Bruno', 'typ': 'City', 'county': 'San Mateo', 'population': 41114, 'land area km3': 14.2},
                      {'city': 'San Carlos', 'typ': 'City', 'county': 'San Mateo', 'population': 28406, 'land area km3': 14.3},
                      {'city': 'San Mateo', 'typ': 'City', 'county': 'San Mateo', 'population': 97207, 'land area km3': 31.4},
                      {'city': 'South San Francisco', 'typ': 'City', 'county': 'San Mateo', 'population': 63632, 'land area km3': 23.7},
                      {'city': 'Woodside', 'typ': 'Town', 'county': 'San Mateo', 'population': 5287, 'land area km3': 30.4},
                      {'city': 'Campbell', 'typ': 'City', 'county': 'Santa Clara', 'population': 39349, 'land area km3': 15},
                      {'city': 'Cupertino', 'typ': 'City', 'county': 'Santa Clara', 'population': 58302, 'land area km3': 29.2},
                      {'city': 'Gilroy', 'typ': 'City', 'county': 'Santa Clara', 'population': 48821, 'land area km3': 41.8},
                      {'city': 'Los Altos', 'typ': 'City', 'county': 'Santa Clara', 'population': 28976, 'land area km3': 16.8},
                      {'city': 'Los Altos Hills', 'typ': 'Town', 'county': 'Santa Clara', 'population': 7922, 'land area km3': 22.8},
                      {'city': 'Los Gatos', 'typ': 'Town', 'county': 'Santa Clara', 'population': 29413, 'land area km3': 28.7},
                      {'city': 'Milpitas', 'typ': 'City', 'county': 'Santa Clara', 'population': 66790, 'land area km3': 35.2},
                      {'city': 'Monte Sereno', 'typ': 'City', 'county': 'Santa Clara', 'population': 3341, 'land area km3': 4.2},
                      {'city': 'Morgan Hill', 'typ': 'City', 'county': 'Santa Clara', 'population': 37882, 'land area km3': 33.4},
                      {'city': 'Mountain View', 'typ': 'City', 'county': 'Santa Clara', 'population': 74066, 'land area km3': 31.1},
                      {'city': 'Palo Alto', 'typ': 'City', 'county': 'Santa Clara', 'population': 64403, 'land area km3': 61.8},
                      {'city': 'San Jose', 'typ': 'City', 'county': 'Santa Clara', 'population': 945942, 'land area km3': 457.2},
                      {'city': 'Santa Clara', 'typ': 'City', 'county': 'Santa Clara', 'population': 116468, 'land area km3': 47.7},
                      {'city': 'Saratoga', 'typ': 'City', 'county': 'Santa Clara', 'population': 29926, 'land area km3': 32.1},
                      {'city': 'Sunnyvale', 'typ': 'City', 'county': 'Santa Clara', 'population': 140081, 'land area km3': 57},
                      {'city': 'Benicia', 'typ': 'City', 'county': 'Solano', 'population': 26997, 'land area km3': 33.5},
                      {'city': 'Dixon', 'typ': 'City', 'county': 'Solano', 'population': 18351, 'land area km3': 18.1},
                      {'city': 'Fairfield', 'typ': 'City', 'county': 'Solano', 'population': 105321, 'land area km3': 96.8},
                      {'city': 'Rio Vista', 'typ': 'City', 'county': 'Solano', 'population': 7360, 'land area km3': 17.3},
                      {'city': 'Suisun City', 'typ': 'City', 'county': 'Solano', 'population': 28111, 'land area km3': 10.6},
                      {'city': 'Vacaville', 'typ': 'City', 'county': 'Solano', 'population': 92428, 'land area km3': 73.5},
                      {'city': 'Vallejo', 'typ': 'City', 'county': 'Solano', 'population': 115942, 'land area km3': 79.4},
                      {'city': 'Cloverdale', 'typ': 'City', 'county': 'Sonoma', 'population': 8618, 'land area km3': 6.9},
                      {'city': 'Cotati', 'typ': 'City', 'county': 'Sonoma', 'population': 7265, 'land area km3': 4.9},
                      {'city': 'Healdsburg', 'typ': 'City', 'county': 'Sonoma', 'population': 11254, 'land area km3': 11.6},
                      {'city': 'Petaluma', 'typ': 'City', 'county': 'Sonoma', 'population': 57941, 'land area km3': 37.2},
                      {'city': 'Rohnert Park', 'typ': 'City', 'county': 'Sonoma', 'population': 40971, 'land area km3': 18.1},
                      {'city': 'Santa Rosa', 'typ': 'City', 'county': 'Sonoma', 'population': 167815, 'land area km3': 106.9},
                      {'city': 'Sebastopol', 'typ': 'City', 'county': 'Sonoma', 'population': 7379, 'land area km3': 4.8},
                      {'city': 'Sonoma', 'typ': 'City', 'county': 'Sonoma', 'population': 10648, 'land area km3': 7.1},
                      {'city': 'Windsor', 'typ': 'Town', 'county': 'Sonoma', 'population': 26801, 'land area km3': 18.8}]
  for row in cleanData:
    for city in citiesInCounties:
      if row['city'] == city['city']:
        row['county'] = city['county']
        row['population'] = city['population']
        row['area'] = city['land area km3']
      # else:
      #   print('no county info for', city)
  return cleanData


#SF de neighborhood olmayan zipler:
#[94192', '94199', '94130', '94016', '94015', '94014', '94013', '94012', '94010', '94704',
#'95014', '94154', '94070', '94030', '94111', '94619', '94158', '90012', '94080', '94002',
#'94129', '94128', '94607', '94141', '94140', '94143', '94142', '94101', '94100', '94105',
#'94104', '94609', '94597', '94113', '94017']]

def correctCityZipcodes(cleanData):
  for row in cleanData:
    if row['zipcode'] in ['94016', '94015', '94014', '94017']:
      row['city'] = 'Daly City'
    elif row['zipcode'] in ['94013', '94010']:
      row['city'] = 'Burlingame'
    elif row['zipcode'] in ['94704']:
      row['city'] = 'Berkeley'
    elif row['zipcode'] in ['95014']:
      row['city'] = 'Cupertino'
    elif row['zipcode'] in ['94070']:
      row['city'] = 'San Carlos'
    elif row['zipcode'] in ['94030']:
      row['city'] = 'Millbrae'
    elif row['zipcode'] in ['94619', '94607', '94609']:
      row['city'] = 'Oakland'
    elif row['zipcode'] in ['94080']:
      row['city'] = 'South San Francisco'
    elif row['zipcode'] in ['94002']:
      row['city'] = 'Belmont'
    elif row['zipcode'] in ['94597']:
      row['city'] = 'Walnut Creek'
    # elif row['zipcode'] in ['90012']:
    #   del row
  return cleanData


# 94192, 94130, 94199, 94012, 94154, 94111, 94158, 94129, 94128, 94141, 94140, 94143, 94142, 94101, 94100, 94105, 94104, 94113 -- SF


# 94192, 94154, 94199, 94141, 94140, 94143, 94142, 94101, 94113, 94111, 94105, 94104, 94158, 94130, 94012, 94100, 90012, 94129, 94128'])

# 90012 -- LA

def addDowntownOuterSF(finalData):
  for row in finalData:
    if row['city'] == 'San Francisco':
      if row['zipcode'] in ['94109','94102','94103','94107','94158','94108','94105','94111','94133']:
        finalData.append({'city': 'San Francisco - Downtown',
                          'zipcode': row['zipcode'],
                          'price': row['price'],
                          'rating': row['rating'],
                          'review_count': row['review_count'],
                          'latitude': row['latitude'],
                          'longitude': row['longitude'],
                          'query_latitude': row['query_latitude'],
                          'query_longitude': row['query_longitude'],
                          'query_category': row['query_category'],
                          'query_price': row['query_price'],
                          'county': row['county'],
                          'population': row['population'],
                          'area': row['area']})
      else:
        finalData.append({'city': 'San Francisco - Outer',
                          'zipcode': row['zipcode'],
                          'price': row['price'],
                          'rating': row['rating'],
                          'review_count': row['review_count'],
                          'latitude': row['latitude'],
                          'longitude': row['longitude'],
                          'query_latitude': row['query_latitude'],
                          'query_longitude': row['query_longitude'],
                          'query_category': row['query_category'],
                          'query_price': row['query_price'],
                          'county': row['county'],
                          'population': row['population'],
                          'area': row['area']})
  return finalData


def addRegion(cleanData):
  eastBay = ['Alameda','Albany','Antioch','Benicia','Berkeley','Brentwood','Castro Valley','Concord','Danville','Davis',
              'Dixon','Dublin','El Cerrito','El Sobrante','Elk Grove','Emeryville','Esparto','Fairfield','Grass Valley',
              'Guinda','Hayward','Kensington','Lafayette','Livermore','Martinez','Moraga','Mountain House','Newark',
              'Oakland','Orinda','Piedmont','Pinole','Pleasant Hill','Pleasanton','Richmond','Roseville','Sacramento',
              'San Leandro','San Lorenzo','San Ramon','Sunol','Tracy','Union City','Walnut Creek']



  northBay = ['Albion','Belvedere','Bolinas','Corte Madera','Greenbrae','Healdsburg','Marin City','Mill Valley',
              'Muir Beach','Napa','Petaluma','San Anselmo','San Rafael','Santa Rosa','Sausalito','Sonoma',
              'Stinson Beach','Tiburon']



  peninsula = ['Aptos','Atherton','Belmont','Brisbane','Burlingame','Campbell','Colma','Cupertino','Daly City',
               'East Palo Alto','El Granada','Emerald Hills','Foster City','Fremont','Half Moon Bay','Hillsborough','La Honda',
               'Los Altos','Los Gatos','Menlo Park','Millbrae','Montara','Monterey','Morgan Hill','Moss Beach',
               'Mountain View','Pacifica','Palo Alto','Pescadero','Pillar Point Harbor','Portola Valley','Redwood City','San Bruno',
               'San Carlos','San Francisco','San Gregorio','San Jose','San Mateo','Santa Clara','Santa Cruz',
               'Saratoga','South San Francisco','Stanford','Sunnyvale','Watsonville','Woodside',
               'San Francisco - Downtown', 'San Francisco - Outer', 'Peninsula']

  deleteCities = ['Carson', 'Moss Landing', 'Redding', 'San Diego']

  noRegion = []
  for row in cleanData:
    if row['city'] in eastBay:
      row['region'] = 'eastBay'
    elif row['city'] in northBay:
      row['region'] = 'northBay'
    elif row['city'] in peninsula:
      row['region'] = 'peninsula'
    elif row['city'] in deleteCities:
      cleanData.remove(row)
    else:
      cleanData.remove(row)
      # noRegion.append(row)
  return cleanData


def writeFinalDataToDB():
  rawData = importRawData()
  dataCorrectedCities = cleanCityNames(rawData)
  dataCorrectedCityZipcode = correctCityZipcodes(dataCorrectedCities)
  dataAddedCensusData = addCensusData(dataCorrectedCityZipcode)
  dataRegionsAddedToSF = addDowntownOuterSF(dataAddedCensusData)
  finalData = addRegion(dataRegionsAddedToSF)

  conn = sqlite.connect('/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpCleanDB.sqlite')
  conn.text_factory = str
  cur = conn.cursor()

  for row in finalData:
    row = defaultdict(lambda: None, row)
    cur.execute('''INSERT INTO CleanBusinessData(id, rating, price, county, query_latitude, query_longitude,
      population, city, review_count, area, zipcode, longitude, query_category, latitude, query_price, region)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (row['id'],row['rating'],row['price'],row['county'],row['query_latitude'],row['query_longitude'],
        row['population'],row['city'],row['review_count'],row['area'],row['zipcode'],
        row['longitude'],row['query_category'],row['latitude'],row['query_price'],row['region']))

  conn.commit()

# writeFinalDataToDB()


# (             'Alameda' - east
#               'Albany' - east
#               'Albion' -up
#               'Antioch' - e
#               'Aptos' - down
#               'Atherton' - Peninsula
#               'Belmont' - Peninsula
#               'Belvedere' - up
#               'Benicia' - up east silebilirsin
#               'Berkeley' - east
#               'Bolinas' - up
#               'Brentwood' - east
#               'Brisbane' - Peninsula
#               'Burlingame' - Peninsula
#               'Campbell' - Peninsula down
#               'Carson' --- sil LA
#               'Castro Valley' - east
#               'Colma' - Peninsula
#               'Concord' - east
#               'Corte Madera' - up
#               'Cupertino' - Peninsula
#               'Daly City' - Peninsula
#               'Danville' -east
#               'Davis' - very up east
#               'Dixon'- very up east
#               'Dublin' -east
#               'East Palo Alto' - Peninsula
#               'El Cerrito' - up east
#               'El Granada' - Peninsula
#               'El Sobrante' - up east
#               'Elk Grove'- very up east
#               'Emerald Hills' - Peninsula
#               'Emeryville' - east
#               'Esparto'- very up east
#               'Fairfield' - up east
#               'Foster City' - Peninsula
#               'Fremont'- Peninsula
#               'Grass Valley'- very up east
#               'Greenbrae' - up
#               'Guinda' - very very up east sil
#               'Half Moon Bay'- Peninsula
#               'Hayward'- east
#               'Healdsburg' -- very very up
#               'Hillsborough' - Peninsula
#               'Kensington' - up east
#               'La Honda'- Peninsula
#               'Lafayette'- east
#               'Livermore' - east
#               'Los Altos'- Peninsula
#               'Los Gatos'- Peninsula
#               'Marin City' - up
#               'Martinez' - east
#               'Menlo Park' - Peninsula
#               'Mill Valley' - up
#               'Millbrae' - Peninsula
#               'Montara' - Peninsula
#               'Monterey' - Peninsula
#               'Moraga'- east
#               'Morgan Hill' - Peninsula down
#               'Moss Beach' - Peninsula
#               'Moss Landing' - very down sil
#               'Mountain House' - east
#               'Mountain View'- Peninsula
#               'Muir Beach' Marin County,
#               'Napa' - up east
#               'Newark' - east
#               'Oakland'- east
#               'Orinda'- east
#               'Pacifica' - Peninsula
#               'Palo Alto'- Peninsula
#               'Pescadero' Peninsula
#               'Petaluma' North Bay
#               'Piedmont'- east
#               'Pillar Point Harbor' - Peninsula
#               'Pinole' - east
#               'Pleasant Hill'- east
#               'Pleasanton' - east
#               'Portola Valley' - Peninsula
#               'Redding' --- sil
#               'Redwood City'- Peninsula
#               'Richmond' - east
#               'Roseville' - up east
#               'Sacramento' - up east
#               'San Anselmo' - up
#               'San Bruno' - Peninsula
#               'San Carlos' - Peninsula
#               'San Diego' -- sil
#               'San Francisco'- Peninsula
#               'San Gregorio' - Peninsula
#               'San Jose'- Peninsula
#               'San Leandro' - east
#               'San Lorenzo' - east
#               'San Mateo'- Peninsula
#               'San Rafael' - up
#               'San Ramon' - east
#               'Santa Clara' - Peninsula
#               'Santa Cruz' - Peninsula
#               'Santa Rosa' - very up
#               'Saratoga' - Peninsula
#               'Sausalito' - up
#               'Sonoma' - very up
#               'South San Francisco'- Peninsula
#               'Stanford'- Peninsula
#               'Stinson Beach' --up
#               'Sunnyvale'- Peninsula
#               'Sunol' - east
#               'Tiburon' -- up
#               'Tracy' - east
#               'Union City' - east
#               'Walnut Creek'- east
#               'Watsonville' - Peninsula down
#               'Woodside'- Peninsula
