from PySide6.QtCore import Qt,QPoint,Slot,QObject
from .ImageView import ShowImage
from  PySide6.QtWidgets import QWidget,QTableWidget,QTableWidgetItem
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QVBoxLayout,QMenu,QHeaderView,QMessageBox,QPushButton,QHBoxLayout,QLabel
from .UpdateUser import UpdateUserData
from .ShowLog import ShowLog
from .Paging import Page
from .UpdateUser import UpdateAdminData
from .Database import PH
from .Creatuser import CreatUser
from .Check import getImgPath
from .GlobalVariable import database
class ShowUser(QWidget):
    def __init__(self,QTableWidget_column_name:list,table_name:str,table_cloumn_name:list,information=None ):
        super().__init__()
        self.information = information
        self.table_name = table_name
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        from PySide6.QtWidgets import QAbstractItemView

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
        # self.qlineedit = QLineEdit()
        # self.qlineedit.setPlaceholderText('Please enter your usernumber')
        # self
        self.tableWidget.customContextMenuRequested[QPoint].connect(self.contextMenu)#菜单右键槽函数
        self.tableWidget.cellChanged.connect(self.on_cell_changed)#单元格变更槽函数
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
        else: self.isNUll = True
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
        for row1 ,i in enumerate(information):
            self.tableWidget.insertRow(row1)
            for row2,cloumn in enumerate(self.table_cloumn_name):
                item  = QTableWidgetItem((i[cloumn]))
                self.tableWidget.setItem(row1, row2, item)
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)

            id_number = i["id_number"]
            imag_path = "img_information/{0}/{1}/{2}.jpg".format(
                self.table_name,id_number,id_number)#获取图片路径
            img_item = EditableIconWidget('变更',imag_path,id_number,parent=self.tableWidget)
            
            
            self.tableWidget.setCellWidget(row1, row2+1,img_item)
            # def returnSlot(id_number):
            #     def wrapper():
            #         self.handle_button_click(id_number)
            #     return wrapper
            # 
            #img_item.button.clicked.connect(returnSlot(id_number))通过闭包传递正确的id_number 
            # img_item.button.clicked.connect(partial(self.handle_button_click,id_number = idnumber))#通过偏函数传递正确的id_number 
            img_item.button.clicked.connect(self.handle_button_click)
    def handle_button_click(self):
        sender = QObject.sender(self).parent()#获取信号发送者的对象
        path = getImgPath(self)
        id_number = sender.id_number
        print(path)
        if path:
            creatuser = CreatUser()
            vector = creatuser.getVector(path)
            creatuser.insertImg(id_number,path,self.table_name)
            database.execute("update {0} set vector = {1} where id_number = {2}"
                             .format(self.table_name,PH,id_number),(vector,))
            QMessageBox.information(self, 'Success', '修改成功')
            sender.label.setPixmap(QPixmap(path))

    def on_cell_changed(self,row, column):
        ...
        #TODO:单元格变更事件

    
    def onTableWidgetCellDoubleClicked(self, row):
        imag_path = "img_information/{0}/{1}/{2}.jpg".format(self.table_name,
                self.information[row]["id_number"],
                self.information[row]["id_number"])
        show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
        show_imag.exec_()
        return







    

class ShowStudentUser(ShowUser):
    def __init__(self,QTableWidget_column_name,table_name,table_cloumn_name,information=None ):
        super().__init__(QTableWidget_column_name,table_name,table_cloumn_name,information)
        self.table_cloumn_name = table_cloumn_name
        
    def on_cell_changed(self,row, column):
        ...
        #TODO:单元格变更事件

       
    @Slot(QPoint)
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
            self.tableWidget.cellWidget(row,4).label.setPixmap(
                QPixmap("img_information/{0}/{2}/{2}.jpg"
            .format(self.table_name,id_number,id_number)))#获取图片路径)
            return

        
        if action == imageView_event:
            imag_path = "img_information/{0}/{1}/{2}.jpg".format(self.table_name,
            self.information[row]["id_number"],
            self.information[row]["id_number"])
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
    def __init__(self,TableWidget_column_name,table_name,table_cloumn,information=None ):
        super().__init__(TableWidget_column_name,table_name,table_cloumn,information)
       
    @Slot(QPoint)
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
            self.tableWidget.cellWidget(row,2).label.setPixmap(
                QPixmap("img_information/{0}/{2}/{2}.jpg"
            .format(self.table_name,id_number,id_number)))#获取图片路径)
       
        if action == imageView_event:
            imag_path = "img_information/{0}/{1}/{2}.jpg".format(self.table_name,
            self.information[row]["id_number"],self.information[row]["id_number"])
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

class EditableIconWidget(QWidget):

    def __init__(self, text, icon_path, id_number,parent=None):
        super().__init__(parent)
        self.id_number = id_number
        self.img_path = icon_path
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.button =  QPushButton(text,parent= self)
        
        self.button.setFixedSize(50, 30)
        self.button.setObjectName("GreenButton2")
        
        
        self.label =QLabel()
        pixmap = QPixmap(icon_path)
        #label.setStyleSheet('border: none;')
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        layout.setSpacing(0)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)