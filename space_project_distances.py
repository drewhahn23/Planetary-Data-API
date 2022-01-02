import numpy as np
import pandas as pd
import requests 
import json
import sys
from skyfield.api import load
from flask import Flask, render_template, redirect, url_for,request,jsonify
from flask import make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-type'

## getting distances of all planets from earth
def conv_to_miles(dist_in_au):
	return float(str(dist_in_au).split(' ')[0]) * 92955807.26743

def get_all_distances():
	ts = load.timescale()
	t = ts.now()
	planets = load('de421.bsp')

	earth, mercury = planets['earth'], planets['mercury']
	astrometric_mercury = earth.at(t).observe(mercury)
	ra_merc, dec_merc, distance_merc_au = astrometric_mercury.radec()

	earth, venus = planets['earth'], planets['venus']
	astrometric_venus = earth.at(t).observe(venus)
	ra_venus, dec_venus, distance_venus_au = astrometric_venus.radec()

	earth, mars = planets['earth'], planets['mars']
	astrometric_mars = earth.at(t).observe(mars)
	ra_mars, dec_mars, distance_mars_au = astrometric_mars.radec()

	earth, jupiter = planets['earth'], planets['JUPITER BARYCENTER']
	astrometric_jupiter = earth.at(t).observe(jupiter)
	ra_jup, dec_jup, distance_jupiter_au = astrometric_jupiter.radec()

	earth, saturn = planets['earth'], planets['SATURN BARYCENTER']
	astrometric_saturn = earth.at(t).observe(saturn)
	ra_sat, dec_sat, distance_saturn_au = astrometric_saturn.radec()

	earth, uranus = planets['earth'], planets['URANUS BARYCENTER']
	astrometric_uranus = earth.at(t).observe(uranus)
	ra_ur, dec_ur, distance_uranus_au = astrometric_uranus.radec()

	earth, neptune = planets['earth'], planets['NEPTUNE BARYCENTER']
	astrometric_neptune = earth.at(t).observe(neptune)
	ra_nep, dec_nep, distance_neptune_au = astrometric_neptune.radec()

	earth, pluto = planets['earth'], planets['PLUTO BARYCENTER']
	astrometric_pluto = earth.at(t).observe(pluto)
	ra_plut, dec_plut, distance_pluto_au = astrometric_pluto.radec()


	distance_merc_miles = conv_to_miles(distance_merc_au)
	distance_venus_miles = conv_to_miles(distance_venus_au)
	distance_mars_miles = conv_to_miles(distance_mars_au)
	distance_jupiter_miles = conv_to_miles(distance_jupiter_au)
	distance_saturn_miles = conv_to_miles(distance_saturn_au)
	distance_uranus_miles = conv_to_miles(distance_uranus_au)
	distance_neptune_miles = conv_to_miles(distance_neptune_au)
	distance_pluto_miles = conv_to_miles(distance_pluto_au)

	distances_dict = {

		'distance_au':{
		##need to add .au to distance_au because skyfield package returns distance object, not raw distance
			'Mercury': distance_merc_au.au,
			'Venus': distance_venus_au.au,
			'Mars': distance_mars_au.au,
			'Jupiter': distance_jupiter_au.au,
			'Saturn': distance_saturn_au.au,
			'Uranus': distance_uranus_au.au,
			'Neptune': distance_neptune_au.au,
			'Pluto': distance_neptune_au.au
		},
		'distance_miles':{
			'Mercury': distance_merc_miles,
			'Venus': distance_venus_miles,
			'Mars': distance_mars_miles,
			'Jupiter': distance_jupiter_miles,
			'Saturn': distance_saturn_miles,
			'Uranus': distance_uranus_miles,
			'Neptune': distance_neptune_miles,
			'Pluto': distance_pluto_miles
		}
	
	}



	df_distances = pd.DataFrame(distances_dict)
	df_distances['englishName'] = df_distances.index
	return df_distances













##getting other planet info 

def planet_info():

	base = 'api.le-systeme-solaire.net/rest/'

	bodies = 'https://api.le-systeme-solaire.net/rest/bodies/'

	body_list = requests.get(url=bodies)


	data = body_list.json()

	list_of_planets = ['Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']
	all_bodies = data['bodies']

	all_planet_data = []
	for obj in all_bodies:
		if obj['englishName'] in list_of_planets:
			all_planet_data.append(obj)


	df = pd.DataFrame(all_planet_data)
	df = df.drop(['id','vol','eccentricity','name','moons','isPlanet','dimension','discoveredBy','discoveryDate','alternativeName','axialTilt','mainAnomaly','argPeriapsis','longAscNode','aroundPlanet','sideralRotation','escape','inclination','avgTemp','rel','flattening','sideralOrbit','polarRadius','meanRadius'],axis=1)
	return df

##merging distance info and planetary info

def merge_dfs(df_distances,df):

	final_df = df.merge(df_distances, on='englishName')
	final_df.rename({'englishName':'name'},axis=1,inplace=True)
	#,'equaRadius':'Radius at Equator (km)'

	ordering_dict = {'Mercury':0,'Venus':1,'Mars':2,'Jupiter':3,'Saturn':4,'Uranus':5,'Neptune':6,'Pluto':7}
	final_df.sort_values(by=['name'],key=lambda x: x.map(ordering_dict),inplace=True)
	final_df.reset_index(inplace=True,drop=True)

	final_df = final_df[['name','distance_miles','distance_au','density','equaRadius','perihelion','aphelion','gravity','semimajorAxis']]
	final_df.rename({
		'distance_miles':'Distance from Earth (mi.)',
		'distance_au':'Distance from Earth (au)',
		'equaRadius':'Equatorial Radius (km)',
		'density':'Density',
		'perihelion':'Perihelion',
		'aphelion':'Aphelion',
		'gravity':'Gravity',
		'semimajorAxis':'Semi-Major Axis'
		},axis=1,inplace=True)
	return final_df

@app.route('/')
@cross_origin()

def main():
	distances = get_all_distances()
	planets = planet_info()
	df = merge_dfs(distances,planets)
	df.set_index('name',inplace=True)
	print(df)
	fin_dict = df.to_dict()
	return jsonify(fin_dict) 

# export FLASK_APP = space_project_distances.py

# flask run 

if __name__ == '__main__':
	try:
		app.run(debug=True)
		# main()
	except Exception as e:
		print(e)



