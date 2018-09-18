#import dependancies 
from flask import Flask, jsonify
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect, func
engine = create_engine("sqlite:///Resources/hawaii2.sqlite", connect_args={'check_same_thread': False}, echo=True)
from sqlalchemy.orm import Session

#set up base classes 
session = Session(bind=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
measurement = Base.classes.Measurements
station = Base.classes.Stations

#CREATE DICTIONARY OF DATES AND PRECIPITATION FOR LAST YEAR
precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date.between('2015-01-01','2015-12-31')).all() 
precip_dict = dict(precipitation)

#CREATE DICTIONARY OF STATIONS 
stations_list = session.query(station.station, station.name).all()
stations_dict = dict(stations_list)

#CREATE DICTIONARY OF DATES AND TOBS FOR LAST YEAR
temperatures = session.query(measurement.date, measurement.tobs).filter(measurement.date.between('2015-01-01','2015-12-31')).all()
tobs_dict = dict(temperatures)



#SET UP FLASK ROUTES
app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Hawaii Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end"
    ) 
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):
    average = session.query(func.avg(measurement.tobs)).filter(measurement.date.between(start, end)).all()
    maximum = session.query(func.max(measurement.tobs)).filter(measurement.date.between(start, end)).all()
    minimum = session.query(func.min(measurement.tobs)).filter(measurement.date.between(start, end)).all()
    temp_dict = {}
    temp_dict["Average Temperature"] = average
    temp_dict["Minimum Temperature"] = minimum
    temp_dict["Maximum Temperature"] = maximum
    return jsonify(temp_dict)

if __name__ == "__main__":
    app.run(debug=True)