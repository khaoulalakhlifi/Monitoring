from flask import Flask, render_template
import openmeteo_requests
from openmeteo_sdk.Variable import Variable
from geopy.geocoders import Nominatim
from app.admin.prediction_module import train_model, make_prediction
import requests_cache
import pandas as pd
from retry_requests import retry
 # Utilisez 'import matplotlib.pyplot as plt' au lieu de 'import matplotlib as plt'
from io import BytesIO
import base64
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import threading
import random
import time
import requests
import json
from app.admin.prediction_module import train_model, make_prediction 


# Fonction pour obtenir les coordonnées géographiques à partir du nom de la ville
def get_coordinates(city):
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError(f"Unable to find coordinates for the city: {city}")

# Saisie du nom de la ville depuis l'utilisateur
city = input("Entrez le nom de la ville : ")

# Obtention des coordonnées géographiques de la ville
latitude, longitude = get_coordinates(city)
print(f"Coordonnées de la ville {city} : Latitude {latitude}, Longitude {longitude}")

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Assurez-vous que toutes les variables météorologiques requises sont répertoriées ici
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability"]
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
    start=pd.to_datetime(hourly.Time(), unit="s"),
    end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
    freq=pd.Timedelta(seconds=hourly.Interval()),
    inclusive="left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["precipitation_probability"] = hourly_precipitation_probability

hourly_dataframe = pd.DataFrame(data=hourly_data)
print(hourly_dataframe)
# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
current_temperature = hourly.Variables(0).ValuesAsNumpy()[0]
current_relative_humidity = hourly.Variables(1).ValuesAsNumpy()[0]

# Utilisez les données pour entraîner les modèles
models = train_model(hourly_dataframe)

new_data = {
    'temperature_2m': current_temperature,
    'relative_humidity_2m': current_relative_humidity,
}

# Faites la prédiction avec les modèles entraînés
prediction_temperature, prediction_humidity = make_prediction(models, new_data)

print(f'Temperature Prediction: {prediction_temperature}')
print(f'Humidity Prediction: {prediction_humidity}')

