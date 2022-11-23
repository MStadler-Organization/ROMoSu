from django.db.models import QuerySet

from dj_server.dj_ros_api_app.helpers.utils import NotFoundError
from dj_server.dj_ros_api_app.models import MonitoringConfig


def is_valid_single_queryset(queryset_to_test: QuerySet):
    """Checks if the queryset contains only a single result"""
    if queryset_to_test.count() != 1: return False
    return True


class InternalDBConnector:

    def get_rt_config_for_id(self, id_to_find):
        """
        Gets a Monitoring config for a given ID
        returns NotFoundError if no Config was found
        """

        result = MonitoringConfig.objects.filter(id=id_to_find)
        if not result or not is_valid_single_queryset(result):
            raise NotFoundError
        return result
