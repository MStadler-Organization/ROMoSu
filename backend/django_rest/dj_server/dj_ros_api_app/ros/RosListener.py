import logging

import roslibpy

from dj_server.dj_ros_api_app.helpers.utils import Singleton


class RosListener(metaclass=Singleton):
    """ROS listener class, used only to listen on ros nodes"""

    def _connect_to_ros(self):
        """Connects to the roscore and returns the client if this was successful"""
        client = roslibpy.Ros(host='localhost', port=9090)  # TODO: change this here later with config
        client.run()
        if client.is_connected:
            logging.info('Successfully connected to ROS bridge from listener')
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
