import serial

class ArduinoReader:
    def __init__(self, port: str, baudrate: int):
        """
        Initialize the serial connection to the Arduino.
        :param port: Serial port (e.g., '/dev/ttyACM0')
        :param baudrate: Baud rate (e.g., 9600)
        """
        self.serial_connection = serial.Serial(port, baudrate, timeout=1)

    def _to_brightness(self, value: float) -> str:
        if value > 900:
            return "Really Bright"
        elif value > 800:
            return "Bright"
        elif 400 <= value <= 800:
            return "Dim"
        else:
            return "Dark"

    def read_sensor_data(self):
        """
        Read data from the Arduino and parse it.
        :return: Dictionary with 'temperature', 'humidity', and 'light'
        """
        if self.serial_connection.in_waiting > 0:
            line = self.serial_connection.readline().decode('utf-8').strip()
            try:
                temperature, humidity, light = map(float, line.split(','))
                brightness = self._to_brightness(light)
                return {
                    'temperature': temperature,
                    'humidity': humidity,
                    'brightness': brightness
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

