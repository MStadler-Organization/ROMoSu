import threading

from dj_server.dj_ros_api_app.InternalDBConnector import InternalDBConnector
from dj_server.dj_ros_api_app.models import MonitoringConfig
from dj_server.dj_ros_api_app.utils import singleton


def start_rt_monitoring(mon_config: MonitoringConfig):
    mon_config.sum_type_id
    pass


@singleton
class RuntimeMonitoringStarter:
    """Handles the active RT Monitoring instances"""

    def init_monitoring(self, runtime_config):
        # get saved monitoring config from runtime config id
        mon_config_qs = self.db_connector.get_rt_config_for_id(runtime_config['config_id'])

        # create new thread for
        threading.Timer(1, start_rt_monitoring, [mon_config_qs[0]]).start()
        # TODO: create required listeners on monitoring topic paths
        # self.get_sums()
        # TODO: forward messages in specified frequency and with required simplified or complex path (as it is or truncated to base topic)

    def __init__(self):
        self.active_rt_list = []
        self.db_connector = InternalDBConnector()
