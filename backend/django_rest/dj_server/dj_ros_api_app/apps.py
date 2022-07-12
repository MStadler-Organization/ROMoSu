from django.apps import AppConfig

from dj_server.dj_ros_mon_app.ros_mon.RosConnector import RosConnector


class DjRosApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dj_server.dj_ros_api_app'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        RosConnector()


