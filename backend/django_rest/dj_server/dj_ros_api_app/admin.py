from django.contrib import admin

# Register your models here.
from dj_server.dj_ros_api_app.models import TopicList, SuMType, MonitoringConfig, ActiveRuntimeConfig

admin.site.register(TopicList)
admin.site.register(SuMType)
admin.site.register(MonitoringConfig)
admin.site.register(ActiveRuntimeConfig)
