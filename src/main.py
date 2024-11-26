import time
import json
from arduino_reader import ArduinoReader
from mqtt_publisher import MQTTPublisher
from mongodb_handler import MongoDBHandler

object_sensor_token = "f44d63b2-6345-4ad2-a472-4d1a2b8f107d"

def load_config(config_path='config.json'):
    with open(config_path, 'r') as file:
        return json.load(file)

def main():
    print("Program started.")
    config = load_config()

    arduino = ArduinoReader(port=config['serial_port'], baudrate=config['baudrate'])
    mqtt = MQTTPublisher(broker=config['mqtt_broker'], port=config['mqtt_port'])
    mongo = MongoDBHandler(database=config['mongodb_database'])

    try:
        while True:
            data = arduino.read_sensor_data()
            if data and data['object_detected'] == 1:
                payload = {
                    "Objeto Detectado": "1"
                }
                print("Objeto detectado")
                mqtt.publish(topic=object_sensor_token, message=json.dumps(payload))
                mongo.insert_data(collection=object_sensor_token, data=payload)

    except KeyboardInterrupt:
        print("Program finished.")
    finally:
        arduino.close()
        mqtt.disconnect()

if __name__ == "__main__":
    main()