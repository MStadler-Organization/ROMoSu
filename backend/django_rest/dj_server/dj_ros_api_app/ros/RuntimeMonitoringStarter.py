import logging
import threading
from typing import List

import roslibpy

from dj_server.dj_ros_api_app.helpers.InternalDBConnector import InternalDBConnector
from dj_server.dj_ros_api_app.helpers.mqtt_forwarder import MQTTForwarder
from dj_server.dj_ros_api_app.helpers.object_classes import RuntimeStarterRESTObject, RosTopicConfigObj, TopicInfo
from dj_server.dj_ros_api_app.helpers.utils import singleton, convert_to_json
from dj_server.dj_ros_api_app.models import MonitoringConfig
from dj_server.dj_ros_api_app.ros.RosConnector import RosConnector

global ros_mon_data


def get_list_of_checked_topics(topic_config_obj: RosTopicConfigObj, name_prefix: str):
    """Recursively parses the config for checked topics and retruns the topic info as a list"""

    result_topic_list: [TopicInfo] = []

    # create qualified topic name to avoid name clashes
    complete_name = name_prefix + '/' + topic_config_obj.name

    if topic_config_obj.isChecked:
        # topic is selected -> add it to the list (subtopics will be covered automatically)
        result_topic_list.append(TopicInfo(complete_name, topic_config_obj.dataType, None))

    else:
        # topic is not selected, check if it has children and if any of the children are selected
        if hasattr(topic_config_obj, 'children') and len(topic_config_obj.children) > 0:
            for child_topic in topic_config_obj.children:
                result_topic_list.extend(get_list_of_checked_topics(child_topic, complete_name))
    return result_topic_list


def get_selected_topic_strings(conf_data: str, initial_prefix: str):
    # convert string to dictionary
    config_as_dict: List[RosTopicConfigObj] = convert_to_json(conf_data)

    # gather the selected topics to monitor
    list_of_topic_obj: [TopicInfo] = []
    for base_topic_obj in config_as_dict:
        checked_topics = get_list_of_checked_topics(base_topic_obj, initial_prefix)
        list_of_topic_obj.extend(checked_topics)
    return list_of_topic_obj


def update_ros_data(message, base_topic: str, sub_topic: TopicInfo):
    global ros_mon_data
    base_topic_data = getattr(ros_mon_data, base_topic)

    setattr(getattr(getattr(ros_mon_data, base_topic), sub_topic.in_topic[:-1]), )
    # TODO: update the data in ros_mon_data in the correct location in tree


def monitor_topic(base_topic: str, sub_topic_list: [TopicInfo]):
    ros_connector: RosConnector = RosConnector()

    for sub_topic in sub_topic_list:
        # create entry in global var for subtopic
        setattr(getattr(ros_mon_data, base_topic), sub_topic.in_topic[:-1], [])
        # create listener and callback if new data is received
        listener = roslibpy.Topic(ros_connector.ROS_CLIENT, sub_topic_list.in_topic, sub_topic_list.type)
        listener.subscribe(lambda message: update_ros_data(message['data'], base_topic, sub_topic))

    while True:
        # loop for the listener
        # TODO: change this to an event which is canceled once the RT is done for the base topic
        pass


def start_rt_monitoring(mon_config: MonitoringConfig, rt_starter: RuntimeStarterRESTObject):
    global ros_mon_data
    rc = RosConnector()

    # check if root topic still exists
    curr_root_topic_list = rc.get_sums()
    if rt_starter.prefix not in curr_root_topic_list:
        logging.error(f'Target root-topic >{rt_starter.prefix}< is not available, aborting monitoring!')
        return

    # get wanted sub-topic-strings
    topic_list = get_selected_topic_strings(mon_config.ecore_data, rt_starter.prefix)

    # start monitoring of the base topic if it is not already monitored
    simple_base_topic_name = rt_starter.prefix[:-1]
    if not hasattr(ros_mon_data, simple_base_topic_name):
        # create new placeholder attribute in global var
        setattr(ros_mon_data, simple_base_topic_name, [])
        # get the subtopics
        sub_topics = rc.get_properties_for_sum(simple_base_topic_name)
        # monitor the topics
        threading.Timer(1, monitor_topic, [simple_base_topic_name, sub_topics]).start()

    # start a new thread for the every topic to forward them accordingly
    for idx, topic in enumerate(topic_list):
        # TODO change the method call here to a mqtt publish loop
        # threading.Timer(1, monitor_topic, [idx, topic, mon_config]).start()
        pass

    mqtt_forwarder: MQTTForwarder = MQTTForwarder()
    mqtt_forwarder.publish('a_simple_topic', 'testmessage')
    # TODO: forward messages in specified frequency and with required simplified or complex path (as it is or truncated to base topic)


@singleton
class RuntimeMonitoringStarter:
    """Handles the active RT Monitoring instances"""

    def init_monitoring(self, runtime_config):
        # map into obj
        rt_starter_obj = RuntimeStarterRESTObject(runtime_config)

        # get saved monitoring config from runtime config id
        mon_config_qs = self.db_connector.get_rt_config_for_id(rt_starter_obj.config_id)

        # create new thread for
        threading.Timer(1, start_rt_monitoring, [mon_config_qs[0], rt_starter_obj]).start()

    def __init__(self):
        self.active_rt_list = []
        self.db_connector = InternalDBConnector()
