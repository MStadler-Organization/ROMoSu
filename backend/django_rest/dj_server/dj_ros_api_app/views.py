# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from dj_server.dj_ros_mon_app.ros_mon.RosConnector import RosConnector


@csrf_exempt
def current_topic_list(request):
    """
    Get current topic list
    """
    if request.method == 'GET':
        print('###########IN GET METHOD###########')
        rc = RosConnector()
        print('########### RC INSTANCE CREATED ###########')
        topics = rc.get_topics()
        print('########### GOT TOPICS ###########')
        rc.disconnect()
        print(topics)
        # topic_json = json.dumps(topics, default=lambda x: x.__dict__)
        # topic_json = json.dumps(topics, default=lambda o: o.encode())
        # TODO: dump this here correctly. JSONresponse provides respective params for serialization
        return JsonResponse(, safe=False)
