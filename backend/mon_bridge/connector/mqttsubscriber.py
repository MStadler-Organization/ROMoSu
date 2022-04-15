import logging

from paho.mqtt import client as mqtt_client
import json


class MQTTSubscriber:
    def __init__(self, host, message_handler, port=1883):
        self.host = host
        self.port = port
        self.message_handler = message_handler

    def on_message_callback(self, client, userdata, message):
        self.message_handler(message.timestamp, message.topic, json.loads(message.payload))

    def connect_mqtt(self):
        logging.info(f'MQTT Monitoring Subscriber connecting to: {self.host} port: {self.port}')

        def connect_callback(client, userdata, flags, rc):
            if rc == 0:
                logging.info("MQTT Monitoring Subscriber connected to MQTT Broker!")
            else:
                logging.info("Failed to connect, return code %d\n", rc)

        self.client = mqtt_client.Client('mqtt-monitoring-subscriber')
        # client.username_pw_set(username, password)
        self.client.on_connect = connect_callback
        self.client.on_message = self.on_message_callback
        self.client.connect(self.host, self.port)
        self.client.loop_start()
        self.client.subscribe('#')
        self.client.subscribe('abc/asd')
