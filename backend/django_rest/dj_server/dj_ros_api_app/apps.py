from django.apps import AppConfig

from dj_server.dj_ros_api_app.helpers.utils import setup


class DjRosApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dj_server.dj_ros_api_app'

    setup()

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
