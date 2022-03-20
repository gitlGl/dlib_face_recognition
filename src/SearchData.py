from  PyQt5.QtWidgets import QWidget,QTableWidget,QLineEdit,QTableWidgetItem,QVBoxLayout
from src.Database import Database
from src.UpdateData import UpdateData
from PyQt5 import QtWidgets
class SearchData(QWidget):
    def __init__(self ):
        super().__init__()
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        # self.qlineedit = QLineEdit()
        # self.qlineedit.setPlaceholderText('Please enter your usernumber')
        # self
        self.tableWidget.cellDoubleClicked.connect(self.on_tableWidget_cellDoubleClicked)
        self.VBoxLayout = QVBoxLayout()
        self.VBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.VBoxLayout)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)#设置首行
        item =QTableWidgetItem()
       
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
       
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText( "学号")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText("姓名")
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText("性别")

    def set_information(self,information):
        self.information = information
        row = self.tableWidget.rowCount()
        print(self.tableWidget.rowCount())
        sid_item = QTableWidgetItem(information["id_number"])
        name_item = QTableWidgetItem(information["user_name"])
        sex_item = QTableWidgetItem(information["gender"])
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, sid_item)
        self.tableWidget.setItem(row, 1, name_item)
        self.tableWidget.setItem(row, 2, sex_item)
    def on_tableWidget_cellDoubleClicked(self, row, column):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        id = self.tableWidget.item(row, 0).text()#表格第一行第一列
        update_data = UpdateData(self.information)
        ok = update_data.exec_()
        if not ok:
            return
        user_name = update_data.user_name_line.text()
        id_number = update_data.id_number_line.text()
        gender = update_data.gender_line.text()
        vector_path = update_data.vector_line.text()
        self.tableWidget.item(row, 0).setText(user_name)
        self.tableWidget.item(row, 1).setText(id_number)
        self.tableWidget.item(row, 2).setText(gender)
     
   
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':
  app = QApplication(sys.argv)
  test = SearchData()
  test.show()
  app.exec_()


   