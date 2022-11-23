#!/usr/bin/env python

import os
import sys
import time

from paho.mqtt import client as mqtt_client

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

# settings
LOCAL_MQTT_IP = 'localhost'
CENTRAL_MQTT_IP = 'ms-web-developer.de'

global local_mqtt_client_id, CENTRAL_MQTT_CLIENT_ID, sm_mqtt_client_id


def get_local_mqtt_client_id():
    global local_mqtt_client_id
    return local_mqtt_client_id


def get_sm_mqtt_client_id():
    global sm_mqtt_client_id
    return sm_mqtt_client_id


def _set_globals():
    global local_mqtt_client_id, CENTRAL_MQTT_CLIENT_ID, sm_mqtt_client_id
    time_in_milli = get_current_milli_time()

    local_mqtt_client_id = f'local-mqtt-{time_in_milli}'

    CENTRAL_MQTT_CLIENT_ID = f'central-mqtt-{time_in_milli}'

    sm_mqtt_client_id = f'sm-mqtt-{time_in_milli}'


def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d \n ", rc)


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
        print('local mqtt is set up')

    def publish_local(self, topic, message):
        self.client.publish(topic, str(message))


class _MQTTForwarderCentral:

    def __init__(self):
        self.connect_central_mqtt()

    def connect_central_mqtt(self):
        global CENTRAL_MQTT_CLIENT_ID
        # Set Connecting Client ID
        client = mqtt_client.Client(CENTRAL_MQTT_CLIENT_ID)
        client.username_pw_set('marco', 'XuXQlBbBGdOyJiplRIvV')
        client.on_connect = _on_connect
        client.connect(CENTRAL_MQTT_IP, 8883)
        self.client = client
        print('central mqtt is set up')

    def publish_central(self, topic, message):
        self.client.publish(topic, str(message))


class MQTTForwarder:
    def __init__(self):
        print('Generating new MQTT Forwarder')
        _set_globals()
        self.mqtt_local_client = _MQTTForwarderLocal()
        self.mqtt_central_client = _MQTTForwarderCentral()

    def publish(self, topic, message, is_central_flag):
        if is_central_flag:
            self.mqtt_central_client.publish_central(topic, message)
        else:
            self.mqtt_local_client.publish_local(topic, message)
