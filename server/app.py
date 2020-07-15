from flask import Flask, jsonify, g
from flask_cors import CORS
import sqlite3

import sys
sys.path.insert(0, '..')
from flights_db import select_all


DBNAME = 'flights'

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect('flights.sqlite3')
  return db

# sanity check route
@app.route('/all_flights', methods=['GET'])
def get_all_flights():
    cur = get_db().execute('SELECT * FROM flights')
    rv = cur.fetchall()
    cur.close()
    return jsonify(rv)

@app.route('/', methods=['GET'])
def description():
  return "<h1>Get Flight Information</h1>"


if __name__ == '__main__':
  app.run(host='10.0.0.62', port='4000')
