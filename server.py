import paho.mqtt.client as mqtt
import pymongo
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de MongoDB
mongo_uri = os.getenv("MONGODB_URI")
mongo_db = "SensorLogs"
mongo_collection = "f44d63b2-6345-4ad2-a472-4d1a2b8f107d"

# Conectar a MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

# Configuración de MQTT
mqtt_broker = "192.168.1.33"
mqtt_port = 1883
mqtt_topic = "f44d63b2-6345-4ad2-a472-4d1a2b8f107d"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        collection.insert_one(data)
        print("Data inserted into MongoDB")
    except Exception as e:
        print(f"Failed to insert data into MongoDB: {e}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker, mqtt_port, 60)

mqtt_client.loop_forever()