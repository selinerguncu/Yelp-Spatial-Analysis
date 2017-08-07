import sqlite3

import os

global appPath
appPath = os.getcwd()

conn = sqlite3.connect(appPath + '/data/feedbackdb.sqlite')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS Feedback;
DROP TABLE IF EXISTS JSON;

CREATE TABLE Feedback (
    id              INTEGER PRIMARY KEY,
    name   TEXT,
    email   TEXT,
    about   TEXT,
    comment   TEXT
)

''')

conn.commit()
conn.close()
