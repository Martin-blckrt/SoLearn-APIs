import os
import pandas as pd
import numpy as np
import json
from datetime import timedelta, datetime
import json

"""
Call OpenWeather and Solcast API to provide data to the model

Solcast data example:
"lat": 43.3412,
	"lon": 3.214,
	"timezone": "Europe/Paris",
	"timezone_offset": 7200,
	"hourly": [
		{
			"dt": 1654693200,
			"temp": 298.53,
			"feels_like": 298.38,
			"pressure": 1013,
			"humidity": 48,
			"dew_point": 286.73,
			"uvi": 7.13,
			"clouds": 100,
			"visibility": 10000,
			"wind_speed": 6.24,
			"wind_deg": 318,
			"wind_gust": 9.18,
			"weather": [
				{
					"id": 804,
					"main": "Clouds",
					"description": "overcast clouds",
					"icon": "04d"
				}
			],
			"pop": 0
		},

Open data example:
"forecasts": [
		{
			"ghi": 601,
			"ghi90": 731,
			"ghi10": 475,
			"ebh": 103,
			"dni": 118,
			"dni10": 26,
			"dni90": 421,
			"dhi": 498,
			"air_temp": 24,
			"zenith": 28,
			"azimuth": 131,
			"cloud_opacity": 31,
			"period_end": "2022-06-08T13:30:00.0000000Z",
			"period": "PT30M"
		},

Features needed:


Output of parsing:
key             match key           source
t_h
HiSolarRad	    ghi                 solcast
SolarRad	    ghi                 solcast
SolarEnergy	    ghi*0.001433/30     solcast
d_m	                        
OutHum	        humidity            open_weather
Bar	            pressure            open_weather
DewPt	        dew_point           open_weather
"""

SAVE_FOLDER = os.path.join(os.getcwd(), "weather_data", "formatted_data")

class Parser():
	def __init__(self, open_json, solcast_json, save = False, save_format = "json", lat = None, lon = None):
		self.open_json = open_json
		self.solcast_json = solcast_json
		self.save = save
		self.save_format = save_format
		self.lat = lat
		self.lon = lon

	def transfom(self):
		df = pd.concat([self.format_solcast(), self.format_open_weather()], axis=1)
		df = df.reindex(columns=['t_h', 'HiSolarRad', 'SolarRad', 'SolarEnergy', 'd_m', 'OutHum', 'Bar', 'DewPt'])
		if self.save:
			date = datetime.now().strftime("%d%m%Y-%H%M")
			try:
				path = os.path.join(SAVE_FOLDER, f"{self.lat}-{self.lon}_{date}.{self.save_format}")
				df.to_json(path)
			except:
				raise
		return df

	def format_solcast(self):
		solcast_data = self.solcast_json['forecasts']
		solcast_data_df = pd.DataFrame(solcast_data)
		# REDUCE DATAFRAME
		solcast_data_df_reduced = solcast_data_df[['period_end', 'ghi', 'ghi90']].copy()
		# CREATE SolaEnergy FEATURE
		solcast_data_df_reduced['SolarEnergy'] = (solcast_data_df_reduced['ghi'] * 0.001433 * 30)
		# CONVERT period_end TO datetime
		solcast_data_df_reduced['dt'] = np.nan
		solcast_data_df_reduced['t_h'] = np.nan
		solcast_data_df_reduced['d_m'] = np.nan
		for index in solcast_data_df_reduced.index:
			date = solcast_data_df_reduced.loc[index, 'period_end'].split('.')[0]
			solcast_data_df_reduced.loc[index, 'dt'] = datetime.strptime( date, '%Y-%m-%dT%H:%M:%S')
			solcast_data_df_reduced.loc[index, 'dt'] += timedelta(minutes=-30)
			# CREATE t_h AND d_m FEATURES
			dt_splited = str(solcast_data_df_reduced.loc[index, 'dt']).split(' ')
			date = dt_splited[0]
			time = dt_splited[1]
			solcast_data_df_reduced.loc[index, 't_h'] = time.split(':')[0]
			# solcast_data_df_reduced['t_h'] = solcast_data_df_reduced['t_h'].astype(str).astype(int)
			solcast_data_df_reduced.loc[index, 'd_m'] = date.split('-')[1]
			# solcast_data_df_reduced['d_m'] = solcast_data_df_reduced['d_m'].astype(str).astype(int)
		solcast_data_df_reduced = solcast_data_df_reduced.drop(['period_end'], axis = 1)
		# DROP LAST ROW
		solcast_data_df_reduced.drop(solcast_data_df_reduced.tail(1).index, inplace = True)
		# RENAME COLUMNS
		solcast_data_df_reduced.rename(columns = {'dt':'datetime', 'ghi90':'HiSolarRad', 'ghi' : 'SolarRad' }, inplace = True)
		# REINDEX
		solcast_data_df_reduced = solcast_data_df_reduced.set_index('datetime')
		solcast_data_df_reduced = solcast_data_df_reduced.sort_index()

		return solcast_data_df_reduced


	def format_open_weather(self):
		open_data = self.open_json['hourly']
		open_data_df = pd.DataFrame(open_data)
		# REDUCE DATAFRAME
		open_data_df_reduced = open_data_df[['dt', 'humidity', 'pressure', 'dew_point']].copy()
		# Convert dew_point FROM KELVIN TO CELSUIS
		open_data_df_reduced['dew_point'] = open_data_df_reduced['dew_point'] - 273.15
		# DUPLICATE ROWS
		open_data_df_reduced = pd.concat([open_data_df_reduced]*2, ignore_index=True)
		# CONVERT DATETIMES
		open_data_df_reduced['dt'] = pd.to_datetime(open_data_df_reduced['dt'], unit='s')
		# SORT ADN REINDEX
		open_data_df_reduced = open_data_df_reduced.sort_values('dt')
		open_data_df_reduced = open_data_df_reduced.reset_index(drop=True)
		# ADD 30 MIN TO DUPLICATED ROWS
		for index in open_data_df_reduced.index:
			if index % 2 == 1:
				open_data_df_reduced.loc[index, 'dt'] += timedelta(minutes=30)
		# RENAME COLUMNS
		open_data_df_reduced.rename(columns = {'dt':'datetime', 'humidity':'OutHum', 'pressure':'Bar', 'dew_point': 'DewPt'}, inplace = True)
		# SET DATE AS INDEX
		open_data_df_reduced = open_data_df_reduced.set_index('datetime')
		open_data_df_reduced = open_data_df_reduced.sort_index()

		return open_data_df_reduced