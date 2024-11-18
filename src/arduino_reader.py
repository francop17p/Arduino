import serial

class ArduinoReader:
    def __init__(self, port: str, baudrate: int):
        """
        Initialize the serial connection to the Arduino.
        :param port: Serial port (e.g., '/dev/ttyACM0')
        :param baudrate: Baud rate (e.g., 9600)
        """
        self.serial_connection = serial.Serial(port, baudrate, timeout=1)

    def read_sensor_data(self):
        """
        Read data from the Arduino and parse it.
        :return: Dictionary with 'temperature', 'humidity', and 'light'
        """
        if self.serial_connection.in_waiting > 0:
            line = self.serial_connection.readline().decode('utf-8').strip()
            try:
                temperature, humidity, light = map(float, line.split(','))
                return {
                    'temperature': temperature,
                    'humidity': humidity,
                    'light': light
                }
            except ValueError:
                print(f"Error parsing line: {line}")
                return None
        return None

    def close(self):
        """
        Close the serial connection.
        """
        self.serial_connection.close()

