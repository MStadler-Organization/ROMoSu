#!/usr/bin/env python

import math
import os
import sys
import threading
import time

import rospy
from actionlib_msgs.msg import GoalStatusArray, GoalStatus
from diagnostic_msgs.msg import DiagnosticArray
from geometry_msgs.msg import Twist, Point
from move_base_msgs.msg import MoveBaseActionResult, MoveBaseActionGoal
from nav_msgs.msg import Odometry
from sensor_msgs.msg import BatteryState, JointState, MagneticField, LaserScan
from turtlebot3_msgs.msg import VersionInfo, SensorState

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from mqtt_forwarder import MQTTForwarder

global mqtt_client_pub_local, has_rotated, is_in_first_rotation, is_on_mission, is_outside_of_home_zone, is_goal_reached, initial_pose, target_mission_pose, is_pickup_complete, is_target_area_entered, is_back_in_home_zone

BatteryStatus_data = {'data': BatteryState()}
Velocity_data = {'data': Twist()}
Diagnostics_data = {'data': DiagnosticArray()}
JointState_data = {'data': JointState()}
MagneticField_data = {'data': MagneticField()}
VersionInfo_data = {'data': VersionInfo()}
Odometry_data = {'data': Odometry()}
SensorState_data = {'data': SensorState()}
LaserScan_data = {'data': LaserScan()}

NA = '(n/a)'
TRIGGER_TOPIC_STRING = 'SuM/trigger'
last_odom_pos = NA
current_mission_id = NA

# ################################################## CONFIG ###################################################
# radius in meter, can be adjusted according to circumstances,
# e.g., 1 means the home-zone is a 1 meter radius
HOME_ZONE_RADIUS = 0.5
TARGET_ZONE_RADIUS = 0.5
# time in seconds until pickup is done after target reached
SECONDS_WAITING_FOR_PICKUP = 10


# ################################################# CONFIG END ################################################

# For later matching the DSL property name is hardcoded here in the pattern *propertyname*_data without suffix


def version_info_callback(data):
    global mqtt_client_pub_local
    try:
        if VersionInfo_data['data'] == VersionInfo():
            # trigger 'activate' because first time received this message
            mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'activate', False)
            print('NEW TRIGGER: activate')
        VersionInfo_data['data'] = data
    except Exception as e:
        print(e)


def battery_state_callback(data):
    try:
        BatteryStatus_data['data'] = data
    except Exception as e:
        print(e)


def set_initial_pose():
    global Odometry_data, initial_pose
    odom_data = Odometry_data['data']
    initial_pose = odom_data.pose.pose.position


def cmd_vel_callback(data):
    global has_rotated, mqtt_client_pub_local, is_in_first_rotation, is_on_mission, is_goal_reached, is_pickup_complete
    try:
        rotation = data.angular.z
        speed = data.linear.x
        if not has_rotated and abs(rotation) > 0:
            # has rotated for the first time -> trigger 'start_calibration'
            has_rotated = True
            is_in_first_rotation = True
            mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'start_calibration', False)
            print('NEW TRIGGER: start_calibration')
        elif is_in_first_rotation and rotation == 0:
            # has stopped rotating for the first time -> trigger 'calibration finished'
            is_in_first_rotation = False
            mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'calibration_finished', False)
            print('NEW TRIGGER: calibration_finished')

            # set init pose
            set_initial_pose()
        elif is_on_mission and is_goal_reached and (abs(speed) or abs(rotation) > 0) and not is_pickup_complete:
            # moving again after reached the goal -> returning to home
            mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'pickup_complete', False)
            print('NEW TRIGGER: pickup_complete')
            is_pickup_complete = True

        Velocity_data['data'] = data
    except Exception as e:
        print(e)


def diagnostic_callback(data):
    try:
        Diagnostics_data['data'] = data
    except Exception as e:
        print(e)


def joint_state_callback(data):
    try:
        JointState_data['data'] = data
    except Exception as e:
        print(e)


def magnetic_field_callback(data):
    try:
        MagneticField_data['data'] = data
    except Exception as e:
        print(e)


def odometry_callback(data: Odometry):
    global last_odom_pos, is_outside_of_home_zone, mqtt_client_pub_local, initial_pose, initial_pose, target_mission_pose, is_target_area_entered, is_back_in_home_zone
    try:
        Odometry_data['data'] = data
        if is_on_mission:
            current_pose = data.pose.pose.position
            distance_from_start = calculate_distance(current_pose, initial_pose)
            # check if distance is outside of HOME_ZONE and the trigger was not already sent
            if distance_from_start > HOME_ZONE_RADIUS and not is_outside_of_home_zone:
                # bot is outside of home zone -> send trigger
                is_outside_of_home_zone = True
                mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'leaving_home', False)
                print('NEW TRIGGER: leaving_home')
            elif distance_from_start <= HOME_ZONE_RADIUS and is_outside_of_home_zone:
                # bot is back in home zone
                is_outside_of_home_zone = False
                mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'entering_home', False)
                print('NEW TRIGGER: entering_home')
                is_back_in_home_zone = True
            elif target_mission_pose.x != 0 and target_mission_pose.y != 0 and not is_target_area_entered:
                distance_to_goal: float = calculate_distance(current_pose, target_mission_pose)
                if distance_to_goal <= TARGET_ZONE_RADIUS:
                    mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'entering_target_area', False)
                    print('NEW TRIGGER: entering_target_area')
                    is_target_area_entered = True

    except Exception as e:
        print(e)


def calculate_distance(new_position: Point, old_position: Point):
    # Calculate the distance between two Points (positions)
    x2 = new_position.x
    x1 = old_position.x
    y2 = new_position.y
    y1 = old_position.y
    dist = math.hypot(x2 - x1, y2 - y1)
    return dist


def sensor_state_callback(data):
    try:
        SensorState_data['data'] = data
    except Exception as e:
        print(e)


def laser_scan_callback(data):
    try:
        LaserScan_data['data'] = data
    except Exception as e:
        print(e)


def move_base_status_callback(data: GoalStatusArray):
    global mqtt_client_pub_local, is_on_mission, current_mission_id, is_goal_reached
    try:
        if len(data.status_list) > 0:
            last_goal: GoalStatus = data.status_list[-1]
            # check if the goal is a new one
            # check if the goal can be reached and the robot is not already on a mission,
            # e.g. not navigating back to the home-zone
            if (last_goal.goal_id.id != current_mission_id) and (last_goal.status == GoalStatus.ACTIVE) and (
                    not is_on_mission):
                is_on_mission = True
                # reset target var
                is_goal_reached = False
                current_mission_id = last_goal.goal_id.id
                mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'mission_started', False)
                print('NEW TRIGGER: mission_started')

    except Exception as e:
        print(e)


def move_base_result_callback(data: MoveBaseActionResult):
    global mqtt_client_pub_local, is_on_mission, current_mission_id, is_goal_reached, is_back_in_home_zone, is_pickup_complete, is_target_area_entered
    # get the current result
    current_result: GoalStatus = data.status
    try:
        # check if the result refers to the current mission goal
        # check if goal was reached successful
        if current_result.goal_id.id == current_mission_id and current_result.status == GoalStatus.SUCCEEDED and not is_goal_reached:
            # goal reached send trigger
            is_goal_reached = True
            mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'target_reached', False)
            print('NEW TRIGGER: target_reached')
            threading.Timer(1, wait_for_pickup).start()
        elif is_back_in_home_zone and current_result.status == GoalStatus.SUCCEEDED and is_on_mission:
            # finished the mission
            mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'mission_finished', False)
            print('NEW TRIGGER: mission_finished')
            # reset mission vars
            is_on_mission = False
            is_back_in_home_zone = False
            is_pickup_complete = False
            is_target_area_entered = False
            set_initial_pose()

    except Exception as e:
        print(e)


def wait_for_pickup():
    global mqtt_client_pub_local
    time.sleep(SECONDS_WAITING_FOR_PICKUP)
    mqtt_client_pub_local.publish(TRIGGER_TOPIC_STRING, 'ready_for_pickup', False)
    print('NEW TRIGGER: ready_for_pickup')


def move_base_goal_callback(data: MoveBaseActionGoal):
    global target_mission_pose
    travel_pose = data.goal.target_pose.pose.position
    current_pose = Odometry_data['data'].pose.pose.position
    # set the target pose to calculate the distance to the target later
    target_mission_pose = Point(x=(travel_pose.x + current_pose.x), y=(travel_pose.y + current_pose.y))


def listener():
    print('Starting data collector')
    # set globals
    global mqtt_client_pub_local, has_rotated, is_in_first_rotation, is_on_mission, is_outside_of_home_zone, is_goal_reached, initial_pose, BatteryStatus_data, Velocity_data, Diagnostics_data, JointState_data, MagneticField_data, VersionInfo_data, Odometry_data, SensorState_data, LaserScan_data, target_mission_pose, is_pickup_complete, is_target_area_entered, is_back_in_home_zone
    mqtt_client_pub_local = MQTTForwarder()
    has_rotated = False
    is_in_first_rotation = False
    is_on_mission = False
    is_outside_of_home_zone = False
    is_goal_reached = False
    initial_pose = Point(x=0, y=0)
    target_mission_pose = Point(x=0, y=0)
    is_pickup_complete = False
    is_target_area_entered = False
    is_back_in_home_zone = False

    # init listener node
    rospy.init_node('turtle_listener', anonymous=True)

    # specify subscriber topics
    # turtlebot topics
    rospy.Subscriber('battery_state', BatteryState, battery_state_callback)
    rospy.Subscriber('cmd_vel', Twist, cmd_vel_callback)
    rospy.Subscriber('diagwnostics', DiagnosticArray, diagnostic_callback)
    rospy.Subscriber('joint_states', JointState, joint_state_callback)
    rospy.Subscriber('magnetic_field', MagneticField, magnetic_field_callback)
    rospy.Subscriber('version_info', VersionInfo, version_info_callback)
    rospy.Subscriber('sensor_state', SensorState, sensor_state_callback)
    rospy.Subscriber('odom', Odometry, odometry_callback)
    rospy.Subscriber('scan', LaserScan, laser_scan_callback)
    # navigation topic
    rospy.Subscriber('move_base/status', GoalStatusArray, move_base_status_callback)
    rospy.Subscriber('move_base/result', MoveBaseActionResult, move_base_result_callback)
    rospy.Subscriber('move_base/goal', MoveBaseActionGoal, move_base_goal_callback)

    try:
        while True:
            # loop
            pass
    except KeyboardInterrupt:
        print('interrupted!')
