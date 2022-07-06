from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import permissions

from dj_server.quickstart.models import Hero
from dj_server.quickstart.serializers import HeroSerializer


class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer


@csrf_exempt
def hero_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        heroes = Hero.objects.all()
        serializer = HeroSerializer(heroes, many=True)
        return JsonResponse(serializer.data, safe=False)
