from rest_framework import serializers

from dj_server.dj_ros_api_app.models import TopicList, SuMType, MonitoringConfig


class TopicListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TopicList
        fields = ('topiclist',)


class SuMTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SuMType
        fields = ('id', 'name')


class MonitoringConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MonitoringConfig
        fields = ('id',
                  'name',
                  'frequencies',
                  'save_type',
                  'sum_type_id',
                  'ecore_data')
