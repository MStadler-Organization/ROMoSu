import time

from roslibpy import Ros


class ROSBridge_Connector():

    def __init__(self, host, port = 9090):
        self.host = host
        self.port = port

    def connect(self):
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print(f'Connect to: {self.host} port: {self.port}')
        self.ros = Ros(self.host, self.port)
        self.ros.run()
        if self.ros.is_connected:
            print("ROS initially connected")
        time.sleep(0.5)


    def get_topics(self):
        if not self.ros.is_connected:
            print('not connected!')
            return None

        tp = self.ros.get_topics()
        topic_list = []
        for i,topic in enumerate(tp):
            type = self.ros.get_topic_type(topic)
            #topic_list.append([topic,type])
            tp = Topic_Info(topic,type)
            topic_list.append(tp)
            print(f'TOPIC: {topic} --> {type}')
        return topic_list
