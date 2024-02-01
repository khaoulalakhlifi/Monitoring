from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import threading
import random
import time
import requests
import json
from geopy.geocoders import Nominatim
from openmeteo_requests import Client as OpenMeteoClient

import requests_cache
import pandas as pd
from retry_requests import retry
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modifiez votre modèle Client dans app.py

# Modifiez votre modèle Client dans app.py
class Client(db.Model):  # Utilisez db.Model au lieu de db.Document
    # Fields of the Client model
    id = db.Column(db.Integer, primary_key=True)
    client_type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(15))
    mac_address = db.Column(db.String(17))
    mqtt_topic = db.Column(db.String(100))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)


# Variable globale pour stocker les dernières données MQTT
latest_mqtt_data = {"temperature": 0.0, "humidity": 0.0}

# Logique de mise à jour des données MQTT (exemple)
def update_mqtt_data(new_data):
    global latest_mqtt_data
    latest_mqtt_data = new_data

# Simulation de la réception des données MQTT (à remplacer par votre logique réelle)
def simulate_mqtt_data():
    while True:
        temperature = random.uniform(20, 30)
        humidity = random.uniform(40, 60)
        new_data = {"temperature": temperature, "humidity": humidity}
        update_mqtt_data(new_data)
        print(f"Simulated MQTT Data - Temperature: {temperature}, Humidity: {humidity}")
        time.sleep(60)


# Exécutez la simulation en arrière-plan (à intégrer dans votre script principal)
mqtt_thread = threading.Thread(target=simulate_mqtt_data)
mqtt_thread.start()

# Variable globale pour stocker les dernières données HTTP
latest_http_data = {"temperature": 0.0, "humidity": 0.0}

# Logique de mise à jour des données HTTP (exemple)
def update_http_data(new_data):
    global latest_http_data
    latest_http_data = new_data
 






# Simulation de l'envoi des données HTTP (à remplacer par votre logique réelle)
def simulate_http_data():
    while True:
        temperature = random.uniform(20, 30)
        humidity = random.uniform(40, 60)
        new_data = {"temperature": temperature, "humidity": humidity}
        update_http_data(new_data)
        
        # Envoyer les données de l'environnement via HTTP
        try:
            http_server_url = "https://eoc2y198jtisdhc.m.pipedream.net"
            response = requests.post(http_server_url, data=json.dumps(new_data), headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                print(f"Environment data sent via HTTP - Temperature: {temperature}, Humidity: {humidity}")
            else:
                print(f"Failed to send data via HTTP - Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error sending data via HTTP: {e}")

        time.sleep(60)

# Exécutez la simulation en arrière-plan (à intégrer dans votre script principal)
http_thread = threading.Thread(target=simulate_http_data)
http_thread.start()
# ... (votre code Flask actuel)
@app.route('/predict_weather')
def select_data_type():
    if request.method == 'POST':
        data_type = request.form['data_type']
    elif request.method == 'GET':
        data_type = request.args.get('data_type', 'both')
    else:
        return jsonify({"error": "Invalid request method"})

    mqtt_data = latest_mqtt_data
    http_data = latest_http_data

    selected_data = {}

    if data_type == 'temperature':
        selected_data['mqttTemperature'] = mqtt_data['temperature']
        selected_data['httpTemperature'] = http_data['temperature']
    elif data_type == 'humidity':
        selected_data['mqttHumidity'] = mqtt_data['humidity']
        selected_data['httpHumidity'] = http_data['humidity']
    else:
        selected_data['mqttTemperature'] = mqtt_data['temperature']
        selected_data['mqttHumidity'] = mqtt_data['humidity']
        selected_data['httpTemperature'] = http_data['temperature']
        selected_data['httpHumidity'] = http_data['humidity']

    return jsonify(selected_data)



@app.route('/')
def index():
    return render_template('admin/iotSection.html')


# Route pour la section IoT
@app.route('/iot')
def iot_section():
    return render_template('admin/iotSection.html')
models = None  # Remplacez None par l'objet réel de vos modèles

# Créez une fonction pour initialiser les modèles
def initialize_models():
    global models



# Route pour récupérer les données MQTT
@app.route('/mqtt_data', methods=['GET'])
def get_mqtt_data():
    # Accédez aux dernières données MQTT stockées dans la variable globale
    mqtt_data = latest_mqtt_data
    return jsonify(mqtt_data)

# Route pour récupérer les données HTTP
@app.route('/http_data', methods=['GET'])
def get_http_data():
    # Accédez aux dernières données HTTP stockées dans la variable globale
    http_data = latest_http_data
    return jsonify(http_data)
app.static_folder = 'static'


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        client_type = request.form.get('client_type')
        name = request.form.get('name')
        ip_address = request.form.get('ip_address')
        mac_address = request.form.get('mac_address')
        mqtt_topic = request.form.get('mqtt_topic')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')

        new_client = Client(
            client_type=client_type,
            name=name,
            ip_address=ip_address,
            mac_address=mac_address,
            mqtt_topic=mqtt_topic,
            longitude=longitude,
            latitude=latitude
        )
        db.session.add(new_client)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_client.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    
    app.run(debug=True, use_reloader=False, threaded=False)

