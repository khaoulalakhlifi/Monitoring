import requests
import time
import random
import json

# URL de votre serveur HTTP
http_server_url = "https://eoc2y198jtisdhc.m.pipedream.net"  # Remplacez par votre URL

while True:
    temperature = random.uniform(20, 30)  # Simuler la température ambiante
    humidity = random.uniform(40, 60)  # Simuler l'humidité

    payload = {"temperature": temperature, "humidity": humidity}

    # Envoyer les données de l'environnement via HTTP
    try:
        response = requests.post(http_server_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print(f"Environment data sent via HTTP - Temperature: {temperature}, Humidity: {humidity}")
        else:
            print(f"Failed to send data via HTTP - Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data via HTTP: {e}")

    time.sleep(60)  # Attendre 60 secondes
