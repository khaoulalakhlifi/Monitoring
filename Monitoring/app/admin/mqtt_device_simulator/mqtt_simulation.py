import paho.mqtt.client as mqtt
import time
import random

# Configuration MQTT
mqtt_broker = "test.mosquitto.org"
mqtt_topic = "environment_data"  # Changer le topic pour refléter les données de l'environnement

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message Published")

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect(mqtt_broker, 1883, 60)

while True:
    temperature = random.uniform(20, 30)  # Simuler la température ambiante
    humidity = random.uniform(40, 60)  # Simuler l'humidité

    payload = {"temperature": temperature, "humidity": humidity}

    # Convertir le payload en chaîne JSON
    payload_str = str(payload)

    # Envoyer les données de l'environnement via MQTT
    client.publish(mqtt_topic, payload_str)

    print(f"Environment data sent - Temperature: {temperature}, Humidity: {humidity}")

    time.sleep(60)  # Attendre 60 secondes
