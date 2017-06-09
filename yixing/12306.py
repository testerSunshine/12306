# -*- coding: utf8 -*-
from PyQt5 import Qt, QtGui
from PyQt5.QtWidgets import QAbstractItemView, QComboBox, QPushButton, QCheckBox

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
        self.t = ticket()
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


class ticket(QtWidgets.QMainWindow, Ui_Form):
    """车票设置窗口"""
    def __init__(self):
        super(ticket, self).__init__()
        self.setWindowTitle("添加车次信息")
        self.setupUi(self)
        self.dateEdit_2.setCalendarPopup(True)
        self.get_ticket_info()
        self.get_set_info()
        self.tableWidget.itemDoubleClicked.connect(self.doubleClickedEvent)

    def doubleClickedEvent(self, item):
        """获取选中车次的车次号"""
        row_num = 0
        self.selectTicketInfo.setColumnCount(1)
        self.selectTicketInfo.setRowCount(row_num)
        if item is None:
            return
        else:
            row = self.tableWidget.currentIndex().row()
            if row is not -1:
                rowCount = self.selectTicketInfo.rowCount()
                print(rowCount)
                row_num = rowCount + 1
                self.selectTicketInfo.setRowCount(row_num)
                ticket = self.tableWidget.item(row, 0).text()
                item = QTableWidgetItem(ticket)
                self.selectTicketInfo.horizontalHeader().setVisible(False)
                self.selectTicketInfo.verticalHeader().setVisible(False)
                self.selectTicketInfo.setItem(0, 0, item)

    def get_select_ticket_info(self):
        """获取所选列车表"""


    def get_ticket_info(self):
        """列车信息表"""
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 表格自适应窗口
        self.table_info = ["车次", "出发站", "到达站", "历时", "商务座", "特等座", "一等座", "二等座", "软卧", "硬卧", "软座", "无座", " "]
        self.tableWidget.setColumnCount(len(self.table_info))  # 设置表格长度
        self.tableWidget.setRowCount(10)
        self.tableWidget.setHorizontalHeaderLabels(self.table_info)  # 设置表格行
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选中的方式
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置为可以选中多个目标
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        newItem = QTableWidgetItem("松鼠")
        self.tableWidget.setItem(0, 0, newItem)
        newItem = QTableWidgetItem("10cm")
        self.tableWidget.setItem(0, 1, newItem)
        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 2, newItem)
        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 3, newItem)
        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 4, newItem)
        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 5, newItem)
        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 6, newItem)
        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 7, newItem)
        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 8, newItem)
        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 9, newItem)
        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 10, newItem)
        newItem = QTableWidgetItem("60g")
        self.tableWidget.setItem(0, 11, newItem)

        self.getTicket = QPushButton()  # 表格最后一行添加按钮，供选择车次使用
        self.getTicket.setText("添加")

        self.tableWidget.setCellWidget(0, 12, self.getTicket)

        newItem = QTableWidgetItem("狐狸")
        self.tableWidget.setItem(1, 0, newItem)

        newItem = QTableWidgetItem("10cm")
        self.tableWidget.setItem(1, 1, newItem)

        newItem = QTableWidgetItem("61g")
        self.tableWidget.setItem(1, 2, newItem)


        self.getTicket = QPushButton()  # 表格最后一行添加按钮，供选择车次使用
        self.getTicket.setText("添加")
        self.tableWidget.setCellWidget(1, 12, self.getTicket)


    def get_set_info(self):
        """选择坐席表"""
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 表格自适应窗口
        self.set_info = ["商务座", "特等座", "一等座", "二等座", "软卧", "硬卧", "软座", "无座"]
        self.setInfo.setColumnCount(1)  # 坐席表
        self.setInfo.setRowCount(len(self.set_info))
        self.setInfo.setHorizontalHeaderLabels(self.table_info)  # 设置表格行
        self.setInfo.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置为可以选中多个目标
        self.setInfo.horizontalHeader().setVisible(False)
        self.setInfo.verticalHeader().setVisible(False)
        for i in range(len(self.set_info)):
            self.checkBySet = QTableWidgetItem(self.set_info[i])
            self.checkBySet.setCheckState(QtCore.Qt.Unchecked)
            self.setInfo.setItem(i, 0, self.checkBySet)

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
