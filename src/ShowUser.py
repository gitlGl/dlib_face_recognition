from PySide6.QtCore import Qt,QPoint,Slot,QObject
from .ImageView import ShowImage
from  PySide6.QtWidgets import QWidget,QTableWidget,QTableWidgetItem
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QVBoxLayout,QMenu,QHeaderView,QMessageBox,QPushButton,QHBoxLayout,QLabel
from .ShowLog import ShowLog
from .Paging import Page
from .Database import PH
from .Creatuser import CreatUser
from .Check import getImgPath
from .Setting import database
from .Check import verifyCellData
from .MyMd5 import MyMd5
import os ,shutil 
from . import Setting
class ShowUser(QWidget):
    def __init__(self,table_name:str,information=None ):
        super().__init__()
        self.table_name = table_name
        self.information = information
        if self.table_name == "admin":
            self.verifyCellDataFn:list = [verifyCellData.idNumber,verifyCellData.password]
            self.verifyCellDataLambda:list = [verifyCellData.id_number_info,verifyCellData.password_info]
            self.table_cloumn_name = ["id_number",'password']
            self.log_column_name = ['id','id_number','log_time']
            self.QTableWidget_column_name = [ '用户ID', '密码',"图片" ]
            self.column = 1
        else:
            self.verifyCellDataFn:list = [ verifyCellData.idNumber,verifyCellData.userName,
                                        verifyCellData.gneder,
                                       verifyCellData.password]
            self.verifyCellDataLambda:list = [verifyCellData.id_number_info,verifyCellData.user_name_info,
                                              verifyCellData.gender_info,verifyCellData.password_info]
            self.table_cloumn_name = ["id_number", "user_name", "gender", "password"]
            self.log_column_name = ['id','id_number','log_time']
            self.QTableWidget_column_name = [ '学号', '姓名', '性别', '密码',"图片" ]
            self.column = 3
        
        
        self.tableWidget = QTableWidget(self)
        self.tableWidget.customContextMenuRequested[QPoint].connect(self.contextMenu)#菜单右键槽函数
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        from PySide6.QtWidgets import QAbstractItemView

        #self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
        # self.qlineedit = QLineEdit()
        # self.qlineedit.setPlaceholderText('Please enter your usernumber')
        # self
        
        #self.tableWidget.cellDoubleClicked.connect(self.onTableWidgetCellDoubleClicked)
        self.VBoxLayout = QVBoxLayout()
        self.VBoxLayout.addWidget(self.tableWidget)
       
        if not information:
            self.isNUll = False
            page_count = Setting.page_count
            self.page = Page(table_name,self.table_cloumn_name,page_count=page_count)
            self.page.information_signal.connect(self.setInformation)
            if  not self.page.information:
                QMessageBox.information(self, '警告', '不存在用户或记录')
                self.close()
                return
            self.VBoxLayout.addWidget(self.page)
        else: self.isNUll = True
        self.setLayout(self.VBoxLayout)
        columncout = len(self.QTableWidget_column_name)
        self.tableWidget.setColumnCount(columncout)#根据数据量确定列数
        self.tableWidget.setHorizontalHeaderLabels(self.QTableWidget_column_name)
        self.setInformation()
        
    def setInformation(self):
        try:
            self.tableWidget.cellChanged.disconnect(self.on_cell_changed)#单元格变更槽函数
        except:
            pass
        if  not self.isNUll:
            self.information = self.page.information
        information = self.information
       
        self.tableWidget.setRowCount(0)
        for row1 ,i in enumerate(information):
            self.tableWidget.insertRow(row1)
            for row2,cloumn in enumerate(self.table_cloumn_name):
                item  = QTableWidgetItem((i[cloumn]))
                color = QColor(111, 156, 207)
                item.setForeground(color)
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
        self.tableWidget.cellChanged.connect(self.on_cell_changed)#单元格变更槽函数
    def handle_button_click(self):
        sender = QObject.sender(self).parent()#获取信号发送者的对象
        path = getImgPath(self)
        id_number = sender.id_number
        
        if path:
            vector = CreatUser.getVector(path)
            CreatUser.insertImg(id_number,path,self.table_name)
            database.execute("update {0} set vector = {1} where id_number = {2}"
                             .format(self.table_name,PH,id_number),(vector,))
            QMessageBox.information(self, 'Success', '修改成功')
            sender.label.setPixmap(QPixmap(path))

    def on_cell_changed(self,row, column):
        id_number = self.information[row]["id_number"]
        text = self.tableWidget.item(row, column).text()
        if not self.verifyCellDataFn[column](
            self,text,self.information[row]):
            self.tableWidget.cellChanged.disconnect(self.on_cell_changed)#单元格变更槽函数
            self.tableWidget.item(row, column).setText("格式错误-"+text)
            self.tableWidget.item(row, column).setForeground(Qt.red)
            self.verifyCellDataLambda[column](self)
            self.tableWidget.cellChanged.connect(self.on_cell_changed)#单元格变更槽函数
            return
        if self.column == column:
            salt = MyMd5.createSalt()
            password = MyMd5.createMd5(text, salt,id_number)
            database.execute("update {0} set {1} = '{2}',salt = '{3}' where id_number = {4}"
                                .format(self.table_name,         
                            self.table_cloumn_name[column],password,salt,id_number))
            self.information[row][self.table_cloumn_name[column]] = text
           
            return
        if column == 0 and self.table_name == "admin" :
            if id_number == '12345678910':
                QMessageBox.critical(self, '警告', '不能修改admin用户')
                self.tableWidget.cellChanged.disconnect(self.on_cell_changed)#单元格变更槽函数
                self.tableWidget.item(row, column).setText(id_number)
                self.tableWidget.cellChanged.connect(self.on_cell_changed)#单元格变更槽函数
                return
            self.changeIdNumber(text,id_number)
            self.information[row][self.table_cloumn_name[column]] = text
            return
        
        qcolor = QColor(111, 156, 207)
        self.tableWidget.item(row, column).setForeground(qcolor)
        database.execute("update {0} set {1} = '{2}' where id_number = {3}"
                         .format(self.table_name,
                                 self.table_cloumn_name[column],text,id_number))
        self.information[row][self.table_cloumn_name[column]] = text

    def changeIdNumber(self,id_number,old_id_number):
        try: 
            database.execute("begin")
            database.execute(
                "update {0} set id_number = {1} where id_number = {2}"
                .format(self.table_name, id_number, old_id_number))
            
            database.execute(
                "update {0} set id_number = {1} where id_number = {2}"
                .format(self.table_name+"_log_time", id_number, old_id_number)) 
            database.conn.commit()

        except Exception as e:
                database.conn.rollback()
                QMessageBox.critical(self, '警告', "未知错误")
                return False

                ##更改用户文件信息
        old_path = "img_information/student/{0}/".format(old_id_number)
        new_path = "img_information/student/{0}/".format(id_number)
        #更改后变更用户日志信息文件夹
        if not os.path.exists(old_path) and not os.path.exists(new_path):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(new_path)
            os.makedirs("img_information/student/{0}/log".format(
                id_number))
            QMessageBox.critical(self, '警告', "该用户图片文件可能丢失！")
            #shutil.rmtree("img_information/student/{0}".format(str(id)))
        else:
            img_path = "img_information/student/{0}/{1}.jpg".format(
                old_id_number, old_id_number)
            if os.path.isfile(img_path):
                os.rename(
                    img_path, "img_information/student/{0}/{1}.jpg".format(
                        old_id_number, id_number))
            else:
                QMessageBox.critical(self, '警告', "该用户图片文件可能丢失！")
            os.rename(old_path, new_path)
        return True


    def Refresh(self):
        self.page.page_number.emit(int(self.page.cur_page.text()))
        self.setInformation()
    def onTableWidgetCellDoubleClicked(self, row):
        imag_path = "img_information/{0}/{1}/{2}.jpg".format(self.table_name,
                self.information[row]["id_number"],
                self.information[row]["id_number"])
        show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
        show_imag.exec_()
        return




       
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
        refresh = pop_menu.addAction("刷新全页")
        if len(selected_rows) == 1:
            imageView_event = pop_menu.addAction("查看图片")
            log_event = pop_menu.addAction("查看日志")

        row = item.row()
        
        action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))#显示菜单列表，pos为菜单栏坐标位置
        if action == None:
            return
        if action == refresh:
            self.Refresh()
            return
        if action == delete_event:
            r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No)
            if r == QMessageBox.No:
                return
            for row in selected_rows:
                if self.table_name =="admin" \
                and self.information[row]["id_number"] == '12345678910':
                    QMessageBox.critical(self, '警告', '不能删除admin用户')
                    return
                self.delete(self.information[row]["id_number"])
                self.tableWidget.removeRow(row) 
                self.information.pop(row)#删除信息列表
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
           self.QTableWidget_column_name, self.table_name, self.log_column_name)
            if not result.page.information:
                return
            result.exec()
            return


     
    def delete(self, id):
        database.execute("begin")
        path = "img_information/{0}/{1}".format(self.table_name,str(id))
        try:
            database.execute(
                "delete from {0} where id_number = {1}".format(self.table_name,id))
            database.execute(
                "delete from {0} where id_number = {1}".format(self.table_name+"_log_time",id))
            database.conn.commit()
        except:
            QMessageBox.critical(self, '警告', "未知错误")
            database.conn.rollback()
            return

        #删除用户日志信息文件
        if os.path.exists(path):
            shutil.rmtree(path)
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