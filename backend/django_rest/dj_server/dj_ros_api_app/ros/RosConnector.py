import logging

import roslibpy

from dj_server.dj_ros_api_app.helpers.object_classes import TopicInfo
from dj_server.dj_ros_api_app.helpers.utils import get_base_topic_string, get_sub_topic_string, singleton


@singleton
class RosConnector:
    """Central ROS connector class, connects to the ROS-bridge"""

    def get_sums(self):
        """Retrieves all ROS topics of the current configuration"""
        if not self.ROS_CLIENT or not self.ROS_CLIENT.is_connected:
            logging.error('ROS bridge is not connected properly!')
            return None

        topics = self.ROS_CLIENT.get_topics()
        possible_sums = []
        for topic in topics:
            base_topic = get_base_topic_string(topic)
            # check if already contained in list
            if base_topic not in possible_sums:
                possible_sums.append(base_topic)

        return possible_sums

    def get_properties_for_sum(self, p_selected_sum):
        """
        Collects properties based on selected SuM
        """

        # get all topics and sort them
        topics = self.ROS_CLIENT.get_topics()
        # sort ascending
        topics.sort()

        topic_list = []

        for topic in topics:
            # base topic name
            base_topic = get_base_topic_string(topic)
            # filter according to SuM and check if it is subtopic
            if base_topic == p_selected_sum and topic.count('/') > 1 and topic not in topic_list:
                # get details
                sub_topic_name = get_sub_topic_string(topic)
                topic_type = self.ROS_CLIENT.get_topic_type(topic)
                type_info = self.ROS_CLIENT.get_message_details(topic_type)
                # add to list
                topic_to_add = TopicInfo(sub_topic_name, topic_type, type_info)
                topic_list.append(topic_to_add)
        return topic_list

    def _connect_to_ros(self):
        """Connects to the roscore and returns the client if this was successful"""
        client = roslibpy.Ros(host='localhost', port=9090)  # TODO: change this here later with config
        client.run()
        if client.is_connected:
            logging.info('Successfully connected to ROS bridge')
            return client
        # something went wrong
        logging.warning('Could not connect to roscore with the rosbridge!')
        self.disconnect(client)

    def disconnect(self, client_to_disconnect=None):
        """Disconnects a given client from the rosbridge"""
        if client_to_disconnect:
            client_to_disconnect.terminate()
        else:
            self.ROS_CLIENT.terminate()
        logging.info('Disconnected from ROS bridge')

    def __init__(self) -> None:
        super().__init__()
        self.ROS_CLIENT = self._connect_to_ros()
