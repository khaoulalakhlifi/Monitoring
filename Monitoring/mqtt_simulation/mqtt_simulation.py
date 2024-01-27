import paho.mqtt.client as mqtt
import time
import random
from pymongo import MongoClient
from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity

# Configuration MQTT
mqtt_broker = "test.mosquitto.org"
mqtt_topic = "environment_data"  # Changer le topic pour refléter les données de l'environnement

# Configuration MongoDB
mongo_host = "localhost"
mongo_port = 27017
mongo_db_name = "environment_data_db"
mongo_collection_name = "environment_data_collection"

# Configuration SNMP
snmp_device_ip = "192.168.1.1"  # Remplacez ceci par l'adresse IP de votre appareil SNMP

# Connexion à MongoDB
mongo_client = MongoClient(mongo_host, mongo_port)
db = mongo_client[mongo_db_name]
collection = db[mongo_collection_name]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message Published")

def get_snmp_data(ip_address, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),  # Remplacez 'public' par votre communauté SNMP
               UdpTransportTarget((ip_address, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )
    if errorIndication:
        return None
    else:
        return varBinds[0][1]

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect(mqtt_broker, 1883, 60)

while True:
    temperature = random.uniform(20, 30)  # Simuler la température ambiante
    humidity = random.uniform(40, 60)  # Simuler l'humidité

    # Utiliser SNMP pour obtenir des données supplémentaires (par exemple, charge mémoire)
    memory_usage = get_snmp_data(snmp_device_ip, '1.3.6.1.4.1.2021.4.6.0')  # Exemple d'OID pour la charge mémoire

    payload = {"temperature": temperature, "humidity": humidity, "memory_usage": memory_usage}

    # Convertir le payload en chaîne JSON
    payload_str = str(payload)

    # Envoyer les données de l'environnement via MQTT
    client.publish(mqtt_topic, payload_str)

    # Enregistrer les données dans MongoDB
    collection.insert_one(payload)

    print(f"Environment data sent and saved - Temperature: {temperature}, Humidity: {humidity}, Memory Usage: {memory_usage}")

    time.sleep(60)  # Attendre 60 secondes
