# import dependencies

import datetime as dt
from secrets import token_bytes
import numpy as np
import pandas as pd

# import dependencies we need for SQLAlchemy

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import dependency we need for Flask
from flask import Flask, jsonify
from sympy import stationary_points

# Set up the Database. The "create_engine" function allows me to access and query the SQLite database.

engine = create_engine("sqlite:///hawaii.sqlite")

# define "Base"

Base = automap_base()


# The "Base.prepare()" is used to reflect the tables.

Base.prepare(engine, reflect=True)

# With the database reflected, we can save our references to each table.
# Create a variable for each class so that we can reference them later.

Measurement = Base.classes.measurement
Station = Base.classes.station

# Finally, create a session link from Python to our database.

session = Session(engine)

# Create a Flask application called "app"

app = Flask(__name__)

# Notice the "__name__ " variable in the code. This is a special type of variable in Python.
# It's value depends on where and how the code is run. For example, if we want to input out "app.py" 
# file into another Python file named "example.py", the variable "__name__ " would be set to "example"
# Here what it might look like:

# We can define the welcome route using the code below: 

@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end<br/>
    ''')


# Route for precipitation analysis. Code should be aligned all the way to the left.

@app.route("/api/v1.0/precipitation")

# Create the preciptation function

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jasonify(precip)

# Route for station analysis. Code should be aligned all the way to the left.

@app.route("/api/v1.0/stations")

# Create Stations() function

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Route for monthly temperature.

@app.route("/api/v1.0/tobs")

# Create function for monthly temperature

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


# Create routes for minimum, maximum, and average temperatures over time range.

start = input("What is your start date in %y-%m-%d format  ")
end = input("What is your end date in %y-%m-%d format  ")

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")


# Create function for min, max, and average temperature over input time range


def stats(start, end):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


# flask run
# After running this code, you'll be able to copy and paste the web address provided by Flask into a web browser. 
# Open /api/v1.0/temp/start/end route and check to make sure you get the correct result, which is # [null,null,null] # You would add the following path to the address in your web browser:
# /api/v1.0/temp/2017-06-01/2017-06-30
# should return
# ["temps":[71.0,77.21989528795811,83.0]]

# from tech help
# if __name__ == '__main__':
#     app.run()
