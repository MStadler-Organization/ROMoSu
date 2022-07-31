# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from dj_server.dj_ros_api_app.apps import DjRosApiAppConfig
from dj_server.dj_ros_api_app.utils import DefaultEncoder


@csrf_exempt
def current_topic_list(request):
    """
    Get current topic list
    """
    if request.method == 'GET':
        # get all ROS topics
        topics = DjRosApiAppConfig.RC.get_topics()
        return JsonResponse(topics, encoder=DefaultEncoder, safe=False)
