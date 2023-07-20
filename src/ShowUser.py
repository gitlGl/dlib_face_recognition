from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize, QPoint,pyqtSlot
from .ImageView import ShowImage
from  PyQt5.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QVBoxLayout,QMenu,QHeaderView,QMessageBox,QAbstractItemView
from .UpdateUser import UpdateUserData
from .ShowLog import ShowLog
from .Paging import Page
from .UpdateUser import UpdateAdminData
import copy
class ShowUser(QWidget):
    def __init__(self,QTableWidget_column_name:list,table_name:str,table_cloumn_name:list,information=None ):
        super().__init__()
        self.information = information
        self.table_name = table_name
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
        # self.qlineedit = QLineEdit()
        # self.qlineedit.setPlaceholderText('Please enter your usernumber')
        # self
        self.tableWidget.customContextMenuRequested[QPoint].connect(self.contextMenu)#菜单右键槽函数
        self.tableWidget.cellDoubleClicked.connect(self.onTableWidgetCellDoubleClicked)
        self.VBoxLayout = QVBoxLayout()
        self.VBoxLayout.addWidget(self.tableWidget)
        self.table_cloumn_name = table_cloumn_name
        if not information:
            self.isNUll = False
            page_count = 30
            self.page = Page(table_name,self.table_cloumn_name,page_count=page_count)
            self.page.information_signal.connect(self.setInformation)
            if  not self.page.information:
                QMessageBox.critical(self, '警告', '不存在用户或记录')
                self.close()
                return
            self.VBoxLayout.addWidget(self.page)
        else:self.isNUll = True
        self.setLayout(self.VBoxLayout)
        columncout = len(QTableWidget_column_name)
        self.tableWidget.setColumnCount(columncout)#根据数据量确定列数
        self.tableWidget.setHorizontalHeaderLabels(QTableWidget_column_name)
        self.setInformation()
        
               
    def setInformation(self):
        if  not self.isNUll:
            self.information = self.page.information
        information = self.information
       
      
        self.tableWidget.setRowCount(0)
        information = copy.deepcopy(self.information)
        for row1 ,i in enumerate(information):
            self.tableWidget.insertRow(row1)
            for row2,cloumn in enumerate(self.table_cloumn_name):
                item  = QTableWidgetItem((i[cloumn]))
                self.tableWidget.setItem(row1, row2, item)
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)

            img_item =  QTableWidgetItem()
            self.tableWidget.setIconSize(QSize(60, 100))
            imag_path = "img_information/{0}/{1}/{2}.jpg".format(
                self.table_name,i["id_number"],i["id_number"])#获取图片路径
            img_item.setIcon(QIcon(imag_path))
            img_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            self.tableWidget.setItem(row1, row2+1,img_item)
           

class ShowStudentUser(ShowUser):
    def __init__(self,str_list_column,table,list_cloumn,information=None ):
        super().__init__(str_list_column,table,list_cloumn,information)
      
    def onTableWidgetCellDoubleClicked(self, row):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        update_data = UpdateUserData(self.information[row])
        ok = update_data.exec_()
        if not ok:
            return
        user_name = update_data.user_name_line.text()
        id_number = update_data.id_number_line.text()
        gender = update_data.gender_line.text()
        password = update_data.password_line.text()
        #变更信息后修改信息
        self.information[row]["id_number"] = id_number
        self.information[row]["user_name"] = user_name
        self.information[row]["gender"] = gender
        self.information[row]["password"] = password
         #变更表格信息
        self.tableWidget.item(row, 0).setText(id_number)
        self.tableWidget.item(row, 1).setText(user_name)
        self.tableWidget.item(row, 2).setText(gender)
        self.tableWidget.item(row, 3).setText(password)
        self.tableWidget.item(row,4).setIcon(QIcon("img_information/{0}/{1}/{2}.jpg"
        .format(self.table_name,self.information[row]["id_number"],self.information[row]["id_number"])))#获取图片路径)
    @pyqtSlot(QPoint)
    def contextMenu(self,pos):
        item = self.tableWidget.itemAt(pos)
        if item == None:
            return
        selected_rows = set()
        for r in self.tableWidget.selectedRanges():
            selected_rows.update(range(r.topRow(), r.bottomRow() + 1))
        selected_rows = list(selected_rows)
        selected_rows.sort(reverse=True)
        pop_menu = QMenu()
        #菜单事件信号
        delete_event = pop_menu.addAction("删除选中")
        if len(selected_rows) == 1:
            change_new_event = pop_menu.addAction("修改")
            imageView_event = pop_menu.addAction("查看图片")
            log_event = pop_menu.addAction("查看日志")
        row = item.row()
        update_data = UpdateUserData(self.information[row])
        action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))#显示菜单列表，pos为菜单栏坐标位置
        if action == None:
            return
        if action == delete_event:
            r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No)
            if r == QMessageBox.No:
                return
            for row in selected_rows:
                update_data.delete(self.information[row]["id_number"])
                self.tableWidget.removeRow(row) 
                self.information.pop(row)#删除信息列表
            return
        if action == change_new_event:
            ok = update_data.exec_()
            if not ok:
                return
            user_name = update_data.user_name_line.text()
            id_number = update_data.id_number_line.text()
            gender = update_data.gender_line.text()
            password = update_data.password_line.text()
        #变更信息后修改信息
            self.information[row]["id_number"] = id_number
            self.information[row]["user_name"] = user_name
            self.information[row]["gender"] = gender
            self.information[row]["password"] = password
           
        #变更表格信息
            self.tableWidget.item(item.row(), 0).setText(id_number)
            self.tableWidget.item(item.row(), 1).setText(user_name)
            self.tableWidget.item(item.row(), 2).setText(gender)
            self.tableWidget.item(row, 3).setText(password)
            self.tableWidget.item(row,4).setIcon(QIcon("img_information/{0}/{2}/{2}.jpg"
    .format(self.table_name,self.information[row]["id_number"],self.information[row]["id_number"])))#获取图片路径)
            return

        
        if action == imageView_event:
            imag_path = "img_information/{0}/{1}/{2}.jpg".format(self.table_name,
            str(self.information[row]["id_number"]),
            str(self.information[row]["id_number"]))
            show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
            show_imag.exec_()
            return
        if action == log_event:
            #result = Database().c.execute("select rowid,id_number,log_time from student_log_time where id_number ={0} order by log_time desc".format(self.information[row]["id_number"])).fetchall()
            result = ShowLog(self.information[row]["id_number"],
            [ '学号','时间',"图片" ], self.table_name,['id','id_number','log_time'])
            if not result.page.information:
                return
            result.exec()
            return

class ShowAdminUser(ShowUser):
    def __init__(self,str_list_column,table,list_cloumn,information=None ):
        super().__init__(str_list_column,table,list_cloumn,information)

    def onTableWidgetCellDoubleClicked(self, row):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        update_data =UpdateAdminData(self.information[row])
        ok = update_data.exec_()
        if not ok:
            return
        
        id_number = update_data.id_number_line.text()
        password = update_data.password_line.text()

        #变更信息后修改信息
        self.information[row]["id_number"] = id_number
        self.information[row]["password"] = password
       
         #变更表格信息
        self.tableWidget.item(row, 0).setText(id_number)
        self.tableWidget.item(row, 1).setText(password)
        self.tableWidget.item(row,2).setIcon(QIcon("img_information/admin/{0}/{1}.jpg"
        .format(self.information[row]["id_number"],self.information[row]["id_number"])))#获取图片路径)
    @pyqtSlot(QPoint)
    def contextMenu(self,pos):
        item = self.tableWidget.itemAt(pos)
        if item == None:
            return
        selected_rows = set()
        for r in self.tableWidget.selectedRanges():
            selected_rows.update(range(r.topRow(), r.bottomRow() + 1))
        selected_rows = list(selected_rows)
        selected_rows.sort(reverse=True)
        pop_menu = QMenu()
        #菜单事件信号
        delete_event = pop_menu.addAction("删除选中")
        if len(selected_rows) == 1:
            change_new_event = pop_menu.addAction("修改")
            imageView_event = pop_menu.addAction("查看图片")
            log_event = pop_menu.addAction("查看日志")
        row = item.row()
        update_data =UpdateAdminData(self.information[row])
        action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))#显示菜单列表，pos为菜单栏坐标位置
        if action == None:
            return
        if action == delete_event:
            r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No)
            if r == QMessageBox.No:
                return
            for row in selected_rows:
                if self.information[row]["id_number"] == "12345678910":
                    QMessageBox.critical(self, '警告', '不能删除admin用户')
                    continue
                update_data.delete(self.information[row]["id_number"])
                self.tableWidget.removeRow(row) 
                self.information.pop(row)#删除信息列表
            return
        
        if action == change_new_event:
            ok = update_data.exec_()
            if not ok:
                return
            password = update_data.password_line.text()
            id_number = update_data.id_number_line.text()
        
        #变更信息后修改信息
            self.information[row]["id_number"] = id_number
            self.information[row]["password"] = password

        #变更表格信息
            self.tableWidget.item(item.row(), 0).setText(id_number)
            self.tableWidget.item(item.row(), 1).setText(password)
            self.tableWidget.item(row,2).setIcon(QIcon("img_information/admin/{0}/{1}.jpg"
    .format(self.information[row]["id_number"],self.information[row]["id_number"])))#获取图片路径)

       
        if action == imageView_event:
            imag_path = "img_information/{0}/{1}/{2}.jpg".format(self.table_name,
            str(self.information[row]["id_number"]),str(self.information[row]["id_number"]))
            show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
            show_imag.exec_()
            return
        if action == log_event:
            result = ShowLog(self.information[row]["id_number"],[ '用户ID', '登录时间',"图片" ],
            self.table_name,['id','id_number','log_time'])
            if not result.page.information:
                return
            result.exec_()
            return

