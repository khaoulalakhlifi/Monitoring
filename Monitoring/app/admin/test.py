from flask import Flask, render_template, request
from prediction_module import train_model, make_prediction
import openmeteo_requests
import requests_cache
from retry_requests import retry
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from geopy.geocoders import Nominatim

app = Flask(__name__)

def get_coordinates(city):
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError(f"Unable to find coordinates for the city: {city}")

def get_city_weather(city):
    latitude, longitude = get_coordinates(city)
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability"]
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

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

    hourly = response.Hourly()
    current_temperature = hourly.Variables(0).ValuesAsNumpy()[0]
    current_relative_humidity = hourly.Variables(1).ValuesAsNumpy()[0]

    models = train_model(hourly_dataframe)

    new_data = {
        'temperature_2m': current_temperature,
        'relative_humidity_2m': current_relative_humidity,
    }

    prediction_temperature, prediction_humidity = make_prediction(models, new_data)

    return {
        'latitude': latitude,
        'longitude': longitude,
        'hourly_dataframe': hourly_dataframe,
        'current_temperature': current_temperature,
        'current_relative_humidity': current_relative_humidity,
        'prediction_temperature': prediction_temperature,
        'prediction_humidity': prediction_humidity,
    }
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_city_weather(city)
        print("Weather Data:", weather_data)  # Ajoutez cette ligne pour le débogage
        return render_template('index.html', weather_data=weather_data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, threaded=False)