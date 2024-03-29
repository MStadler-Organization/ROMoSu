# Create your views here.
import json
import logging

from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from dj_server.dj_ros_api_app.helpers.utils import DefaultEncoder, NotFoundError, convert_to_json
from dj_server.dj_ros_api_app.models import SuMType, MonitoringConfig
from dj_server.dj_ros_api_app.ros.RosConnector import RosConnector
from dj_server.dj_ros_api_app.ros.RuntimeMonitoringStarter import RuntimeMonitoringStarter
from dj_server.dj_ros_api_app.serializers import SuMTypeSerializer, MonitoringConfigSerializer, \
    ActiveRuntimeConfigSerializer


@csrf_exempt
def possible_sums(request):
    """
    Get current topic list
    """
    if request.method == 'GET':
        # get all possible SuMs
        rc = RosConnector()
        sums = rc.get_sums()
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
        rc = RosConnector()
        props = rc.get_properties_for_sum(p_sum)

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


@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def mon_config(request):
    """Create and get new config files"""
    if request.method == 'GET':
        if request.query_params.get('sum_type'):
            # return only the one with the sum_type
            #  check if object exists
            try:
                configs_to_return = MonitoringConfig.objects.filter(sum_type_id=request.query_params.get('sum_type'))
                if not configs_to_return:
                    raise NotFoundError
            except (SuMType.DoesNotExist, NotFoundError):
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = MonitoringConfigSerializer(configs_to_return, many=True)
            return JsonResponse(serializer.data, encoder=DefaultEncoder, safe=False)

        else:
            # return all objects contained in db
            mon_configs = MonitoringConfig.objects.all()
            serializer = MonitoringConfigSerializer(mon_configs, many=True)
            return JsonResponse(serializer.data, encoder=DefaultEncoder, safe=False)

    if request.method == 'POST':
        # parse request body
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        # create new object and save it to DB

        if body and body['configFileData'] and body['configFileData']['name'] and body['configFileData'][
            'ecore_data'] and \
                body['configFileData']['save_type'] and body['configFileData']['sum_type_id'] and \
                body['configFileData'][
                    'frequencies']:
            temp_obj = MonitoringConfig()
            temp_obj.name = body['configFileData']['name']
            temp_obj.save_type = body['configFileData']['save_type']
            temp_obj.sum_type_id = body['configFileData']['sum_type_id']
            temp_obj.frequencies = str(body['configFileData']['frequencies'])
            temp_obj.ecore_data = convert_to_json(str(body['configFileData']['ecore_data']))
            temp_obj.save()

            return Response(data='Successfully created new config!', status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        # delete the config
        # check if object exists
        try:
            config_to_delete = MonitoringConfig.objects.get(id=request.query_params.get('id'))
        except MonitoringConfig.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # delete it
        serializer = MonitoringConfigSerializer(config_to_delete, many=False)
        config_to_delete.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        config_to_patch = MonitoringConfig.objects.get(id=request.query_params.get('id'))

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        serializer = MonitoringConfigSerializer(config_to_patch, data=body,
                                                partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response('Invalid params!', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def runtime_config(request):
    rt_starter: RuntimeMonitoringStarter = RuntimeMonitoringStarter()

    if request.method == 'GET':
        # return all objects contained in db
        return JsonResponse(encoder=DefaultEncoder, data=rt_starter.get_json_serializable_list(),
                            status=status.HTTP_200_OK, safe=False)

    if request.method == 'POST':
        # parse request body
        request_config_data = JSONParser().parse(request)
        serializer = ActiveRuntimeConfigSerializer(data=request_config_data['pRTConfig'])
        # check form of request data and save it
        if serializer.is_valid():
            rt_data = rt_starter.init_monitoring(serializer.data)
            return JsonResponse(encoder=DefaultEncoder, data=rt_data, status=status.HTTP_201_CREATED, safe=False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        # delete the config and stop the monitoring
        # check if object exists
        try:
            # check if exists and deletes it
            id_to_delete = request.query_params.get('id')
            deleted_config = rt_starter.delete_active_config(id_to_delete)
        except NotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(deleted_config, status=status.HTTP_200_OK)
