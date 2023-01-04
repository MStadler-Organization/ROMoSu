import json
import logging
import threading
from copy import copy
from typing import List

import roslibpy

from dj_server.dj_ros_api_app.helpers.InternalDBConnector import InternalDBConnector
from dj_server.dj_ros_api_app.helpers.mqtt_forwarder import MQTTForwarder
from dj_server.dj_ros_api_app.helpers.object_classes import RuntimeStarterRESTObject, RosTopicConfigObj, TopicInfo
from dj_server.dj_ros_api_app.helpers.utils import singleton, convert_to_json, ros_msg2json, convert_json_to_conf_obj, \
    NotFoundError, generate_unique_id, get_current_time, flatten_dict, add_prefix_to_dict, get_query_prefix, unflatten, \
    get_exact_current_time_in_millis
from dj_server.dj_ros_api_app.models import MonitoringConfig
from dj_server.dj_ros_api_app.ros.RosConnector import RosConnector
from dj_server.dj_ros_api_app.ros.RosListener import RosListener

ros_mon_data = {}
ros_listener = RosListener()
rc = RosConnector()
mqtt_forwarder = MQTTForwarder()
is_ros_data_initalized = False
COMPLETE_SAVE_TYPE = 'Complete (but complex)'
SIMPLE_SAVE_TYPE = 'Simple (but flattened)'


def get_list_of_checked_topics(topic_config_obj: RosTopicConfigObj, name_prefix: str):
    """Recursively parses the config for checked topics and returns the topic info as a list"""

    result_topic_list: [TopicInfo] = []

    # create qualified topic name to avoid name clashes
    complete_name = name_prefix + '/' + topic_config_obj.name

    if topic_config_obj.isChecked:
        # topic is selected -> add it to the list (subtopics will be covered automatically)
        result_topic_list.append(TopicInfo(complete_name, topic_config_obj.dataType, None))
        # check subtopics for selection
        if hasattr(topic_config_obj, 'children') and len(topic_config_obj.children) > 0:
            for child_topic in topic_config_obj.children:
                result_topic_list.extend(get_list_of_checked_topics(child_topic, complete_name))
    else:
        # topic is not selected, check if it has children and if any of the children are selected
        if hasattr(topic_config_obj, 'children') and len(topic_config_obj.children) > 0:
            for child_topic in topic_config_obj.children:
                result_topic_list.extend(get_list_of_checked_topics(child_topic, complete_name))
    return result_topic_list


def get_selected_topic_strings(conf_data: str, initial_prefix: str):
    """Parses a monitoring configuration for selected topics"""
    # convert string to dictionary
    config_as_json: str = convert_to_json(conf_data)
    config_as_dict: List[RosTopicConfigObj] = convert_json_to_conf_obj(config_as_json)

    # gather the selected topics to monitor
    list_of_topic_obj: [TopicInfo] = []
    for base_topic_obj in config_as_dict:
        checked_topics = get_list_of_checked_topics(base_topic_obj, initial_prefix)
        list_of_topic_obj.extend(checked_topics)
    return list_of_topic_obj


def update_ros_data(message, base_topic: str, sub_topic: TopicInfo):
    """The callback function of the ros listener, updates the global ros_mon_data variable"""
    time_in_millis_at_topic_arrival = get_exact_current_time_in_millis()
    global ros_mon_data
    # flatten dictionary
    flattened_dict = flatten_dict(message)
    # add base topic as prefix
    flattened_dict = add_prefix_to_dict(flattened_dict, f'{base_topic}${sub_topic.in_topic}$')
    # update values in ros_mon_data
    for key, value in flattened_dict.items():
        ros_mon_data[key] = value
        time_in_millis_after_cache = get_exact_current_time_in_millis()
        ros_mon_data[
            key] = time_in_millis_after_cache - time_in_millis_at_topic_arrival  # tim till cache todo: remove this


def monitor_topic(base_topic: str, sub_topic: TopicInfo, thread_event: threading.Event):
    """Starts a ROS topic subscription on a given topic"""

    if not ros_listener:
        logging.error(f'Got no ROS-Listener instance!')

    # create listener and callback if new data is received
    listener = roslibpy.Topic(ros_listener.ROS_CLIENT, base_topic + '/' + sub_topic.in_topic, sub_topic.type)
    listener.subscribe(lambda message: update_ros_data(message, base_topic, sub_topic))
    logging.info(f'Created subscriber on {sub_topic.in_topic}')

    while not thread_event.is_set():
        # loop for the listener
        pass


def get_current_ros_data(topic):
    """Gets the data of the global cached ros_mon_data var for a given (sub-)topic"""

    # transform topic name to name query prefix
    if isinstance(topic, TopicInfo):
        query_prefix_key = get_query_prefix(topic.in_topic)
    elif isinstance(topic, str):
        query_prefix_key = get_query_prefix(topic)
    else:
        logging.error(f'Cannot get data for topic: >{topic}<')
        return

    # local copy of global var
    local_ros_mon_data = ros_mon_data.copy()

    if query_prefix_key in local_ros_mon_data:
        # no nested element, return the value directly
        return local_ros_mon_data[query_prefix_key]

    # nested topic is wanted, get the subtopics
    result_dict = dict()
    # query all wanted data
    for key, value in local_ros_mon_data.items():
        if key.startswith(query_prefix_key):
            # this data is part of the result
            # remove unwanted prefixes to flatten the data correctly afterwards
            shortened_key = key[len(query_prefix_key) + 1:]
            result_dict[shortened_key] = value

    # unflatten dict for correct json serialization
    return unflatten(result_dict)


def get_mqtt_topic(topic: str, save_type: str):
    """Returns the mqtt topic based on the save type"""

    if save_type == COMPLETE_SAVE_TYPE:
        # use the complete topic hierarchy
        return topic
    elif save_type == SIMPLE_SAVE_TYPE:
        # use the flattened topic name
        hierarchy_list = topic.split('/')
        simple_topic = f'{hierarchy_list[0]}/{hierarchy_list[1]}/'
        if len(hierarchy_list) > 2:
            # more subtopics to come, use '#' as delimiter
            for idx in range(2, len(hierarchy_list)):
                simple_topic = f'{simple_topic}${hierarchy_list[idx]}'

        # remove first occurrence of $ as it would else be "/$"
        simple_topic = simple_topic.replace('$', '', 1)

        return simple_topic


def forward_message(topic: TopicInfo, seconds_to_wait: float, save_type: str, thread_event: threading.Event):
    """Forwards the topic via mqtt in a given frequency"""
    mqtt_topic = get_mqtt_topic(topic.in_topic, save_type)

    while not thread_event.is_set():
        time_before_access = get_exact_current_time_in_millis()
        data_to_publish = get_current_ros_data(topic)
        mqtt_forwarder.publish(mqtt_topic, ros_msg2json(data_to_publish), time_before_access)
        thread_event.wait(seconds_to_wait)


def get_frequencies(frequencies: str):
    """Converts the string of frequencies to an integer list"""
    im_result = frequencies.replace('[', '')
    im_result = im_result.replace(']', '')
    im_result = im_result.replace(' ', '')
    im_result = im_result.split(',')
    result = []

    for entry in im_result:
        result.append(float(entry))

    return result


def get_sec_lvl_topics(config: str):
    """Extracts the second level topics from a string monitoring config"""

    conf_as_dict = convert_json_to_conf_obj(config)
    result = []
    for sec_lvl_topic in conf_as_dict:
        result.append(sec_lvl_topic)
    return result


def get_frequency_for_topic(topic: TopicInfo, frequency_list, sec_lvl_topics_of_config):
    """Returns the specified frequency for a topic, frequency array of ints and a sec-level monitoring config list"""
    curr_idx = 0
    topic_hierarchy = topic.in_topic.split('/')
    for sec_lvl_topic in sec_lvl_topics_of_config:
        if sec_lvl_topic.name == topic_hierarchy[1]:
            # found the right topic in the config, this is the index in the frequency list
            return frequency_list[curr_idx]
        else:
            curr_idx = curr_idx + 1
    logging.error(f'Found no frequency for topic={topic.in_topic}')
    return -1


def get_topic_names_of_list(topic_list):
    """Returns the 'in_topic' elements of a TopicInfo list"""
    result = []
    for topic in topic_list:
        result.append({'name': topic.in_topic})
    return result


@singleton
class RuntimeMonitoringStarter:
    """Handles the active RT Monitoring instances"""

    def increase_base_topic_counter(self, prefix):
        """Increases the counter for the base_topic"""
        if not self.is_not_monitored(prefix):
            for conf in self.active_base_topic_list:
                if conf['base_topic'] == prefix:
                    conf['counter'] = conf['counter'] + 1

    def is_not_monitored(self, prefix):
        """
        Checks if another active monitoring config is already monitoring the base topic; :returns True,
        if it is not monitoring the prefix
        """
        for conf in self.active_base_topic_list:
            if conf['base_topic'] == prefix:
                return False
        return True

    def update_data_on_active_rt_list(self):
        """Updates the data in the active RT"""
        for conf in self.active_rt_list:
            for topic in conf['selected_topics']:
                topic['last_data'] = str(get_current_ros_data(topic['name']))

    def get_json_serializable_list(self):
        """Returns a list of all active rt-configs as a json-able object"""

        # load current data into the object
        self.update_data_on_active_rt_list()

        jsonable_list = []
        for conf in self.active_rt_list:
            jsonable_list.append(
                {'id': conf['id'],
                 'prefix': conf['prefix'],
                 'sum_type_id': conf['sum_type_id'],
                 'config_id': conf['config_id'],
                 'start_time': conf['start_time'],
                 'selected_topics': conf['selected_topics'],
                 'query_time': get_current_time()}
            )
        return jsonable_list

    def delete_active_config(self, id_to_delete: int):
        """Deletes a runtime monitoring instance"""
        for active_config in self.active_rt_list:
            if active_config['id'] == id_to_delete:
                self.stop_monitoring(active_config)
                self.active_rt_list.remove(active_config)
                del active_config['thread_event']
                return active_config
        raise NotFoundError

    def stop_monitoring(self, rt_config_to_stop):
        """Stops the monitoring for a given rt-config"""
        # stop the event to kill all the forwarding threads
        rt_config_to_stop['thread_event'].set()

        # check if this was also the last config for the base_topic
        for bt_obj in self.active_base_topic_list:
            if bt_obj['base_topic'] == rt_config_to_stop['prefix']:
                bt_obj['counter'] = bt_obj['counter'] - 1
                if bt_obj['counter'] <= 0:
                    bt_obj['thread_event'].set()
                    self.active_base_topic_list.remove(bt_obj)

    def add_topic_list_to_rt_data(self, topic_list, id):
        """adds the selected topics to the active runtime data object"""
        # search correct configurations
        for conf in self.active_rt_list:
            if conf['id'] == id:
                conf['selected_topics'] = get_topic_names_of_list(topic_list)

    def start_rt_monitoring(self, mon_config: MonitoringConfig, rt_starter: RuntimeStarterRESTObject, rc_id):
        """Starts the monitoring for a given monitoring config"""

        # check if root topic still exists
        curr_root_topic_list = rc.get_sums()
        if rt_starter.prefix not in curr_root_topic_list:
            logging.error(f'Target root-topic >{rt_starter.prefix}< is not available, aborting monitoring!')
            return

        # get wanted sub-topic-strings
        topic_list = get_selected_topic_strings(mon_config.ecore_data, rt_starter.prefix)
        self.add_topic_list_to_rt_data(topic_list, rc_id)

        # start monitoring of the base topic if it is not already monitored
        if self.is_not_monitored(rt_starter.prefix):
            simple_base_topic_name = rt_starter.prefix

            thread_event = threading.Event()

            # add the base topic
            self.active_base_topic_list.append(
                {'base_topic': rt_starter.prefix, 'counter': 1, 'thread_event': thread_event})

            # get the subtopics
            sub_topics = rc.get_properties_for_sum(simple_base_topic_name)
            # monitor the topics
            for topic in sub_topics:
                threading.Timer(1, monitor_topic, [simple_base_topic_name, topic, thread_event]).start()
        else:
            self.increase_base_topic_counter(rt_starter.prefix)

        # transform frequencies

        frequency_list = get_frequencies(mon_config.frequencies)
        # get the second level topics from the config to match the frequencies
        sec_lvl_topics_of_config = get_sec_lvl_topics(mon_config.ecore_data)
        # start a new thread for every topic to forward them accordingly
        for topic in topic_list:
            fq = get_frequency_for_topic(topic, frequency_list, sec_lvl_topics_of_config)
            threading.Timer(1, forward_message,
                            [topic, fq, mon_config.save_type, rt_starter.thread_event]).start()

    def init_monitoring(self, runtime_config):
        # add additional data
        runtime_config['id'] = generate_unique_id()
        runtime_config['start_time'] = get_current_time()
        runtime_config['thread_event'] = threading.Event()
        self.active_rt_list.append(runtime_config)

        # map into obj
        rt_starter_obj = RuntimeStarterRESTObject(runtime_config)

        # get saved monitoring config from runtime config id
        mon_config_qs = self.db_connector.get_rt_config_for_id(rt_starter_obj.config_id)

        # create json-serializable obj
        jsonable_obj = copy(rt_starter_obj)

        # publish metadata
        jsonable_obj.thread_event = ''
        mqtt_forwarder.publish(f'{rt_starter_obj.prefix}/meta', json.dumps(
            {
                'prefix': jsonable_obj.prefix,
                'sum_type_id': jsonable_obj.sum_type_id,
            }
        ))

        # start monitoring
        self.start_rt_monitoring(mon_config_qs[0], rt_starter_obj, runtime_config['id'])

        del jsonable_obj.thread_event
        return jsonable_obj

    def __init__(self):
        self.active_rt_list = []
        self.active_base_topic_list = []
        self.db_connector = InternalDBConnector()
