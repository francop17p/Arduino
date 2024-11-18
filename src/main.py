import time
import json
from arduino_reader import ArduinoReader

def main():
    arduino = ArduinoReader(port='/dev/ttyACM0', baudrate=9600)
    try:
        while True:
            data = arduino.read_sensor_data()
            if data:
                print(f"Temperature: {data['temperature']}°C, "
                      f"Humidity: {data['humidity']}%, "
                      f"Light: {data['light']} units")
    except KeyboardInterrupt:
        print("Program finished.")
    finally:
        arduino.close()

if __name__ == "__main__":
    main();
