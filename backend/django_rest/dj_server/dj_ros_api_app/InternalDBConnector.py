from dj_server.dj_ros_api_app.models import MonitoringConfig
from dj_server.dj_ros_api_app.utils import NotFoundError


class InternalDBConnector:

    def get_rt_config_for_id(self, id_to_find):
        """
        Gets a Monitoring config for a given ID
        returns NotFoundError if no Config was found
        """

        result = MonitoringConfig.objects.filter(id=id_to_find)
        if not result:
            raise NotFoundError
        return result
