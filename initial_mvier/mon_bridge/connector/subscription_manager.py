import logging
import time

from roslibpy import Ros

from connector.dynamic_subscriber import DynamicSubscriber
from connector.mqttforwarder import MQTTForwarder


class Topic_Info():
    def __init__(self, in_topic, type, out_topic='', period=0):
        self.in_topic = in_topic
        self.type = type
        self.out_topic = out_topic
        self.period = period


class SubscriptionManager(object):
    _instance = None
    subscriber_list = {}

    ros = None

    def __new__(cls, monitoring_config):
        if cls._instance is None:
            # print('Creating the object')
            cls._instance = super(SubscriptionManager, cls).__new__(cls)
            SubscriptionManager.monitoring_config = monitoring_config
            SubscriptionManager.mqtt_forwarder = MQTTForwarder(SubscriptionManager.monitoring_config.mqtt_host)
        return cls._instance

    @staticmethod
    def connect():
        if SubscriptionManager.mqtt_forwarder.is_connected:
            logging.info('MQTT already connected')
        else:
            SubscriptionManager.mqtt_forwarder.connect_mqtt()
        if SubscriptionManager.ros is not None and SubscriptionManager.ros.is_connected:
            logging.info('Already connected!')
            return
        logging.info(
            f'ROS-Bridge connecting to: {SubscriptionManager.monitoring_config.ros_bridge_host} port: {SubscriptionManager.monitoring_config.ros_bridge_port}')
        SubscriptionManager.ros = Ros(SubscriptionManager.monitoring_config.ros_bridge_host,
                                      SubscriptionManager.monitoring_config.ros_bridge_port)
        SubscriptionManager.ros.run()

        if SubscriptionManager.ros.is_connected:
            logging.info('ROS Bridge successfully connected')
        time.sleep(0.5)

    @staticmethod
    def subscribe(topic, type, interval, out_topic=None):
        if out_topic is None:
            out_topic = topic
        if SubscriptionManager.is_subscribed(topic):
            ds = SubscriptionManager.subscriber_list[topic]
            ds.set_interval(interval)
            ds.set_outtopic(out_topic)
        else:
            ds = DynamicSubscriber(topic, type, interval, out_topic, SubscriptionManager.ros,
                                   SubscriptionManager.mqtt_forwarder)
            ds.subscribe()
            SubscriptionManager.subscriber_list[topic] = ds

    @staticmethod
    def unsubscribe(topic):
        if topic in SubscriptionManager.subscriber_list:
            ds = SubscriptionManager.subscriber_list[topic]
            ds.unsubscribe()
            SubscriptionManager.subscriber_list.pop(topic)
        else:
            print(f'Not subscribed to {topic}')

    def is_subscribed(topic):
        return topic in SubscriptionManager.subscriber_list

    def get_topics(self):
        if not SubscriptionManager.ros.is_connected:
            print('not connected!')
            return None

        tp = SubscriptionManager.ros.get_topics()
        topic_list = []
        for i, topic in enumerate(tp):
            rtype = self.ros.get_topic_type(topic)
            tp = Topic_Info(topic, rtype)
            topic_list.append(tp)
        return topic_list
