from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize, QPoint,pyqtSlot
from .ImageView import ShowImage
from  PyQt5.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QVBoxLayout,QMenu,QHeaderView,QMessageBox,QAbstractItemView
from src.UpdateUserData import UpdateUserData
from .ShowLog import ShowLog
from .Paging import Page
class ShowStudentUser(QWidget):
    def __init__(self,str_list_column,information=None ):
        super().__init__()
        self.information = information
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
        # self.qlineedit = QLineEdit()
        # self.qlineedit.setPlaceholderText('Please enter your usernumber')
        # self
        self.tableWidget.customContextMenuRequested[QPoint].connect(self.context_menu)#菜单右键槽函数
        self.tableWidget.cellDoubleClicked.connect(self.on_tableWidget_cellDoubleClicked)
        self.VBoxLayout = QVBoxLayout()
        self.VBoxLayout.addWidget(self.tableWidget)

        self.page_count = 30
        self.list_cloumn = ["id_number","user_name","gender","password"]
        self.page = Page("student",self.list_cloumn,page_count=self.page_count)
        self.page.information_signal.connect(self.set_information)
        if not information:
            
            self.VBoxLayout.addWidget(self.page)
        else:
            self.page.information = information
            self.page.hide()
        self.setLayout(self.VBoxLayout)
        columncout = len(str_list_column)
        self.tableWidget.setColumnCount(columncout)#根据数据量确定列数
        self.tableWidget.setHorizontalHeaderLabels(str_list_column)
        self.set_information()
    def set_information(self):
        self.information = self.page.information
        row = 0
        self.tableWidget.setRowCount(0)
        for i in self.information:
            self.tableWidget.insertRow(row)
            row2 = 0
            for cloumn in self.list_cloumn:
                if cloumn == 'password':
                    continue
                if cloumn != "gender":
                    item  = QTableWidgetItem((i[cloumn]))
                    self.tableWidget.setItem(row, row2, item)
                    item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                   
                else:
                    if  i["gender"] == 0:
                        i["gender"] = "女"
                    else:
                        i["gender"] = "男"
                    sex_item = QTableWidgetItem(i["gender"])
                    sex_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                    self.tableWidget.setItem(row, row2, sex_item)
                row2 +=1


            img_item =  QTableWidgetItem()
            self.tableWidget.setIconSize(QSize(60, 100))
            imag_path = "img_information/student/{0}/{1}.jpg".format(i["id_number"],i["id_number"])#获取图片路径
            img_item.setIcon(QIcon(imag_path))
            img_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            self.tableWidget.setItem(row, len(self.list_cloumn)-1,img_item)
            row = row + 1
           
    def on_tableWidget_cellDoubleClicked(self, row):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        print(row)
        print(self.information)
        update_data = UpdateUserData(self.information[row])
        ok = update_data.exec_()
        if not ok:
            return
        user_name = update_data.user_name_line.text()
        id_number = update_data.id_number_line.text()
        gender = update_data.gender_line.text()
        #变更信息后修改信息
        self.information[row]["id_number"] = id_number
        self.information[row]["user_name"] = user_name
        self.information[row]["gender"] = gender
         #变更表格信息
        self.tableWidget.item(row, 0).setText(id_number)
        self.tableWidget.item(row, 1).setText(user_name)
        self.tableWidget.item(row, 2).setText(gender)
        self.tableWidget.item(row,3).setIcon(QIcon("img_information/student/{0}/{1}.jpg"
        .format(self.information[row]["id_number"],self.information[row]["id_number"])))#获取图片路径)
    @pyqtSlot(QPoint)
    def context_menu(self,pos):
        pop_menu = QMenu()
        #菜单事件信号
        change_new_event = pop_menu.addAction("修改")
        delete_event = pop_menu.addAction("删除")
        imageView_event = pop_menu.addAction("查看图片")
        log_event = pop_menu.addAction("查看日志")
        item = self.tableWidget.itemAt(pos)
        if item == None:
            return
        row = item.row()
        update_data = UpdateUserData(self.information[row])
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
            self.information[row]["id_number"] = id_number
            self.information[row]["user_name"] = user_name
            self.information[row]["gender"] = gender
        #变更表格信息
            self.tableWidget.item(item.row(), 0).setText(id_number)
            self.tableWidget.item(item.row(), 1).setText(user_name)
            self.tableWidget.item(item.row(), 2).setText(gender)
            self.tableWidget.item(row,3).setIcon(QIcon("img_information/student/{0}/{1}.jpg"
    .format(self.information[row]["id_number"],self.information[row]["id_number"])))#获取图片路径)
            return

        if action == delete_event:
            r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if r == QMessageBox.No:
                return
            update_data.delete(self.information[row]["id_number"])
            self.tableWidget.removeRow(row) 
            self.information.remove(self.information[row])#删除信息列表
            return
        if action == imageView_event:
            imag_path = "img_information/student/{0}/{1}.jpg".format(str(self.information[row]["id_number"]),
            str(self.information[row]["id_number"]))
            show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
            show_imag.exec_()
            return
        if action == log_event:
            #result = Database().c.execute("select rowid,id_number,log_time from student_log_time where id_number ={0} order by log_time desc".format(self.information[row]["id_number"])).fetchall()
            self.result = ShowLog(self.information[row]["id_number"],
            [ '学号','时间',"图片" ], "student",['rowid','id_number','log_time'])
            self.result.exec()
            return

