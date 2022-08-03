# Create your views here.
import logging

from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from dj_server.dj_ros_api_app.apps import DjRosApiAppConfig
from dj_server.dj_ros_api_app.models import SuMType
from dj_server.dj_ros_api_app.serializers import SuMTypeSerializer
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
            return Response('Invalid params, check documentation!', status=status.HTTP_400_BAD_REQUEST)

        # get properties for given SuM
        props = DjRosApiAppConfig.RC.get_properties_for_sum(p_sum)

        return JsonResponse(props, encoder=DefaultEncoder, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
def sum_types(request):
    """
    Get/Post/Delete SuM types
    """

    if request.method == 'GET':
        # return all objects contained in db
        sum_types = SuMType.objects.all()
        serializer = SuMTypeSerializer(sum_types, many=True)
        return JsonResponse(serializer.data, encoder=DefaultEncoder, safe=False)

    elif request.method == 'POST':
        # parse request body
        sum_type_data = JSONParser().parse(request)
        serializer = SuMTypeSerializer(data=sum_type_data)
        # check form of request data and save it
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        #  check if object exists
        try:
            sum_type_to_delete = SuMType.objects.get(id=request.query_params.get('id'))
        except SuMType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # delete it
        serializer = SuMTypeSerializer(sum_type_to_delete, many=False)
        sum_type_to_delete.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
