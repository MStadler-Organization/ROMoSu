import time

from roslibpy import Ros
from monitoring_topic_ui import TopicSelector
from connector.subscription_manager import SubscriptionManager

host = 'mv-x1'
port = 9090
url = u'ws://%s:%d' % (host, port)

def cb(tl):
    print('topic received!')
    tops = tl['topics']
    types = tl['types']
    for i,topic in enumerate(tops):
        print(f'TOPIC: {topic} --> {types[i]}')

def connect():
    global ros
    ros = Ros(host, port)
    ros.run()

    if ros.is_connected:
        print("ROS initially connected")
    time.sleep(0.5)
    # event = threading.Event()
    # ros.on('close', lambda m: event.set())
    # ros.close()
    # event.wait(5)
    tp = ros.get_topics()#cb)

    #time.sleep(30)
    global topic_list
    topic_list = []
    #tops = tp['topics']
    #types = tp['types']
    for i,topic in enumerate(tp):
        type = ros.get_topic_type(topic)
        topic_list.append([topic,type])
        print(f'TOPIC: {topic} --> {type}')




# def hdl(m):
#     print(m)
#
# def run_thread(count):
#     print('register logger')
#     service = roslibpy.Service(ros, '/rosout/get_loggers', 'roscpp/GetLoggers')
#     request = roslibpy.ServiceRequest()
#
#     print('Calling service...')
#     result = service.call(request)
#     print('Service response: {}'.format(result['loggers']))
#
# import threading


if __name__ == '__main__':
    connect()
    sel = TopicSelector(topic_list)
    SubscriptionManager.connect()

    #thread = threading.Thread(target = run_thread, args = (10, ))
    #thread.start()
    sel.show_selector()


