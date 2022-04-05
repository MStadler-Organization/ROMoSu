import logging

from paho.mqtt import client as mqtt_client
import json


class MQTTForwarder:
    def __init__(self, host, port=1883):
        self.host = host
        self.port = port
        self.is_connected= False

    def connect_mqtt(self):
        logging.info(f'MQTT Publisher connecting to: {self.host} port: {self.port}')

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT Broker!")
                self.is_connected = True
            else:
                logging.error("Failed to connect, return code %d\n", rc)
                self.is_connected = False

        self.client = mqtt_client.Client('mqtt_ros_message_forwarder')
        self.client.on_connect = on_connect
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    def publish(self, topic, message):
        self.client.publish(topic, json.dumps(message))
