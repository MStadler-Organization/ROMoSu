import json
import os

CONFIG_PATH = 'config/conf.json'

class Monitoring_Config():

    def __init__(self,ros_bridge_host=None, ros_bridge_port=9090, mqtt_host=None, mqtt_port=None):
        self.ros_bridge_host = ros_bridge_host
        self.ros_bridge_port= ros_bridge_port
        self.mqtt_host=mqtt_host
        self.mqtt_port = mqtt_port



class MonitoringConfigRunner:
    def __init__(self):
        self.mon_config = Monitoring_Config()

    def save_config(self):
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.mon_config.__dict__, f, indent=3)

    def load_config(self):
        if not os.path.isfile(CONFIG_PATH):
            with open(CONFIG_PATH, 'w') as f:
                json.dump(Monitoring_Config().__dict__, f, indent=3)
        with open(CONFIG_PATH) as f:
            self.mon_config = Monitoring_Config(**json.load(f))
