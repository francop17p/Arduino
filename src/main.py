import time
import json
from arduino_reader import ArduinoReader
from mqtt_publisher import MQTTPublisher

temperature_sensor_token = "token-sensor1"
light_sensor_token = "token-sensor2"

def load_config(config_path='config.json'):
    with open(config_path, 'r') as file:
        return json.load(file)

def main():
    config = load_config()

    arduino = ArduinoReader(port=config['serial_port'], baudrate=config['baudrate'])
    mqtt = MQTTPublisher(broker=config['mqtt_broker'], port=config['mqtt_port'])

    try:
        while True:
            data = arduino.read_sensor_data()
            if data:
                mqtt.publish(
                    topic=temperature_sensor_token,
                    message=json.dumps({
                        "temperature": data['temperature'],
                        "humidity": data['humidity'],
                    })
                )

                mqtt.publish(
                    topic=light_sensor_token,
                    message=json.dumps({
                        "brightness": data['brightness']
                    })
                )

                print(f"Data sent: {data}")
    except KeyboardInterrupt:
        print("Program finished.")
    finally:
        arduino.close()
        mqtt.disconnect()

if __name__ == "__main__":
    main();
