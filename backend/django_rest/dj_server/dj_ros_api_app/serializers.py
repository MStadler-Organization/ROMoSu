from rest_framework import serializers

from dj_server.dj_ros_api_app.models import TopicList, SuMType


class TopicListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TopicList
        fields = ('topiclist',)


class SuMTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SuMType
        fields = ('id','name')
