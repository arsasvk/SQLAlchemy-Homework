import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
import datetime as dt
import json

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
	return (
		f"Available Routes are as follows: <br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/start/<br/>"
		f"/api/v1.0/start/<start_date>/<end_date><br/>"
	)


@app.route("/api/v1.0/precipitation")
def precipitation(): 

# Design a query to retrieve the last 12 months of precipitation data and plot the results
	latest_date = session.query(Measurement.date).order_by(Measurement.date.desc())

# Calculate the date 1 year ago from the last data point in the database
	last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
	sel = [Measurement.date, Measurement.prcp]
	year_presp = session.query(*sel).\
	filter(Measurement.date > last_year).\
	order_by(Measurement.date).all()

	presp_totals = []

	for p in year_presp:
		row = {}
		row["date"] = year_presp[0]
		row["presp"] = year_presp[1]
		presp_totals.append(row)

	return jsonify(presp_totals)


@app.route("/api/v1.0/stations")
def stations(): 

	station_list = session.query(Measurement.station.distinct()).all()

	station_names = list(np.ravel(station_list))

	return jsonify(station_names)



@app.route("/api/v1.0/tobs")
def tobs(): 

	# Design a query to retrieve the last 12 months of precipitation data and plot the results
	latest_date = session.query(Measurement.date).order_by(Measurement.date.desc())

# Calculate the date 1 year ago from the last data point in the database
	last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	sel_1 = [Measurement.date, Measurement.tobs]
	year_tobs = session.query(*sel_1).filter(and_(Measurement.date > last_year)).order_by(Measurement.date).all()
	return jsonify(year_tobs)

@app.route("/api/v1.0/start/<start_date>")
def start(start_date):
	#start_date = '2017-08-08'
	start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)
		).filter(Measurement.date >= start_date).all()
	temp_list = list(np.ravel(start_temp))
	return jsonify(temp_list)


@app.route("/api/v1.0/start/<start_date>/<end_date>")
def startend(start_date, end_date):
	#start_date = '2017-08-08'
	start_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)
		).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
	temp_list = list(np.ravel(start_temp))
	return jsonify(temp_list)


	
if __name__ == "__main__":
	app.run(debug=True)
