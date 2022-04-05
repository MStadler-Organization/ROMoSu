import importlib
import logging
import threading

import roslibpy



def resolve_type(name):
    components  = name.replace('/','.')
    components = components.split('.')
    components.insert( -1,'msg')
    print(components)
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def resolve_type_name(name):
    components  = name.replace('/','.')
    components = components.split('.')
    components.insert( -1,'msg')
    l_mod = importlib.import_module('.'.join(components[:-1]))
    klass = getattr(l_mod, str(components[-1]))
    return klass


class DynamicSubscriber():
    def __init__(self,topic_name,topic_type,interval,out_topic, ros_bridge, mqtt_forwarder):
        self.topic_name = topic_name
        self.out_topic = out_topic
        self.topic_type = topic_type
        self.interval = interval
        self.ros_bridge = ros_bridge
        self.mqtt_forwarder=mqtt_forwarder
        self.pill2kill = threading.Event()
        self.thread = threading.Thread(target=self.publish_to_mqtt, args=(self.pill2kill, ))
        self.data=None


    def set_data(self, message):
        self.data = message
        if 'header' in self.data:
            del self.data['header']

    def subscribe(self):
        logging.info(f'subscribing to:{self.topic_name} [{self.topic_type}] --> out_topic: {self.out_topic}')
        self.listener = roslibpy.Topic(self.ros_bridge, self.topic_name, self.topic_type)
        self.listener.subscribe(self.set_data)
        self.thread.start()

    def  set_interval(self,interval):
        self.interval=interval

    def msg2json(self,msg):
       # y = yaml.load(str(msg))
       # return json.dumps(y,indent=4)
        #json_str = json_message_converter.convert_ros_message_to_json(msg)
        #print(json_str)
        return msg

    def unsubscribe(self):
        #self.s.unregister()
        self.listener.unsubscribe()
        self.pill2kill.set()
        self.thread.join()

    #### needs to be thread safe!!!
    def publish_to_mqtt(self,stop_event):
        while not stop_event.wait(self.interval):
            if self.data is None:
                pass
                #self.mqtt_forwarder.publish(self.topic_name+'/'+'error',{'message': 'no data received'})
            else:
                self.mqtt_forwarder.publish(self.out_topic,self.msg2json(self.data))
                self.data=None

    def callback(self,data):
        #print('new value')
        self.data = data
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)


