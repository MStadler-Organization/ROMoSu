#!/usr/bin/env python
import logging
import os
import sys
import time

from paho.mqtt import client as mqtt_client

from dj_server.dj_ros_api_app.helpers.utils import singleton

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

# settings
LOCAL_MQTT_IP = 'localhost'

global local_mqtt_client_id


def _set_globals():
    global local_mqtt_client_id
    time_in_milli = get_current_milli_time()
    local_mqtt_client_id = f'local-mqtt-{time_in_milli}'


def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker!")
    else:
        logging.error("Failed to connect, return code %d \n ", rc)


def get_current_milli_time():
    return str(round(time.time() * 1000))


class _MQTTForwarderLocal:

    def __init__(self):
        self.connect_local_mqtt()

    def connect_local_mqtt(self):
        global local_mqtt_client_id
        # Set Connecting Client ID
        client = mqtt_client.Client(local_mqtt_client_id)
        client.on_connect = _on_connect
        client.connect(LOCAL_MQTT_IP, 1883)
        self.client = client
        logging.info('local mqtt is set up')

    def publish_local(self, topic, message):
        self.client.publish(topic, str(message))


@singleton
class MQTTForwarder:
    def __init__(self):
        logging.info('Generating new MQTT Forwarder')
        _set_globals()
        self.mqtt_local_client = _MQTTForwarderLocal()

    def publish(self, topic, message):
        self.mqtt_local_client.publish_local(topic, message)
