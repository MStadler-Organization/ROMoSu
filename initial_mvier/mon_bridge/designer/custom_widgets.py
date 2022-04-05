from PyQt5 import QtWidgets


class Custom_Table(QtWidgets.QTableView):

    def __init__(self,  parent = None):
        super(Custom_Table, self).__init__(parent)

        rowHeight = self.fontMetrics().height()
        self.verticalHeader().setDefaultSectionSize(rowHeight+20)
        #self.setModel(model)

    def setHorizontalHeaderLabels(self,header):
#      self.setHorizontalHeader(header)
      width = 600
      self.setColumnWidth(0, width * 0.20) # 25% Width Column
      self.setColumnWidth(1, width * 0.55) # 75% Width Column
      self.setColumnWidth(2, width * 0.15) # 75% Width Column
      self.setColumnWidth(3, width * 0.10) # 75% Width Column

    def resizeEvent(self, event):
        width = event.size().width()
        self.setColumnWidth(0, width * 0.30) # 25% Width Column
        self.setColumnWidth(1, width * 0.35) # 75% Width Column
        self.setColumnWidth(2, width * 0.15) # 75% Width Column
        self.setColumnWidth(3, width * 0.15) # 75% Width Column
