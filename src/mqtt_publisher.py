import paho.mqtt.client as mqtt

class MQTTPublisher:
    def __init__(self, broker: str, port: int):
        """
        Initialize the MQTT publisher.
        :param broker: MQTT broker address.
        :param port: MQTT broker port.
        """
        self.client = mqtt.Client()
        try:
            self.client.connect(broker, port)
            print(f"Connected to MQTT broker at {broker}:{port}")
        except Exception as e:
            print(f"Failed to connect to MQTT broker at {broker}:{port} - {e}")

    def publish(self, topic: str, message: str):
        """
        Publish a message to a specific topic.
        :param topic: MQTT topic.
        :param message: Message payload (string).
        """
        result = self.client.publish(topic, message)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Message published to topic {topic}: {message}")
        else:
            print(f"Failed to publish message to topic {topic}: {message} - {result.rc}")

    def disconnect(self):
        """
        Disconnect from the MQTT broker.
        """
        self.client.disconnect()
        print("Disconnected from MQTT broker")