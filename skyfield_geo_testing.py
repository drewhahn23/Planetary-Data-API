import pandas as pd 
import numpy as np 
from skyfield.api import load 
# from space_project_distance import conv_to_miles


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
	ra_jupiter, dec_juptier, distance_jupiter = position_jupiter.radec()

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
			'Saturn': x_saturn
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
			'Jupiter': dec_juptier.radians,
			'Saturn': dec_jupiter.radians,
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

	print(df_positions.T)


	return df_positions.T





if __name__ == '__main__':
	get_pos_relative_sun()
	# try:
	# 	get_pos()

	# except Exception as e:
	# 	print(e)