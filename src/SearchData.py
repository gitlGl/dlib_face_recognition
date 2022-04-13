from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
from  PyQt5.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QVBoxLayout,QMenu,QHeaderView,QMessageBox
from src.UpdateData import UpdateData
from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint,pyqtSlot,Qt
from .ImageView import ShowImage
from .Database import Database
from .ShowStudentLog import ShowStudentLog
class SearchData(QWidget):
    def __init__(self,information,str_list_column ):
        super().__init__()
        self.information = information
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
        columncout = len(str_list_column)
        self.tableWidget.setColumnCount(columncout)#根据数据量确定列数
        self.tableWidget.setHorizontalHeaderLabels(str_list_column)
        self.set_information()
    def set_information(self):
        row = 0
        self.tableWidget.setRowCount(0)
        print(len(self.information))
        for i in self.information:
            self.tableWidget.insertRow(row)
            sid_item = QTableWidgetItem(str(i["id_number"]))
            name_item = QTableWidgetItem(i["user_name"])
            if  i["gender"] == 0:
                i["gender"] = "女"
            else:
                i["gender"] = "男"
            sex_item = QTableWidgetItem(i["gender"])
            img_item =  QTableWidgetItem()
            self.tableWidget.setIconSize(QSize(60, 100))
            imag_path = "img_information/student/{0}/{1}.jpg".format(i["id_number"],i["id_number"])
            img_item.setIcon(QIcon(imag_path))
            sid_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            name_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            sex_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            
            self.tableWidget.setItem(row, 0, sid_item)
            self.tableWidget.setItem(row, 1, name_item)
            self.tableWidget.setItem(row, 2, sex_item)
            self.tableWidget.setItem(row, 3,img_item)
            row = row + 1
            self.tableWidget.setRowCount(row)
      
           
    def on_tableWidget_cellDoubleClicked(self, row, column):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        update_data = UpdateData(self.information[row])
        ok = update_data.exec_()
        print("是否",ok)
        if not ok:
            return
        user_name = update_data.user_name_line.text()
        id_number = update_data.id_number_line.text()
        gender = update_data.gender_line.text()
        #变更信息后修改信息
        self.information[row]["id_number"] = int(id_number)
        self.information[row]["user_name"] = user_name
        self.information[row]["gender"] = gender

        self.tableWidget.item(row, 0).setText(id_number)
        self.tableWidget.item(row, 1).setText(user_name)
        self.tableWidget.item(row, 2).setText(gender)
    @pyqtSlot(QPoint)
    def context_menu(self,pos):
        print("测试",pos)
        pop_menu = QMenu()
        #菜单事件信号
        change_new_event = pop_menu.addAction("修改")
        delete_event = pop_menu.addAction("删除")
        imageView_event = pop_menu.addAction("查看图片")
        log_event = pop_menu.addAction("查看日志")
        item = self.tableWidget.itemAt(pos)
        if item != None:
            row = item.row()
            update_data = UpdateData(self.information[row])
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
                self.information[row]["id_number"] = int(id_number)
                self.information[row]["user_name"] = user_name
                self.information[row]["gender"] = gender
            #变更表格信息
                self.tableWidget.item(item.row(), 0).setText(id_number)
                self.tableWidget.item(item.row(), 1).setText(user_name)
                self.tableWidget.item(item.row(), 2).setText(gender)
            elif action == delete_event:
                r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if r == QMessageBox.No:
                   return
                update_data.delete(int(self.information[row]["id_number"]))
                self.tableWidget.removeRow(row) 
                self.information.remove(self.information[row])#删除信息列表
            elif action == imageView_event:
                imag_path = "img_information/student/{0}/{1}.jpg".format(str(self.information[row]["id_number"]),str(self.information[row]["id_number"]))
                show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
                show_imag.exec_()
            elif action == log_event:
                result = Database().c.execute("select rowid,id_number,log_time from student_log_time where id_number ={0}".format(self.information[row]["id_number"])).fetchall()
                self.result = ShowStudentLog(result,[ '时间',"图片" ])
                self.result.exec()

