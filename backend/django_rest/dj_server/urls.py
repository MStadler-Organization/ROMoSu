"""dj_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from dj_server.dj_ros_api_app import views

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('possible-sums/', views.possible_sums),
    path('props-for-sum/', views.properties_for_sum),
    path('sum-types/', views.sum_types),
    path('sum-types/<int:pk>', views.sum_types),
    path('config-file/', views.mon_config),
    path('config-file/<int:pk>', views.mon_config),
    path('runtime-config/', views.runtime_config),
]
