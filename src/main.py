import time
import json
from arduino_reader import ArduinoReader
from mqtt_publisher import MQTTPublisher
from mongodb_handler import MongoDBHandler

temperature_sensor_token = "17e4e62a-785d-4570-bff0-2b506338353f"
light_sensor_token = "token-sensor2"

def load_config(config_path='config.json'):
    with open(config_path, 'r') as file:
        return json.load(file)

def main():
    config = load_config()

    arduino = ArduinoReader(port=config['serial_port'], baudrate=config['baudrate'])
    mqtt = MQTTPublisher(broker=config['mqtt_broker'], port=config['mqtt_port'])
    mongo = MongoDBHandler(database=config['mongodb_database'])

    try:
        while True:
            data = arduino.read_sensor_data()
            if data:
                data_per_token = {
                    temperature_sensor_token: {
                        "temperature": data['temperature'],
                        "humidity": data['humidity']
                    },
                    light_sensor_token: {
                        "brightness": data['brightness']
                    }
                }
                for token, payload in data_per_token.items():
                    print(f"Data sent {token}: {payload}")
                    mqtt.publish(topic=token, message=json.dumps(payload))
                    mongo.insert_data(collection=token, data=payload)

    except KeyboardInterrupt:
        print("Program finished.")
    finally:
        arduino.close()
        mqtt.disconnect()

if __name__ == "__main__":
    main();
