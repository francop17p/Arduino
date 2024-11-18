import paho.mqtt.client as mqtt


class MQTTPublisher:
    def __init__(self, broker: str, port: int):
        """
        Initialize the MQTT publisher.
        :param broker: MQTT broker address.
        :param port: MQTT broker port.
        """
        self.client = mqtt.Client()
        self.client.connect(broker, port)

    def publish(self, topic: str, message: str):
        """
        Publish a message to a specific topic.
        :param topic: MQTT topic.
        :param message: Message payload (string).
        """
        self.client.publish(topic, message)

    def disconnect(self):
        """
        Disconnect from the MQTT broker.
        """
        self.client.disconnect()

