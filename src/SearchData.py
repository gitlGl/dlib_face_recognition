from  PyQt5.QtWidgets import QWidget,QTableWidget,QLineEdit,QTableWidgetItem,QVBoxLayout,QMenu,QHeaderView,QMessageBox
from src.Database import Database
from src.UpdateData import UpdateData
from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint,pyqtSlot,Qt
class SearchData(QWidget):
    def __init__(self ):
        super().__init__()
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
        # self.qlineedit = QLineEdit()
        # self.qlineedit.setPlaceholderText('Please enter your usernumber')
        # self
        self.tableWidget.customContextMenuRequested[QPoint].connect(self.context_menu)#菜单右键槽函数
        self.tableWidget.cellDoubleClicked.connect(self.on_tableWidget_cellDoubleClicked)
        self.VBoxLayout = QVBoxLayout()
        self.VBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.VBoxLayout)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        
        self.tableWidget.setHorizontalHeaderLabels([ '学号', '姓名', '性别',"图片" ])
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
        update_data = UpdateData(self.information)
        ok = update_data.exec_()
        print("是否",ok)
        if not ok:
            return
        user_name = update_data.user_name_line.text()
        id_number = update_data.id_number_line.text()
        gender = update_data.gender_line.text()
        #变更信息后修改信息
        self.information["id_number"] = id_number
        self.information["user_name"] = user_name
        self.information["gender"] = gender

        self.tableWidget.item(row, 0).setText(id_number)
        self.tableWidget.item(row, 1).setText(user_name)
        self.tableWidget.item(row, 2).setText(gender)
    @pyqtSlot(QPoint)
    def context_menu(self,pos):
        print("测试",pos)
        update_data = UpdateData(self.information)
        pop_menu = QMenu()
        #菜单事件信号
        change_new_event = pop_menu.addAction("修改")
        delete_event = pop_menu.addAction("删除")
        item = self.tableWidget.itemAt(pos)
        if item != None:  
            action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))#显示菜单列表，pos为菜单栏坐标位置
            if action == change_new_event:
                user_name = update_data.user_name_line.text()
                id_number = update_data.id_number_line.text()
                gender = update_data.gender_line.text()
                ok = update_data.exec_()
                if not ok:
                    return
                user_name = update_data.user_name_line.text()
                id_number = update_data.id_number_line.text()
                gender = update_data.gender_line.text()
            #变更信息后修改信息
                self.information["id_number"] = id_number
                self.information["user_name"] = user_name
                self.information["gender"] = gender
            #变更表格信息
                self.tableWidget.item(0, 0).setText(id_number)
                self.tableWidget.item(0, 1).setText(user_name)
                self.tableWidget.item(0, 2).setText(gender)
            elif action == delete_event:
                r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if r == QMessageBox.No:
                   return
                update_data.delete(int(self.information["id_number"]))
                self.tableWidget.itemDelegate()
                # self.tableWidget.item(0, 1).setText(user_name)
                # self.tableWidget.item(0, 2).setText(gender)

from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':
  app = QApplication(sys.argv)
  test = SearchData()
  test.show()
  app.exec_()


   