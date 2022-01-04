import numpy as np
import pandas as pd
import requests 
import json
import sys
from skyfield.api import load
from flask import Flask, render_template, redirect, url_for,request,jsonify
from flask import make_response
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
# from skyfield_geo_testing import get_pos_relative_sun

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-type'
api =  Api(app)

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

	# relative_sun = get_pos_relative_sun()
	# df_relative_sun = pd.DataFrame(relative_sun)

	# df_distances = df_distances.merge(df_relative_sun,on='englishName')

	##upon merge - earth gets dropped from df -> might be a problem -> maybe dont merge, call get_pos from different app route?

	df_distances = df_distances.apply(lambda x: time_to_reach(x),axis=1)
	# print(df_distances)
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

#time to reach traveling at avg speed taken to get to mars: 26.5 km/s

def time_to_reach(row):

	dist_kilo = float(row['distance_miles']) * 1.609344
	time_in_s = dist_kilo/26.5
	years = round(float(time_in_s/(3600*24*365)),3)

	row['Years to Reach'] = years

	return row


##merging distance info and planetary info

def merge_dfs(df_distances,df):

	final_df = df.merge(df_distances, on='englishName')
	final_df.rename({'englishName':'name'},axis=1,inplace=True)
	#,'equaRadius':'Radius at Equator (km)'

	ordering_dict = {'Mercury':0,'Venus':1,'Mars':2,'Jupiter':3,'Saturn':4,'Uranus':5,'Neptune':6,'Pluto':7}
	final_df.sort_values(by=['name'],key=lambda x: x.map(ordering_dict),inplace=True)
	final_df.reset_index(inplace=True,drop=True)

	final_df = final_df[['name','distance_miles','distance_au','density','equaRadius','perihelion','aphelion','gravity','Years to Reach']]
	final_df.rename({
		'distance_miles':'Distance from Earth (mi.)',
		'distance_au':'Distance from Earth (au)',
		'equaRadius':'Equatorial Radius (km)',
		'density':'Density',
		'perihelion':'Perihelion',
		'aphelion':'Aphelion',
		'gravity':'Gravity',
		# 'semimajorAxis':'Semi-Major Axis'
		},axis=1,inplace=True)
	return final_df

# api.add_resource('/')
@app.route('/')
@cross_origin()

def main():
	distances = get_all_distances()
	planets = planet_info()
	df = merge_dfs(distances,planets)
	df.set_index('name',inplace=True)
	df = df.T
	# print(df)
	fin_dict = df.to_dict()
	return jsonify(fin_dict) 


# api.add_resource('/positions',endpoints='positions')
@app.route('/positions')
@cross_origin()

def get_pos_relative_sun():
	ts = load.timescale()
	t = ts.now()
	eph = load('de421.bsp')

	sun, mercury = eph['sun'], eph['mercury']
	position_mercury = sun.at(t).observe(mercury)
	x_mercury, y_mercury, z_mercury = position_mercury.xyz.au
	ra_mercury, dec_mercury, distance_mercury = position_mercury.radec()

	sun, venus = eph['sun'], eph['venus']
	position_venus = sun.at(t).observe(venus)
	x_venus, y_venus, z_venus = position_venus.xyz.au
	ra_venus, dec_venus, distance_venus = position_venus.radec()


	sun, earth = eph['sun'], eph['earth']

	position_earth = sun.at(t).observe(earth)
	# print('Cartesian ICRS: ')

	#all of these are relative to sun
	x_earth, y_earth, z_earth = position_earth.xyz.au
	# print(' x = {} au'.format(x))
	# print(' y = {} au'.format(y))
	# print(' z = {} au'.format(z))

	ra_earth, dec_earth, distance_earth = position_earth.radec()
	# print(' ', ra, 'right ascension')
	# print(' ', dec, 'declination')
	# print(' ', distance, 'distance')

	sun, mars = eph['sun'], eph['mars']
	position_mars = sun.at(t).observe(mars)
	x_mars, y_mars, z_mars = position_mars.xyz.au
	ra_mars, dec_mars, distance_mars = position_mars.radec()

	sun, jupiter = eph['sun'], eph['JUPITER BARYCENTER']
	position_jupiter = sun.at(t).observe(jupiter)
	x_jupiter, y_jupiter, z_jupiter = position_jupiter.xyz.au
	ra_jupiter, dec_jupiter, distance_jupiter = position_jupiter.radec()

	sun, saturn = eph['sun'], eph['SATURN BARYCENTER']
	position_saturn = sun.at(t).observe(saturn)
	x_saturn, y_saturn, z_saturn = position_saturn.xyz.au
	ra_saturn, dec_saturn, distance_saturn = position_saturn.radec()

	sun, uranus = eph['sun'], eph['URANUS BARYCENTER']
	position_uranus = sun.at(t).observe(uranus)
	x_uranus, y_uranus, z_uranus = position_uranus.xyz.au 
	ra_uranus, dec_uranus, distance_uranus = position_uranus.radec()

	sun, neptune = eph['sun'], eph['NEPTUNE BARYCENTER']
	position_neptune = sun.at(t).observe(neptune)
	x_neptune, y_neptune, z_neptune = position_neptune.xyz.au 
	ra_neptune, dec_neptune, distance_neptune = position_neptune.radec()

	sun, pluto = eph['sun'], eph['PLUTO BARYCENTER']
	position_pluto = sun.at(t).observe(pluto)
	x_pluto, y_pluto, z_pluto = position_pluto.xyz.au 
	ra_pluto, dec_pluto, distance_pluto = position_pluto.radec()

	position_dict = {

		'x_coord': {

			'Mercury':x_mercury,
			'Venus':x_venus,
			'Earth':x_earth,
			'Mars': x_mars,
			'Jupiter': x_jupiter,
			'Saturn': x_saturn,
			'Uranus': x_uranus,
			'Neptune': x_neptune,
			'Pluto':x_pluto 
		},
		'y_coord': {
			'Mercury':y_mercury,
			'Venus':y_venus,
			'Earth':y_earth,
			'Mars': y_mars,
			'Jupiter': y_jupiter,
			'Saturn': y_saturn,
			'Uranus': y_uranus,
			'Neptune': y_neptune,
			'Pluto': y_pluto
		},
		'z_coord': {
			'Mercury':z_mercury,
			'Venus':z_venus,
			'Earth':z_earth,
			'Mars': z_mars,
			'Jupiter': z_jupiter,
			'Saturn': z_saturn,
			'Uranus': z_uranus,
			'Neptune': z_neptune,
			'Pluto': z_pluto
		},
		'right_ascension': {
			'Mercury':ra_mercury.radians,
			'Venus':ra_venus.radians,
			'Earth':ra_earth.radians,
			'Mars': ra_mars.radians,
			'Jupiter': ra_jupiter.radians,
			'Saturn': ra_saturn.radians,
			'Uranus': ra_uranus.radians,
			'Neptune': ra_neptune.radians,
			'Pluto': ra_pluto.radians
		},
		'declination': {
			'Mercury':dec_mercury.radians,
			'Venus':dec_venus.radians,
			'Earth':dec_earth.radians,
			'Mars': dec_mars.radians,
			'Jupiter': dec_jupiter.radians,
			'Saturn': dec_saturn.radians,
			'Uranus': dec_uranus.radians,
			'Neptune': dec_neptune.radians,
			'Pluto': dec_pluto.radians
		},
		'distance_au_from_sun': {
			'Mercury':distance_mercury.au,
			'Venus':distance_venus.au,
			'Earth':distance_earth.au,
			'Mars': distance_mars.au,
			'Jupiter': distance_jupiter.au,
			'Saturn': distance_saturn.au,
			'Uranus': distance_uranus.au,
			'Neptune': distance_neptune.au,
			'Pluto': distance_pluto.au
		}
	}

	df_positions = pd.DataFrame(position_dict)
	# df_positions['name'] = df_positions.index

	# df_positions = df_positions[['']]

	final_df = df_positions.T
	fin_dict_pos = final_df.to_dict()


	return jsonify(fin_dict_pos)


# export FLASK_APP = space_project_distances.py

# flask run 

if __name__ == '__main__':
	try:
		app.run(debug=True)
		# main()
	except Exception as e:
		print(e)



