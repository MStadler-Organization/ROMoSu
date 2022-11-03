#!/usr/bin/env python

import os
import sys

import paho.mqtt.client as mqtt

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from mqtt_forwarder import LOCAL_MQTT_IP, get_sm_mqtt_client_id
from data_collector import *
from utils import ros_msg2json, make_ros_log

global mqtt_forwarder_obj, sm_mqtt_sub_client, BatteryStatus_config_event, Velocity_config_event, Diagnostics_config_event, JointState_config_event, MagneticField_config_event, VersionInfo_config_event, Odometry_config_event, SensorState_config_event, LaserScan_config_event

BatteryStatus_config_obj = {
    'frequency': 99999.0,
    'is_central_scope': False,
    'is_thread_running': False
}


def handle_BatteryStatus_data():
    global mqtt_forwarder_obj, BatteryStatus_config_event

    BatteryStatus_config_event = threading.Event()
    BatteryStatus_config_obj['is_thread_running'] = True

    while not BatteryStatus_config_event.is_set():
        data = BatteryStatus_data['data']
        msg = ros_msg2json(data)

        # forward msg
        mqtt_forwarder_obj.publish('BatteryStatus', msg, BatteryStatus_config_obj['is_central_scope'])
        # wait according to config
        BatteryStatus_config_event.wait(BatteryStatus_config_obj['frequency'])

    BatteryStatus_config_obj['is_thread_running'] = False


Velocity_config_obj = {
    'frequency': 99999.0,
    'is_central_scope': False,
    'is_thread_running': False
}


def handle_Velocity_data():
    global mqtt_forwarder_obj, Velocity_config_event

    Velocity_config_event = threading.Event()
    Velocity_config_obj['is_thread_running'] = True

    while not Velocity_config_event.is_set():
        data = Velocity_data['data']
        msg = ros_msg2json(data)

        # forward msg
        mqtt_forwarder_obj.publish('Velocity', msg, Velocity_config_obj['is_central_scope'])
        # wait according to config
        Velocity_config_event.wait(Velocity_config_obj['frequency'])

    Velocity_config_obj['is_thread_running'] = False


Diagnostics_config_obj = {
    'frequency': 99999.0,
    'is_central_scope': False,
    'is_thread_running': False
}


def handle_Diagnostics_data():
    global mqtt_forwarder_obj, Diagnostics_config_event

    Diagnostics_config_event = threading.Event()
    Diagnostics_config_obj['is_thread_running'] = True

    while not Diagnostics_config_event.is_set():
        data = Diagnostics_data['data']
        msg = ros_msg2json(data)

        # forward msg
        mqtt_forwarder_obj.publish('Diagnostics', msg, Diagnostics_config_obj['is_central_scope'])
        # wait according to config
        Diagnostics_config_event.wait(Diagnostics_config_obj['frequency'])

    Diagnostics_config_obj['is_thread_running'] = False


JointState_config_obj = {
    'frequency': 99999.0,
    'is_central_scope': False,
    'is_thread_running': False
}


def handle_JointState_data():
    global mqtt_forwarder_obj, JointState_config_event

    JointState_config_event = threading.Event()
    JointState_config_obj['is_thread_running'] = True

    while not JointState_config_event.is_set():
        data = JointState_data['data']
        msg = ros_msg2json(data)

        # forward msg
        mqtt_forwarder_obj.publish('JointState', msg, JointState_config_obj['is_central_scope'])
        # wait according to config
        JointState_config_event.wait(JointState_config_obj['frequency'])

    JointState_config_obj['is_thread_running'] = False


MagneticField_config_obj = {
    'frequency': 99999.0,
    'is_central_scope': False,
    'is_thread_running': False
}


def handle_MagneticField_data():
    global mqtt_forwarder_obj, MagneticField_config_event

    MagneticField_config_event = threading.Event()
    MagneticField_config_obj['is_thread_running'] = True

    while not MagneticField_config_event.is_set():
        data = MagneticField_data['data']
        msg = ros_msg2json(data)

        # forward msg
        mqtt_forwarder_obj.publish('MagneticField', msg, MagneticField_config_obj['is_central_scope'])
        # wait according to config
        MagneticField_config_event.wait(MagneticField_config_obj['frequency'])

    MagneticField_config_obj['is_thread_running'] = False


VersionInfo_config_obj = {
    'frequency': 99999.0,
    'is_central_scope': False,
    'is_thread_running': False
}


def handle_VersionInfo_data():
    global mqtt_forwarder_obj, VersionInfo_config_event

    VersionInfo_config_event = threading.Event()
    VersionInfo_config_obj['is_thread_running'] = True

    while not VersionInfo_config_event.is_set():
        data = VersionInfo_data['data']
        msg = ros_msg2json(data)

        # forward msg
        mqtt_forwarder_obj.publish('VersionInfo', msg, VersionInfo_config_obj['is_central_scope'])
        # wait according to config
        VersionInfo_config_event.wait(VersionInfo_config_obj['frequency'])

    VersionInfo_config_obj['is_thread_running'] = False


Odometry_config_obj = {
    'frequency': 99999.0,
    'is_central_scope': False,
    'is_thread_running': False
}


def handle_Odometry_data():
    global mqtt_forwarder_obj, Odometry_config_event

    Odometry_config_event = threading.Event()
    Odometry_config_obj['is_thread_running'] = True

    while not Odometry_config_event.is_set():
        data = Odometry_data['data']
        msg = ros_msg2json(data)

        # forward msg
        mqtt_forwarder_obj.publish('Odometry', msg, Odometry_config_obj['is_central_scope'])
        # wait according to config
        Odometry_config_event.wait(Odometry_config_obj['frequency'])

    Odometry_config_obj['is_thread_running'] = False


SensorState_config_obj = {
    'frequency': 99999.0,
    'is_central_scope': False,
    'is_thread_running': False
}


def handle_SensorState_data():
    global mqtt_forwarder_obj, SensorState_config_event

    SensorState_config_event = threading.Event()
    SensorState_config_obj['is_thread_running'] = True

    while not SensorState_config_event.is_set():
        data = SensorState_data['data']
        msg = ros_msg2json(data)

        # forward msg
        mqtt_forwarder_obj.publish('SensorState', msg, SensorState_config_obj['is_central_scope'])
        # wait according to config
        SensorState_config_event.wait(SensorState_config_obj['frequency'])

    SensorState_config_obj['is_thread_running'] = False


LaserScan_config_obj = {
    'frequency': 99999.0,
    'is_central_scope': False,
    'is_thread_running': False
}


def handle_LaserScan_data():
    global mqtt_forwarder_obj, LaserScan_config_event

    LaserScan_config_event = threading.Event()
    LaserScan_config_obj['is_thread_running'] = True

    while not LaserScan_config_event.is_set():
        data = LaserScan_data['data']
        msg = ros_msg2json(data)

        # forward msg
        mqtt_forwarder_obj.publish('LaserScan', msg, LaserScan_config_obj['is_central_scope'])
        # wait according to config
        LaserScan_config_event.wait(LaserScan_config_obj['frequency'])

    LaserScan_config_obj['is_thread_running'] = False


def switch_to_state(state):
    global mqtt_forwarder_obj, BatteryStatus_config_event, Velocity_config_event, Diagnostics_config_event, JointState_config_event, MagneticField_config_event, VersionInfo_config_event, Odometry_config_event, SensorState_config_event, LaserScan_config_event

    temp_BatteryStatus_config_obj = BatteryStatus_config_obj.copy()
    temp_Velocity_config_obj = Velocity_config_obj.copy()
    temp_Diagnostics_config_obj = Diagnostics_config_obj.copy()
    temp_JointState_config_obj = JointState_config_obj.copy()
    temp_MagneticField_config_obj = MagneticField_config_obj.copy()
    temp_VersionInfo_config_obj = VersionInfo_config_obj.copy()
    temp_Odometry_config_obj = Odometry_config_obj.copy()
    temp_SensorState_config_obj = SensorState_config_obj.copy()
    temp_LaserScan_config_obj = LaserScan_config_obj.copy()

    match state:
        case 'active':
            BatteryStatus_config_obj['frequency'] = 1
            BatteryStatus_config_obj['is_central_scope'] = True
            Velocity_config_obj['frequency'] = 5
            Velocity_config_obj['is_central_scope'] = True
            Diagnostics_config_obj['frequency'] = 1
            Diagnostics_config_obj['is_central_scope'] = True
            JointState_config_obj['frequency'] = 5
            JointState_config_obj['is_central_scope'] = True
            MagneticField_config_obj['frequency'] = 5
            MagneticField_config_obj['is_central_scope'] = True
            VersionInfo_config_obj['frequency'] = 3
            VersionInfo_config_obj['is_central_scope'] = True
            Odometry_config_obj['frequency'] = 5
            Odometry_config_obj['is_central_scope'] = True
            SensorState_config_obj['frequency'] = 5
            SensorState_config_obj['is_central_scope'] = True
            LaserScan_config_obj['frequency'] = 5
            LaserScan_config_obj['is_central_scope'] = True
        case 'calibrating':
            BatteryStatus_config_obj['frequency'] = 5
            BatteryStatus_config_obj['is_central_scope'] = False
            Diagnostics_config_obj['frequency'] = 10
            Diagnostics_config_obj['is_central_scope'] = False
            Velocity_config_obj['frequency'] = 1
            Velocity_config_obj['is_central_scope'] = True
            JointState_config_obj['frequency'] = 5
            JointState_config_obj['is_central_scope'] = False
            MagneticField_config_obj['frequency'] = 1
            MagneticField_config_obj['is_central_scope'] = True
            VersionInfo_config_obj['frequency'] = 10
            VersionInfo_config_obj['is_central_scope'] = False
            Odometry_config_obj['frequency'] = 1
            Odometry_config_obj['is_central_scope'] = True
            SensorState_config_obj['frequency'] = 1
            SensorState_config_obj['is_central_scope'] = True
            LaserScan_config_obj['frequency'] = 1
            LaserScan_config_obj['is_central_scope'] = True
        case 'ready':
            BatteryStatus_config_obj['frequency'] = 5
            BatteryStatus_config_obj['is_central_scope'] = False
            Velocity_config_obj['frequency'] = 1
            Velocity_config_obj['is_central_scope'] = True
            JointState_config_obj['frequency'] = 5
            JointState_config_obj['is_central_scope'] = False
            Diagnostics_config_obj['frequency'] = 1
            Diagnostics_config_obj['is_central_scope'] = True
            MagneticField_config_obj['frequency'] = 5
            MagneticField_config_obj['is_central_scope'] = False
            VersionInfo_config_obj['frequency'] = 5
            VersionInfo_config_obj['is_central_scope'] = False
            Odometry_config_obj['frequency'] = 5
            Odometry_config_obj['is_central_scope'] = False
            SensorState_config_obj['frequency'] = 5
            SensorState_config_obj['is_central_scope'] = False
            LaserScan_config_obj['frequency'] = 5
            LaserScan_config_obj['is_central_scope'] = False
        case 'in_home_zone':
            BatteryStatus_config_obj['frequency'] = 3
            BatteryStatus_config_obj['is_central_scope'] = False
            Velocity_config_obj['frequency'] = 2
            Velocity_config_obj['is_central_scope'] = True
            JointState_config_obj['frequency'] = 2
            JointState_config_obj['is_central_scope'] = False
            Diagnostics_config_obj['frequency'] = 10
            Diagnostics_config_obj['is_central_scope'] = True
            MagneticField_config_obj['frequency'] = 10
            MagneticField_config_obj['is_central_scope'] = False
            VersionInfo_config_obj['frequency'] = 10
            VersionInfo_config_obj['is_central_scope'] = False
            Odometry_config_obj['frequency'] = 1
            Odometry_config_obj['is_central_scope'] = True
            SensorState_config_obj['frequency'] = 10
            SensorState_config_obj['is_central_scope'] = False
            LaserScan_config_obj['frequency'] = 10
            LaserScan_config_obj['is_central_scope'] = False
        case 'travelling_to_target_location':
            BatteryStatus_config_obj['frequency'] = 2
            BatteryStatus_config_obj['is_central_scope'] = True
            Velocity_config_obj['frequency'] = 1
            Velocity_config_obj['is_central_scope'] = True
            JointState_config_obj['frequency'] = 1
            JointState_config_obj['is_central_scope'] = True
            Diagnostics_config_obj['frequency'] = 5
            Diagnostics_config_obj['is_central_scope'] = True
            MagneticField_config_obj['frequency'] = 10
            MagneticField_config_obj['is_central_scope'] = False
            VersionInfo_config_obj['frequency'] = 10
            VersionInfo_config_obj['is_central_scope'] = False
            Odometry_config_obj['frequency'] = 1
            Odometry_config_obj['is_central_scope'] = True
            SensorState_config_obj['frequency'] = 10
            SensorState_config_obj['is_central_scope'] = False
            LaserScan_config_obj['frequency'] = 1
            LaserScan_config_obj['is_central_scope'] = True
        case 'enter_target_zone':
            BatteryStatus_config_obj['frequency'] = 5
            BatteryStatus_config_obj['is_central_scope'] = True
            Velocity_config_obj['frequency'] = 2
            Velocity_config_obj['is_central_scope'] = True
            JointState_config_obj['frequency'] = 5
            JointState_config_obj['is_central_scope'] = True
            Diagnostics_config_obj['frequency'] = 5
            Diagnostics_config_obj['is_central_scope'] = True
            MagneticField_config_obj['frequency'] = 5
            MagneticField_config_obj['is_central_scope'] = False
            VersionInfo_config_obj['frequency'] = 2
            VersionInfo_config_obj['is_central_scope'] = False
            Odometry_config_obj['frequency'] = 1
            Odometry_config_obj['is_central_scope'] = True
            SensorState_config_obj['frequency'] = 5
            SensorState_config_obj['is_central_scope'] = False
            LaserScan_config_obj['frequency'] = 1
            LaserScan_config_obj['is_central_scope'] = True
        case 'target_location_reached':
            BatteryStatus_config_obj['frequency'] = 5
            BatteryStatus_config_obj['is_central_scope'] = False
            Velocity_config_obj['frequency'] = 5
            Velocity_config_obj['is_central_scope'] = False
            JointState_config_obj['frequency'] = 2
            JointState_config_obj['is_central_scope'] = True
            MagneticField_config_obj['frequency'] = 10
            MagneticField_config_obj['is_central_scope'] = False
            VersionInfo_config_obj['frequency'] = 10
            VersionInfo_config_obj['is_central_scope'] = False
            Diagnostics_config_obj['frequency'] = 2
            Diagnostics_config_obj['is_central_scope'] = True
            Odometry_config_obj['frequency'] = 5
            Odometry_config_obj['is_central_scope'] = False
            SensorState_config_obj['frequency'] = 5
            SensorState_config_obj['is_central_scope'] = False
            LaserScan_config_obj['frequency'] = 5
            LaserScan_config_obj['is_central_scope'] = False
        case 'waiting_for_pickup':
            BatteryStatus_config_obj['frequency'] = 10
            BatteryStatus_config_obj['is_central_scope'] = False
            Velocity_config_obj['frequency'] = 10
            Velocity_config_obj['is_central_scope'] = False
            JointState_config_obj['frequency'] = 10
            JointState_config_obj['is_central_scope'] = False
            Diagnostics_config_obj['frequency'] = 10
            Diagnostics_config_obj['is_central_scope'] = False
            MagneticField_config_obj['frequency'] = 10
            MagneticField_config_obj['is_central_scope'] = False
            VersionInfo_config_obj['frequency'] = 10
            VersionInfo_config_obj['is_central_scope'] = False
            Odometry_config_obj['frequency'] = 1
            Odometry_config_obj['is_central_scope'] = True
            SensorState_config_obj['frequency'] = 1
            SensorState_config_obj['is_central_scope'] = True
            LaserScan_config_obj['frequency'] = 1
            LaserScan_config_obj['is_central_scope'] = True
        case 'return_to_home_location':
            BatteryStatus_config_obj['frequency'] = 2
            BatteryStatus_config_obj['is_central_scope'] = True
            Velocity_config_obj['frequency'] = 1
            Velocity_config_obj['is_central_scope'] = True
            JointState_config_obj['frequency'] = 1
            JointState_config_obj['is_central_scope'] = True
            Diagnostics_config_obj['frequency'] = 1
            Diagnostics_config_obj['is_central_scope'] = True
            MagneticField_config_obj['frequency'] = 2
            MagneticField_config_obj['is_central_scope'] = False
            Odometry_config_obj['frequency'] = 1
            Odometry_config_obj['is_central_scope'] = True
            SensorState_config_obj['frequency'] = 1
            SensorState_config_obj['is_central_scope'] = True
            VersionInfo_config_obj['frequency'] = 5
            VersionInfo_config_obj['is_central_scope'] = False
            LaserScan_config_obj['frequency'] = 1
            LaserScan_config_obj['is_central_scope'] = True
        case 'battery':
            BatteryStatus_config_obj['frequency'] = 1
            BatteryStatus_config_obj['is_central_scope'] = True
            Velocity_config_obj['frequency'] = 5
            Velocity_config_obj['is_central_scope'] = True
            JointState_config_obj['frequency'] = 99999.0
            Diagnostics_config_obj['frequency'] = 5
            Diagnostics_config_obj['is_central_scope'] = True
            MagneticField_config_obj['frequency'] = 99999.0
            VersionInfo_config_obj['frequency'] = 99999.0
            Odometry_config_obj['frequency'] = 99999.0
            SensorState_config_obj['frequency'] = 99999.0
            LaserScan_config_obj['frequency'] = 99999.0
        case 'diagnostic':
            BatteryStatus_config_obj['frequency'] = 1
            BatteryStatus_config_obj['is_central_scope'] = True
            Velocity_config_obj['frequency'] = 1
            Velocity_config_obj['is_central_scope'] = True
            JointState_config_obj['frequency'] = 1
            JointState_config_obj['is_central_scope'] = True
            Diagnostics_config_obj['frequency'] = 1
            Diagnostics_config_obj['is_central_scope'] = True
            MagneticField_config_obj['frequency'] = 1
            MagneticField_config_obj['is_central_scope'] = True
            VersionInfo_config_obj['frequency'] = 3
            VersionInfo_config_obj['is_central_scope'] = True
            Odometry_config_obj['frequency'] = 1
            Odometry_config_obj['is_central_scope'] = True
            SensorState_config_obj['frequency'] = 1
            SensorState_config_obj['is_central_scope'] = True
            LaserScan_config_obj['frequency'] = 1
            LaserScan_config_obj['is_central_scope'] = True

    if temp_BatteryStatus_config_obj != BatteryStatus_config_obj:
        BatteryStatus_config_event.set()
        while not BatteryStatus_config_obj['is_thread_running']:
            # wait for thread to shut down
            pass
        # start new thread
        threading.Timer(1, handle_BatteryStatus_data).start()

    if temp_Velocity_config_obj != Velocity_config_obj:
        Velocity_config_event.set()
        while not Velocity_config_obj['is_thread_running']:
            # wait for thread to shut down
            pass
        # start new thread
        threading.Timer(1, handle_Velocity_data).start()

    if temp_Diagnostics_config_obj != Diagnostics_config_obj:
        Diagnostics_config_event.set()
        while not Diagnostics_config_obj['is_thread_running']:
            # wait for thread to shut down
            pass
        # start new thread
        threading.Timer(1, handle_Diagnostics_data).start()

    if temp_JointState_config_obj != JointState_config_obj:
        JointState_config_event.set()
        while not JointState_config_obj['is_thread_running']:
            # wait for thread to shut down
            pass
        # start new thread
        threading.Timer(1, handle_JointState_data).start()

    if temp_MagneticField_config_obj != MagneticField_config_obj:
        MagneticField_config_event.set()
        while not MagneticField_config_obj['is_thread_running']:
            # wait for thread to shut down
            pass
        # start new thread
        threading.Timer(1, handle_MagneticField_data).start()

    if temp_VersionInfo_config_obj != VersionInfo_config_obj:
        VersionInfo_config_event.set()
        while not VersionInfo_config_obj['is_thread_running']:
            # wait for thread to shut down
            pass
        # start new thread
        threading.Timer(1, handle_VersionInfo_data).start()

    if temp_Odometry_config_obj != Odometry_config_obj:
        Odometry_config_event.set()
        while not Odometry_config_obj['is_thread_running']:
            # wait for thread to shut down
            pass
        # start new thread
        threading.Timer(1, handle_Odometry_data).start()

    if temp_SensorState_config_obj != SensorState_config_obj:
        SensorState_config_event.set()
        while not SensorState_config_obj['is_thread_running']:
            # wait for thread to shut down
            pass
        # start new thread
        threading.Timer(1, handle_SensorState_data).start()

    if temp_LaserScan_config_obj != LaserScan_config_obj:
        LaserScan_config_event.set()
        while not LaserScan_config_obj['is_thread_running']:
            # wait for thread to shut down
            pass
        # start new thread
        threading.Timer(1, handle_LaserScan_data).start()


def on_sm_message(client, userdata, message):
    new_state = str(message.payload.decode("utf-8"))
    make_ros_log('received new state from statemachine: ' + new_state)
    switch_to_state(new_state)


def spin_mqtt():
    global sm_mqtt_sub_client
    sm_mqtt_sub_client.loop_forever()


def main():
    global mqtt_forwarder_obj, sm_mqtt_sub_client
    mqtt_forwarder_obj = MQTTForwarder()

    # call threads for the topics
    threading.Timer(1, handle_BatteryStatus_data).start()
    threading.Timer(1, handle_Velocity_data).start()
    threading.Timer(1, handle_Diagnostics_data).start()
    threading.Timer(1, handle_JointState_data).start()
    threading.Timer(1, handle_MagneticField_data).start()
    threading.Timer(1, handle_VersionInfo_data).start()
    threading.Timer(1, handle_Odometry_data).start()
    threading.Timer(1, handle_SensorState_data).start()
    threading.Timer(1, handle_LaserScan_data).start()

    # create subscriber to statemachine
    sm_mqtt_sub_client = mqtt.Client(get_sm_mqtt_client_id() + str(round(time.time() * 1000)))
    sm_mqtt_sub_client.connect(LOCAL_MQTT_IP, 1883)
    sm_mqtt_sub_client.subscribe('statemachine/new_state')
    sm_mqtt_sub_client.on_message = on_sm_message

    threading.Timer(1, spin_mqtt).start()

    # call data_collector
    listener()


if __name__ == '__main__':
    main()
