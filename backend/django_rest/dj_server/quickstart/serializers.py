from django.contrib.auth.models import User, Group
from rest_framework import serializers

from dj_server.quickstart.models import Hero


class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ('name', 'alias')
