# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'monitoring_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from designer.custom_widgets import Custom_Table


class Ui_Monitoring(object):
    def setupUi(self, Monitoring):
        Monitoring.setObjectName("Monitoring")
        Monitoring.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Monitoring)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_select = QtWidgets.QWidget()
        self.tab_select.setObjectName("tab_select")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_select)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_select)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.tab_select)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 2, 0, 1, 1)
        self.lbl = QtWidgets.QLabel(self.tab_select)
        self.lbl.setObjectName("lbl")
        self.gridLayout_2.addWidget(self.lbl, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_select)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)
        self.btn_retrieve = QtWidgets.QPushButton(self.tab_select)
        self.btn_retrieve.setObjectName("btn_retrieve")
        self.gridLayout_2.addWidget(self.btn_retrieve, 3, 0, 1, 2)
        self.tbl_topics = Custom_Table(self.tab_select)
        self.tbl_topics.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tbl_topics.setObjectName("tbl_topics")
        self.gridLayout_2.addWidget(self.tbl_topics, 4, 0, 1, 2)
        self.tabWidget.addTab(self.tab_select, "")
        self.tab_monitor = QtWidgets.QWidget()
        self.tab_monitor.setObjectName("tab_monitor")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_monitor)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.cb_monitor_topic = QtWidgets.QComboBox(self.tab_monitor)
        self.cb_monitor_topic.setObjectName("cb_monitor_topic")
        self.gridLayout_3.addWidget(self.cb_monitor_topic, 0, 0, 1, 1)
        self.btn_monitor = QtWidgets.QPushButton(self.tab_monitor)
        self.btn_monitor.setObjectName("btn_monitor")
        self.gridLayout_3.addWidget(self.btn_monitor, 0, 1, 1, 1)
        self.tree_monitoring = QtWidgets.QTreeView(self.tab_monitor)
        self.tree_monitoring.setObjectName("tree_monitoring")
        self.gridLayout_3.addWidget(self.tree_monitoring, 1, 0, 1, 2)
        self.tabWidget.addTab(self.tab_monitor, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        Monitoring.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Monitoring)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Monitoring.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Monitoring)
        self.statusbar.setObjectName("statusbar")
        Monitoring.setStatusBar(self.statusbar)

        self.retranslateUi(Monitoring)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Monitoring)

    def retranslateUi(self, Monitoring):
        _translate = QtCore.QCoreApplication.translate
        Monitoring.setWindowTitle(_translate("Monitoring", "MainWindow"))
        self.lbl.setText(_translate("Monitoring", "ROS Core"))
        self.label_2.setText(_translate("Monitoring", "MQTT Broker"))
        self.btn_retrieve.setText(_translate("Monitoring", "Retrieve Topics"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_select), _translate("Monitoring", "Topic Selection"))
        self.btn_monitor.setText(_translate("Monitoring", "Show Monitoring Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_monitor), _translate("Monitoring", "Monitoring Data"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Monitoring = QtWidgets.QMainWindow()
    ui = Ui_Monitoring()
    ui.setupUi(Monitoring)
    Monitoring.show()
    sys.exit(app.exec_())
