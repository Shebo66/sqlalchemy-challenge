#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/temp<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations"
    )


@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations names"""
    # Query all stations
    results = session.query(station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/prcp")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all prcp"""
    # Query all stations
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    #all_prcp = list(np.ravel(results))
    all_prcp = results

    return jsonify(all_prcp)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs"""
    # Query all stations
    last_year=dt.date(2017,8,23)-dt.timedelta(days=365)
    temperature = session.query(measurement.tobs).filter(measurement.station=='USC00519281').filter(measurement.date>=last_year).all()
    session.close()

    # Convert list of tuples into normal list
    #all_prcp = list(np.ravel(results))
    all_tobs = temperature

    return jsonify(all_tobs)


@app.route("/api/v1.0/temp/<start><end>")
def temp(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs"""
    # Query all stations
    temp = session.query(func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).filter(measurement.date>=start).filter(measurement.date<=end).all()
     
    session.close()

    # Convert list of tuples into normal list
    #all_prcp = list(np.ravel(results))
    all_temp = temp

    return jsonify(all_temp)

if __name__ == '__main__':
    app.run(debug=True)

