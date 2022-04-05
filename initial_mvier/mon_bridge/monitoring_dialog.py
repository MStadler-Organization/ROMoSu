import logging
import sys

from PyQt5 import QtWidgets

from config.monitoring_config import Monitoring_Config, MonitoringConfigRunner
from connector.subscription_manager import SubscriptionManager
from designer.monitoring_ui import Ui_Monitoring
from ui import tab_topicselect
from ui.tab_monitoring import TabMonitoring
from ui.tab_topicselect import TableModel


class MonitoringApplication(QtWidgets.QMainWindow, Ui_Monitoring):
    def __init__(self):
        super().__init__()
        self.monitoring_config = Monitoring_Config()
        self.read_config()
        self.data = []
        self.setupUi(self)

    def read_config(self):
        self.loader = MonitoringConfigRunner()
        self.loader.load_config()
        self.monitoring_config = self.loader.mon_config

    def retrieve_topics(self):
        self.monitoring_config.ros_bridge_host = self.lineEdit.text()
        self.monitoring_config.mqtt_host = self.lineEdit_2.text()
        self.loader.save_config()
        self.ros_bridge = SubscriptionManager(self.monitoring_config)
        self.ros_bridge.connect()
        topics = self.ros_bridge.get_topics()
        # print(topics)
        self.tblmodel = TableModel(topics)
        self.tbl_topics.setModel(self.tblmodel)

    def set_monitoring(self):
        index = self.tbl_topics.selectedIndexes()
        chngd_topic = self.tblmodel.get_topic(index[0].row())
        tab_topicselect.select_topic(chngd_topic)

    def initialize(self):
        self.tab_monitoring = TabMonitoring(self)
        self.tbl_topics.setHorizontalHeaderLabels(['ROS-Topic', 'Datatype', 'Forward-Topic', 'Period'])
        self.btn_retrieve.clicked.connect(self.retrieve_topics)
        self.tbl_topics.doubleClicked.connect(self.set_monitoring)
        self.btn_monitor.clicked.connect(self.tab_monitoring.activate_monitoring)
        self.tree_monitoring.setEnabled(False)
        self.lineEdit.setText(self.monitoring_config.ros_bridge_host)
        self.lineEdit_2.setText(self.monitoring_config.mqtt_host)


def main():
    global app;
    # FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
    logging.basicConfig(level='INFO',
                        format='%(asctime)s: %(name)10s - %(levelname)s - %(message)60s - {%(filename)s:%(lineno)d}',
                        datefmt='%d-%m-%y %H:%M:%S')

    # logging.Formatter("[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)", "%Y-%m-%d %H:%M:%S")

    app = QtWidgets.QApplication(sys.argv)
    window = MonitoringApplication()
    window.show()
    window.initialize()
    app.exec_()


if __name__ == '__main__':
    main()
