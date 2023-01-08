from multiprocessing.reduction import duplicate
import os
from input_weatherAPI import getOpenWeatherData, getSolcastData, saveFile
import pandas as pd
import numpy as np
import json
from datetime import datetime
from datetime import timedelta
import json

from sklearn.model_selection import cross_val_predict
from catboost import CatBoostRegressor, Pool

MODEL_PATH = os.path.join(os.getcwd(), "models", "saved_models", "catboost_model.json")
CROSS_VAL = 10

OPEN_FILE = "./weather_data/open_weather/43.3412-3.214_09062022-1108.json"
SOLCAST_FILE = "./weather_data/solcast/43.3412-3.214_09062022-1108.json"

DATA_PATH = os.path.join(os.getcwd(), 'models', 'data', 'hourly_weather_delteil.csv')

LAT = 43.3412
LON = 3.214

def open_weather():
    # GET AND SAVE OPEN WEATHER DATA
    # getOpenWeatherData(LAT, LON, save_txt=True, save_json=True)
    # getSolcastData(LAT, LON, hours=48, save_txt=True, save_json=True)
    
    # READING OPEN JSON FILES
    try:
        open_file = open(OPEN_FILE)
    except:
        raise
    open_json = json.load(open_file)
    open_data = open_json['hourly']
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


def solcast():
    # GET AND SAVE OPEN WEATHER DATA
    # getSolcastData(LAT, LON, hours=48, save_txt=True, save_json=True)
    
    # READING SOLCAST JSON FILES
    try:
        solcast_file = open(SOLCAST_FILE)
    except:
        raise
    solcast_json = json.load(solcast_file)
    solcast_data = solcast_json['forecasts']
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

def concat(solcast, open_weather):
    df = pd.concat([solcast, open_weather], axis=1)
    df = df.reindex(columns=['t_h', 'HiSolarRad', 'SolarRad', 'SolarEnergy', 'd_m', 'OutHum', 'Bar', 'DewPt'])
    print(df)
    print(df.dtypes)
    df.to_csv(r'.\weather_data\open_solcast.csv')
    return df


def training_data():
    big_df = pd.read_csv(DATA_PATH, low_memory=False, index_col='datetime', parse_dates=True)
    df = big_df[[
    't_h',
    'HiSolarRad',
    'SolarRad',
    'SolarEnergy',
    'd_m',
    'OutHum',
    'Bar',
    'DewPt']]
    for key in df.columns:   
        df[key].replace(to_replace='---', value=np.nan)
    df = df.dropna()
    print(df.loc[df['d_m'] == 6])
    new_df = df.loc[df['d_m'] == 6]
    print(new_df.dtypes)
    new_df.to_csv(r'.\weather_data\train_data.csv')
    return df

def predict(X):
    model = CatBoostRegressor()
    model.load_model(MODEL_PATH, format='json')
    cross_predictions = model.predict(X)
    print(cross_predictions)
    return cross_predictions


if __name__ == "__main__":
    concat(solcast(), open_weather())
    training_data()
    res = predict(concat(solcast(), open_weather()))
    print(len(res))