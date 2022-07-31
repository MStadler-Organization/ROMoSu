from rest_framework import serializers

from dj_server.dj_ros_api_app.models import TopicList


class TopicListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TopicList
        fields = ('topiclist')
