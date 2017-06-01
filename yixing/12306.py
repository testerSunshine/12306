# -*- coding: utf8 -*-
from PyQt5 import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QAbstractItemView

from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFontDialog
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem

__author__ = 'MR.wen'

from PyQt5 import QtWidgets, QtCore
from yixing.test import Ui_MainWindow
from yixing.tiket import Ui_Form


class myWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    _signal = QtCore.pyqtBoundSignal(str)

    def __init__(self):
        super(myWindow, self).__init__()
        self.setupUi(self)
        self.fileOpen.triggered.connect(self.opMsg)
        self.closeFile.triggered.connect(self.close)
        self.actionTst.triggered.connect(self.childShow)
        self.pushButton_2.clicked.connect(self.call_ticket)

    def getStr(self):
        print (self.lineEdit.text())
        self.textEdit.setText(self.lineEdit.text())

    def call_ticket(self):
        """
        调用添加坐席俺窗口
        :return:
        """
        self.t = tiket()
        self.t.show()

    def getDate(self):
        print("is ok!")

    def opMsg(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "All Files (*);;Text Files (*.txt)")
        print(file)
        self.statusbar.showMessage(file)

    def childShow(self):
        self.gridLayout.addWidget(self.child)
        print("gridLayout id ok! ")
        self.child.show()


class tiket(QtWidgets.QMainWindow, Ui_Form):
    """车票设置窗口"""
    def __init__(self):
        super(tiket, self).__init__()
        self.setWindowTitle("添加车次信息")
        self.setupUi(self)
        self.dateEdit_2.setCalendarPopup(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)    # 表格自适应窗口
        table_length = ["车次", "出发站", "到达站", "历时", "商务座", "特等座", "一等座", "二等座", "软卧", "硬卧", "软座", "无座"]
        self.tableWidget.setColumnCount(len(table_length))  # 设置表格长度
        self.tableWidget.setRowCount(10)
        self.tableWidget.setHorizontalHeaderLabels(table_length)  # 设置表格行
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选中的方式
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)   # 设置为可以选中多个目标
        newItem = QTableWidgetItem("松鼠")
        self.tableWidget.setItem(0, 0, newItem)

        newItem = QTableWidgetItem("10cm")
        self.tableWidget.setItem(0, 1, newItem)

        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 2, newItem)

        newItem = QTableWidgetItem("松鼠")
        self.tableWidget.setItem(1, 0, newItem)

        newItem = QTableWidgetItem("10cm")
        self.tableWidget.setItem(1, 1, newItem)

        newItem = QTableWidgetItem("61g")
        self.tableWidget.setItem(1, 2, newItem)

        self.onlySelect.clicked.connect(self.outSelect)

    def outSelect(self, item=None):
        if item is None:
            return
        else:
            rows = self.tableWidget.currentRow
            print(rows)
            for i in range(self.tableWidget.columnCount()):   # 选中行数之后，遍历改列所有数据
                print(self.tableWidget.item(rows, i).text())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myshow = myWindow()
    myshow.show()
    sys.exit(app.exec_())
