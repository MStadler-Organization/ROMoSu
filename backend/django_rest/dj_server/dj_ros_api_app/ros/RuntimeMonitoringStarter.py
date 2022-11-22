import logging
import threading
from typing import List

from dj_server.dj_ros_api_app.helpers.InternalDBConnector import InternalDBConnector
from dj_server.dj_ros_api_app.helpers.object_classes import RuntimeStarterRESTObject, RosTopicConfigObj, TopicInfo
from dj_server.dj_ros_api_app.helpers.utils import singleton, convert_to_json
from dj_server.dj_ros_api_app.models import MonitoringConfig
from dj_server.dj_ros_api_app.ros.RosConnector import RosConnector


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


def start_rt_monitoring(mon_config: MonitoringConfig, rt_starter: RuntimeStarterRESTObject):
    rc = RosConnector()

    # check if root topic still exists
    curr_root_topic_list = rc.get_sums()
    if rt_starter.prefix not in curr_root_topic_list:
        logging.error(f'Target root-topic >{rt_starter.prefix}< is not available, aborting monitoring!')

    # get wanted sub-topic-strings
    topic_list = get_selected_topic_strings(mon_config.ecore_data, rt_starter.prefix)

    # TODO: now monitor these topics with the rosbridge in a new thread
    print(len(topic_list))

    for entry in topic_list:
        print(entry)


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
        # TODO: create required listeners on monitoring topic paths
        # self.get_sums()
        # TODO: forward messages in specified frequency and with required simplified or complex path (as it is or truncated to base topic)

    def __init__(self):
        self.active_rt_list = []
        self.db_connector = InternalDBConnector()
