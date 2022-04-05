from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
import logging

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from connector.subscription_manager import SubscriptionManager
from ui.ui_util import *

HEADER_LABELS = ['ROS-Topic', 'DataType', 'Forward-Topic', 'Period']


class Topic_Info():
    def __init__(self, in_topic, type, out_topic='' , period=0):
        self.in_topic = in_topic
        self.type = type
        self.out_topic = out_topic
        self.period = period


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.thumbSize = 24

    def data(self, index, role):
        topic = self._data[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return topic.in_topic
            if index.column() == 1:
                return topic.type
            if index.column() == 2:
                return topic.out_topic
            if index.column() == 3:
                return topic.period
        if role == Qt.DecorationRole:
            if index.column() == 3:
                if float(topic.period) > 0:
                    return QPixmap(ICON_ENABLED).scaled(QSize(self.thumbSize, self.thumbSize), Qt.KeepAspectRatio)
                elif float(topic.period) == -1:
                    return QPixmap(ICON_PASSTHROUGH).scaled(QSize(self.thumbSize, self.thumbSize), Qt.KeepAspectRatio)
                else:
                    return QPixmap(ICON_DISABLED).scaled(QSize(self.thumbSize, self.thumbSize), Qt.KeepAspectRatio)

    def get_topic(self, index):
        return self._data[index]

    # def flags(self, index):
    #     return Qt.ItemIsEnabled | Qt.ItemSelectionMode | Qt.ItemIsEditable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return HEADER_LABELS[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        return TOPIC_TABLE_NUM_COL


class TopicSelectionDialog(QDialog):
    def __init__(self, ros_topic, parent=None):
        super().__init__(parent)
        # Load the dialog's GUI
        self.diag = loadUi(UI_DIALOG, self)
        self.result_data = None
        self.rbtn_disabled.clicked.connect(self.update_btn_status)
        self.rbtn_continuous.clicked.connect(self.update_btn_status)
        self.rbtn_period.clicked.connect(self.update_btn_status)
        self.lbl_topic_ros.setText(ros_topic.in_topic)

    def update_btn_status(self):
        self.txt_period.setEnabled(self.rbtn_period.isChecked())

    def accept(self):
        logging.info('Topic Changed')
        self.diag.close()
        period = 0
        if self.rbtn_period.isChecked():
            period = float(self.diag.txt_period.text().replace(',', '.').replace('seconds', ''))
        if self.rbtn_continuous.isChecked():
            period = -1
        self.result_data = (self.diag.txt_topic_mapped.toPlainText(), period)

    # def reject(self):
    #     print('reject')
    #     self.diag.close()
    #     self.result_data = None


def select_topic(topic_to_change):
    t = TopicSelectionDialog(topic_to_change)
    t.exec_()
    result_data = t.result_data
    if result_data:
        topic_to_change.period = float(result_data[1])
        if result_data[1] == 0:
            topic_to_change.out_topic = None
            SubscriptionManager.unsubscribe(topic_to_change.in_topic)
        else:
            topic_to_change.out_topic = result_data[0] if len(result_data[0]) > 0 else topic_to_change.in_topic
            SubscriptionManager.subscribe(topic_to_change.in_topic, topic_to_change.type, topic_to_change.period,
                                          topic_to_change.out_topic)
