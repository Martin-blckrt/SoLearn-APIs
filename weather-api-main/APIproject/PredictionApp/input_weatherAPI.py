
from datetime import datetime
import json 
import os
import requests

LAT = 43.3412
LON = 3.214

WEATHER_FOLDER = os.path.join(os.getcwd(), "weather_data")
SOLCAST_FOLDER = "solcast"
OPEN_FOLDER = "open_weather"

TOKEN_OPEN = "49afb958f2e6418e3e582687eeda45b4"
TOKEN_SOLCAST = "bm6u4mB_RRGjzJb_OFKvMbuVdfjS9bMl"


def getOpenWeatherData(latitude, longitude, save_txt=True, save_json=True):
    headers = {'Content-Type': 'application/json'}
    url_open = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=current,minutely,daily,alerts&appid={TOKEN_OPEN}"
    try:
        response = requests.get(url_open, headers=headers)
    except:
        raise
    if save_json:
        saveFile(json.dumps(response.json()), latitude, longitude, "json", solcast_data=False)
    if save_txt:
        saveFile(response.text, latitude, longitude, "txt", solcast_data=False)
    return response.json()


def getSolcastData(latitude, longitude, hours=48, save_txt=True, save_json=True):
    headers = {'Content-Type': 'application/json'}
    url_solcast = f"https://api.solcast.com.au/world_radiation/forecasts?latitude={latitude}&longitude={longitude}&hours={hours}&api_key={TOKEN_SOLCAST}"
    try:
        response = requests.get(url_solcast, headers=headers)
    except:
        raise 
    if save_json:
        saveFile(json.dumps(response.json()), latitude, longitude, "json", solcast_data=True)
    if save_txt:
        saveFile(response.text, latitude, longitude, "txt", solcast_data=True)
    return response.json()


def saveFile(obj, latitude, longitude, format, solcast_data=True):
    date = datetime.now().strftime("%d%m%Y-%H%M")
    folder = OPEN_FOLDER
    if solcast_data:
        folder = SOLCAST_FOLDER
    try:
        path = os.path.join(WEATHER_FOLDER, folder, f"{latitude}-{longitude}_{date}.{format}")
        with open(path, "w+") as outfile:
            outfile.write(obj)
    except:
        raise