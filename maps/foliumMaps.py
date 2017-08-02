import folium
from folium import plugins
import numpy as np

import sqlite3 as sqlite
import os
import sys

import pandas as pd

#extract data from yelp DB and clean it:
DB_PATH = "/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpdb.sqlite"

conn = sqlite.connect(DB_PATH)



#######################################
############ organize data ############
#######################################
def organizeData(mapParameters):
  business = str(mapParameters['business'])
  city = str(mapParameters['city'])
  price = str(mapParameters['price'])
  rating = float(mapParameters['rating'])

  if 'zipcode' in mapParameters.keys():
    zipcode = str(mapParameters['zipcode'])
    sql = "SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zip_code, price, rating, review_count FROM Business WHERE query_category = '%s' AND city = '%s' AND zip_code = '%s' AND price = '%s' AND rating = '%r'" % (business, city, zipcode, price, rating)
    coordinates = pd.read_sql_query(sql, conn)
  else:
    sql = "SELECT longitude, latitude, query_latitude, query_latitude, query_category, query_price, city, zip_code, price, rating, review_count FROM Business WHERE query_category = '%s' AND city = '%s' AND price = '%s' AND rating = '%r'" % (business, city, price, rating)
    coordinates = pd.read_sql_query(sql, conn)
    print('here')


  if len(coordinates) <= 1860:
    for i in range(len(coordinates)):
        if coordinates["longitude"][i] == None:
            coordinates["longitude"][i] = coordinates["query_longitude"][i]
        if coordinates["latitude"][i] == None:
            coordinates["latitude"][i] = coordinates["query_latitude"][i]

  #   coordinates = []

  #   for i in range(len(coords)): #max ~1860 coordinates
  #       coordinate = []
  #       coordinate.append(coords["latitude"][i])
  #       coordinate.append(coords["longitude"][i])
  #       coordinates.append(coordinate)

  #   # convert list of lists to list of tuples
  #   coordinates = [tuple([i[0],i[1]]) for i in coordinates]
  #   # print(coordinates[0:10])
    return coordinates
  # else:
  #   print("Too many data points; cannot be mapped!")

#######################################
##### visualize the coordinates #######
#######################################
def makeMarkerMap(coordinates):
  # # get center of map
  # meanlat = np.mean([float(i[0]) for i in coordinates])
  # meanlon = np.mean([float(i[1]) for i in coordinates])

  meanlat = np.mean(coordinates['latitude'])
  meanlon = np.mean(coordinates['longitude'])


  #Initialize map
  mapa = folium.Map(location=[meanlat, meanlon],
                    tiles='OpenStreetMap', zoom_start=11)
  # add markers
  for i in range(len(coordinates)):
      # create popup on click
      html="""
      Rating: {}<br>
      Popularity: {}<br>
      Price: {}<br>
      """
      html = html.format(coordinates["rating"][i],\
                 coordinates["review_count"][i],\
                 coordinates["price"][i])
      iframe = folium.IFrame(html=html, width=100, height=10) #element yok
      popup = folium.Popup(iframe, max_width=2650)

      #  add marker to map
      folium.Marker(tuple([coordinates['latitude'],coordinates['longitude']]), popup=None,).add_to(mapa)

  return mapa.save("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/foliumMarkers.html")

#######################################
####### cluster nearby points #########
#######################################
def makeClusterMap(coordinates):
  from folium.plugins import MarkerCluster # for marker clusters
  meanlat = np.mean(coordinates['latitude'])
  meanlon = np.mean(coordinates['longitude'])
  # initialize map
  mapa = folium.Map(location=[meanlat, meanlon],
                    tiles='Cartodb Positron', zoom_start=13)

  # add marker clusters
  mapa.add_child(MarkerCluster(locations=coordinates, popups=coordinates))

  return mapa.save("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/foliumCluster.html")

  #######################################
  ####### generate a heat map ###########
  #######################################
def makeHeatmapMap(coordinates):
  from folium.plugins import HeatMap
  meanlat = np.mean(coordinates['latitude'])
  meanlon = np.mean(coordinates['longitude'])
  # initialize map
  mapa = folium.Map(location=[meanlat, meanlon],
                    tiles='OpenStreetMap', zoom_start=13)

  # add heat
  mapa.add_child(HeatMap(coordinates))

  return mapa.save("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/yelp/static/foliumHeatmap.html")


# saving the map as an image doesnt seem to work
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# # for different tiles: https://github.com/python-visualization/folium
# delay=5
# fn='foliumHeatmap.html'
# tmpurl='file:///Users/selinerguncu/Desktop/PythonProjects/Fun%20Projects/Yelp%20Project/Simulation/foliumHeatmap.html'.format(path=os.getcwd(),mapfile=fn)
# mapa.save(fn)

# firefox_capabilities = DesiredCapabilities.FIREFOX
# firefox_capabilities['marionette'] = True

# browser = webdriver.Firefox(capabilities=firefox_capabilities, executable_path='/Users/selinerguncu/Downloads/geckodriver')
# browser.get(tmpurl)
# #Give the map tiles some time to load
# time.sleep(delay)
# browser.save_screenshot('mynewmap.png')
# browser.quit()
