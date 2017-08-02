import os
import sqlite3 as sqlite
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# APP_PATH = os.getcwd()

# conn = sqlite.connect(APP_PATH + '/data/yelpdb.sqlite')

# Load default config and override config from an environment variable
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
    rv = sqlite.connect(app.config['DATABASE'])
    rv.row_factory = sqlite.Row
    return rv


