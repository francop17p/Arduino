import time
import json
import serial
from arduino_reader import ArduinoReader
from mqtt_publisher import MQTTPublisher

object_sensor_token = "1501b86d-5899-4b8b-a6da-99ccc1b1f021"

def load_config(config_path='config.json'):
    with open(config_path, 'r') as file:
        return json.load(file)

def read_sensor_data(serial_port):
    try:
        line = serial_port.readline().decode('utf-8').strip()
        if line:
            try:
                data = json.loads(line)
                return data
            except json.JSONDecodeError:
                print("Error al analizar la línea: ", line)
                return None
    except Exception as e:
        print(f"Error leyendo datos del puerto serie: {e}")
        return None

def main():
    print("Program started.")
    config = load_config()

    serial_port = serial.Serial(config['serial_port'], baudrate=config['baudrate'], timeout=1)

    mqtt = MQTTPublisher(broker=config['mqtt_broker'], port=config['mqtt_port'])

    try:
        while True:
            data = read_sensor_data(serial_port)
            if data and 'ObjetoDetectado' in data:
                if data['ObjetoDetectado'] == 1:
                    payload = {
                        "Objeto Detectado": "1"
                    }
                    print("Objeto detectado")
                    if not mqtt.client.is_connected():
                        print("MQTT client not connected, attempting to reconnect...")
                        mqtt.client.reconnect()
                    mqtt.publish(topic=object_sensor_token, message=json.dumps(payload))

    except KeyboardInterrupt:
        print("Program finished.")
    finally:
        serial_port.close()
        mqtt.disconnect()

if __name__ == "__main__":
    main()