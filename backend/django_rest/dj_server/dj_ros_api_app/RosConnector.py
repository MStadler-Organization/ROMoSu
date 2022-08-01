import logging

import roslibpy


class TopicInfo():
    def __init__(self, in_topic, type, out_topic='', period=0):
        self.in_topic = in_topic
        self.type = type


class RosConnector:
    """Central ROS connector class, connects to the ROS-bridge"""

    def get_topics(self):
        """Retrieves all ROS topics of the current configuration"""
        if not self.ROS_CLIENT or not self.ROS_CLIENT.is_connected:
            logging.error('ROS bridge is not connected properly!')
            return None

        topics = self.ROS_CLIENT.get_topics()
        topic_list = []
        for i, topic in enumerate(topics):
            rtype = self.ROS_CLIENT.get_topic_type(topic)
            topics = TopicInfo(topic, rtype)
            topic_list.append(topics)
        return topic_list

    def get_sums(self):
        """Retrieves all ROS topics of the current configuration"""
        if not self.ROS_CLIENT or not self.ROS_CLIENT.is_connected:
            logging.error('ROS bridge is not connected properly!')
            return None

        topics = self.ROS_CLIENT.get_topics()
        possible_sums = []
        for topic in topics:
            # remove preceding slash
            trunc_topic_name = topic[1:]
            # check if topic is a root-topic
            if trunc_topic_name.count('/') > 0:
                # no root-topic, get base topic
                trunc_topic_name = trunc_topic_name[:trunc_topic_name.index('/')]
            # check if already contained in list
            if trunc_topic_name not in possible_sums:
                possible_sums.append(trunc_topic_name)

        return possible_sums

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
