# Create your views here.
import logging

from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from dj_server.dj_ros_api_app.apps import DjRosApiAppConfig
from dj_server.dj_ros_api_app.utils import DefaultEncoder


@csrf_exempt
def possible_sums(request):
    """
    Get current topic list
    """
    if request.method == 'GET':
        # get all possible SuMs
        sums = DjRosApiAppConfig.RC.get_sums()
        return JsonResponse(sums, encoder=DefaultEncoder, safe=False)


@csrf_exempt
def properties_for_sum(request):
    """
    Get properties for given SuM
    """
    if request.method == 'GET':
        # get sum param from request
        try:
            p_sum = request.GET['sum']
        except MultiValueDictKeyError:
            logging.warning('used invalid query param')
            return HttpResponseBadRequest('Invalid params, check documentation!')

        # get properties for given SuM
        props = DjRosApiAppConfig.RC.get_properties_for_sum(p_sum)

        return JsonResponse(props, encoder=DefaultEncoder, safe=False)
