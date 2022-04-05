import time
from collections import deque

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from connector.mqttsubscriber import MQTTSubscriber


class TabMonitoring():

    def __init__(self, parent_dialog):
        self.parent_dialog = parent_dialog
        self.data = []

    def activate_monitoring(self, dialog):
        self.parent_dialog.tree_monitoring.setEnabled(True)
        self.mqtt_subscriber = MQTTSubscriber(self.parent_dialog.monitoring_config.mqtt_host, self.new_message)
        self.mqtt_subscriber.connect_mqtt()

    def new_message(self, timestamp, topic, message):
            self.data.insert(0, [timestamp, topic, message])
            self.tbl_model = QStandardItemModel()
            self.tbl_model.setHorizontalHeaderLabels(['Timestamp', 'Message'])
            self.parent_dialog.tree_monitoring.header().setDefaultSectionSize(250)
            self.parent_dialog.tree_monitoring.setModel(self.tbl_model)
            self.import_data(self.data[:20])
            self.parent_dialog.tree_monitoring.expandAll()
            self.parent_dialog.tree_monitoring.resizeColumnToContents(1)

    def import_data(self, data, root=None):
        self.tbl_model.setRowCount(0)
        if root is None:
            root = self.tbl_model.invisibleRootItem()
        seen = {}
        values = deque(data)
        while values:
            value = values.popleft()
            if value[1] not in seen:
                parent = root
                topic_item = QStandardItem(value[1])
                parent.appendRow([topic_item])
                seen[value[1]] = topic_item
            else:
                topic_item = seen[value[1]]

            msg_item = QStandardItem(str(value[2]))
            topic_item.appendRow([
                QStandardItem(time.ctime(value[0])),
                msg_item
            ])
            topic_item.child(parent.rowCount() - 1)
