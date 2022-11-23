#!/usr/bin/env python

import json
import time

import rospy
import yaml


def make_ros_log(msg):
    rospy.loginfo(time.ctime() + ' -- ' + msg + '\n\n')


def get_current_milli_time():
    return str(round(time.time() * 1000))


# Convert a ROS message to JSON format
def ros_msg2json(msg):
    y = yaml.safe_load(str(msg))
    return json.dumps(y, indent=4)
