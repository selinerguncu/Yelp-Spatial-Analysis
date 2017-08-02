This research investigates the effect of spatial competition on the price-quality relationship in seven business categories using a comprehensive data set from Yelp.com.

You can find the details (e.g., data and model specifics, conceptualization, findings) [here](http://yelpproject.selinerguncu.com/).

## Installation

To run this program you will need `python` and `pip` already installed. Also, you need to install web.py and Python requests library, and create an empty sqlite database.


```bash
$ export YELP_CLIENT_ID=<your-yelp-client-id>
$ export YELP_CLIENT_SECRET=<your-yelp-client-secret>
$ pip install flask
$ pip install geopy
$ pip install requests
$ pip install timestring
$ pip3 install pyshp
$ pip install gmaps
$ pip install gmplot
$ pip3 install folium
$ pip3.6 install beautifulsoup4
$ pip install -U selenium
$ mkdir ***
$ python bin/***.py
$ python bin/***.py
```
This program can run on Python 2.x or 3.x. Your imports should change depending on the version.

For Python 3.0 and later:
```python
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
```

For Python 2.x:
```python
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode
```

After you've done this, your program should be running on localhost:8080.

##### Yelp Data Visualization

Data consists of businesses, in seven different categories, located in Bay Area. Plese see the maps [here](http://yelpproject.selinerguncu.com/) that are created based on this data.


##### Yelp Data Analysis and Simulation

You can simulate market entries using [this interface](http://yelpproject.selinerguncu.com/). Your results will be based on the findings of this research.

## License
MIT
