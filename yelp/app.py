import os
import sqlite3 as sqlite
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from maps import foliumMaps, circleMap

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# APP_PATH = os.getcwd()

# conn = sqlite.connect(APP_PATH + '/data/yelpdb.sqlite')

# Load default config and override config from an environment variable

APP_PATH = os.getcwd()
print(APP_PATH)
DB_PATH = "/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpdb.sqlite"

app.config.update(dict(
  DATABASE=os.path.join(app.root_path, 'yelpdb'),
  SECRET_KEY='development key',
  USERNAME='admin',
  PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


#You can create a simple database connection through SQLite and then tell it to use the sqlite3.Row object to represent rows.
#This allows the rows to be treated as if they were dictionaries instead of tuples.

def connect_db():
  """Connects to the specific database."""
  # rv = sqlite.connect(app.config['DATABASE'])
  conn = sqlite.connect(DB_PATH)
  conn.row_factory = sqlite.Row
  cur = conn.cursor()
  return cur


# def get_db():
#   """Opens a new database connection if there is none yet for the
#   current application context.
#   """
#   if not hasattr(g, 'sqlite_db'):
#     g.sqlite_db = connect_db()
#   return g.sqlite_db

# @app.teardown_appcontext
# def close_db(error):
#   """Closes the database again at the end of the request."""
#   if hasattr(g, 'sqlite_db'):
#     g.sqlite_db.close()


# def init_db():
#   db = get_db()
#   with app.open_resource('schema.sql', mode='r') as f:
#     db.cursor().executescript(f.read())
#   db.commit()

# @app.cli.command('initdb')
# def initdb_command():
#   """Initializes the database."""
#   init_db()
#   print('Initialized the database.')


#summary is the main template
@app.route('/')
def main():
  return redirect(url_for('intro'))

@app.route('/intro')
def intro():
  return render_template('/intro/summary.html')

@app.route('/intro/summary')
def introSummary():
  return render_template('/intro/summary.html')

@app.route('/intro/concept')
def introConcept():
  return render_template('/intro/concept.html')

@app.route('/intro/method')
def introMethod():
  return render_template('/intro/method.html')

@app.route('/intro/findings')
def introFindings():
  return render_template('/intro/findings.html')


@app.route('/maps', methods=['GET', 'POST'])
def maps():
    return redirect(url_for('mapsSetup'))
  # return render_template('/maps/setup.html', cities=sorted(cities), zipcodes=sorted(zipcodes), cityZipcodeDict=cityZipcodeDict)

@app.route('/maps/setup', methods=['GET', 'POST'])
def mapsSetup():
  if request.method == 'POST':
    print(request.form)
    return redirect(url_for('mapsAllmaps'))

  conn = sqlite.connect("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/yelpdb.sqlite")
  cur = conn.cursor()
  cur.execute('''SELECT city FROM Business''',)
  citiesTuples = cur.fetchall()
  cities = set(citiesTuples)

  cur.execute('''SELECT zip_code FROM Business''',)
  zipcodesTuples = cur.fetchall()
  zipcodes = set(zipcodesTuples)

  cur.execute('''SELECT city, zip_code FROM Business''',)
  cityZipcodeTuples = cur.fetchall()

  cityZipcodeTupleSets = set(cityZipcodeTuples)
  cityZipcodeDict={}
  for city,zip_code in cityZipcodeTupleSets:
      if not city in cityZipcodeDict.keys():
        cityZipcodeDict[city] = [zip_code]
      else:
        cityZipcodeDict[city].append(zip_code)
  return render_template('/maps/setup.html', cities=sorted(cities), zipcodes=sorted(zipcodes), cityZipcodeDict=cityZipcodeDict)

@app.route('/maps/allmaps', methods=['GET', 'POST'])
def mapsAllmaps():
  mapParameters = {'city' : request.form['city'],
                         'price' : request.form['price'],
                         'rating' : request.form['rating'] }

  if request.form["business"] == 'reastaurants':
    mapParameters['business'] = 'Reastaurants'
  elif request.form["business"] == 'coffee':
    mapParameters['business'] = 'Coffee'
  elif request.form["business"] == 'bars':
    mapParameters['business'] = 'Bars'
  elif request.form["business"] == 'giftshop':
    mapParameters['business'] = 'Giftshops'
  elif request.form["business"] == 'beautysvc':
    mapParameters['business'] = 'Beauty and Spas'
  elif request.form["business"] == 'nightlife':
    mapParameters['business'] = 'Nightlife'
  elif request.form["business"] == 'food':
    mapParameters['business'] = 'Food'

  if 'zipcode' in request.form.keys():
    mapParameters['zipcode'] = request.form['zipcode']

  print(mapParameters)
  coordinates = foliumMaps.organizeData(mapParameters)
  foliumMaps.makeMarkerMap(coordinates)
  foliumMaps.makeClusterMap(coordinates)
  foliumMaps.makeHeatmapMap(coordinates)
  circleMap.makeCircleMapRating(coordinates)
  circleMap.makeCircleMapPrice(coordinates)

  return render_template('/maps/allmaps.html', mapParameters=mapParameters)

@app.route('/simulation', methods=['GET', 'POST'])
def simulation():
  if request.method == 'POST':
    return redirect(url_for('simulationPlay'))
  else:
    return redirect(url_for('simulationIntro'))

@app.route('/simulation/intro')
def simulationIntro():
  return render_template('/simulation/intro.html')

@app.route('/simulation/play', methods=['GET', 'POST'])
def simulationPlay():
  return render_template('/simulation/play.html')

#rawdata is the main template
@app.route('/analysis')
def analysis():
  return render_template('/analysis/rawdata.html')

@app.route('/analysis/rawdata')
def analysisRawdata():
  return render_template('/analysis/rawdata.html')

@app.route('/analysis/outline')
def analysisOutline():
  return render_template('/analysis/outline.html')

@app.route('/analysis/estimation')
def analysisEstimation():
  return render_template('/analysis/estimation.html')

@app.route('/analysis/results')
def analysisResults():
  return render_template('/analysis/results.html')

@app.route('/analysis/technicalities')
def analysisTechnicalities():
  return render_template('/analysis/technicalities.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
  return render_template('/feedback/feedback.html')

@app.route('/feedbacksent', methods=['GET', 'POST'])
def feedbackSent():
  errorComment = None
  errorAbout = None
  print(request.form)
  if request.method == 'POST':
    if str(request.form["comment"]) == '':
      errorComment = 'So, what is your comment?'
      return render_template('/feedback/feedback.html' , errorComment=errorComment)
    elif not "about" in request.form.keys():
      if str(request.form["otherAbout"]) == '':
        errorAbout = 'What is your comment about?'
        return render_template('/feedback/feedback.html' , errorAbout=errorAbout)
    if request.form["about"] == 'other' and str(request.form["otherAbout"]) == '':
      errorAbout = 'What is your comment about?'
      return render_template('/feedback/feedback.html' , errorAbout=errorAbout)


  conn = sqlite.connect("/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/Yelp/data/feedbackdb.sqlite")
  cur = conn.cursor()
  cur.execute('''INSERT INTO Feedback (name, email, about, comment) VALUES (?, ?, ?, ?)''',
    (request.form['name'], request.form['email'], request.form['about'], request.form['comment']))
  conn.commit()
  return render_template('/feedback/feedbacksent.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('main'))
  return render_template('login.html', error=error)



# @app.route('/maps/<subroute>')
# def intro(subroute):
#   return render_template('/maps.html', subroute=subroute)
