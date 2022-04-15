
from .ImageView import ImageView
from .Database import Database
from .ImageView import ShowImage
from .Creatuser import CreatUser
from .GlobalVariable import models
from .MyMd5 import MyMd5
import os,sys
from PyQt5.QtCore import Qt
import numpy as np
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QGroupBox,QPushButton,\
QFileDialog,QMessageBox, QMenu,QApplication,QLineEdit,QDialog
from test import StyleSheet
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
from  PyQt5.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QVBoxLayout,QMenu,QHeaderView,QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint,pyqtSlot,Qt
import PIL.Image
class SearchData(QWidget):
    def __init__(self,information,str_list_column ):
        super().__init__()
        self.information = information
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
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
            log_time = QTableWidgetItem(i["log_time"])
            
            img_item =  QTableWidgetItem()
            self.tableWidget.setIconSize(QSize(60, 100))
            imag_path = "img_information/admin/{0}/log/{1}.jpg".format(i["id_number"],i["log_time"])
            img_item.setIcon(QIcon(imag_path))
            sid_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            self.tableWidget.setItem(row, 0, sid_item)
            self.tableWidget.setItem(row, 1, log_time)
            self.tableWidget.setItem(row, 2,img_item)
            row = row + 1
            self.tableWidget.setRowCount(row)
    def on_tableWidget_cellDoubleClicked(self, row, column):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        imag_path = "img_information/admin/{0}/log/{1}.jpg".format(str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
        show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
        show_imag.exec_()
    @pyqtSlot(QPoint)
    def context_menu(self,pos):
        print("测试",pos)
        pop_menu = QMenu()
        #菜单事件信号
        delete_event = pop_menu.addAction("删除")
        imageView_event = pop_menu.addAction("查看图片")
        item = self.tableWidget.itemAt(pos)
        if item != None:
            row = item.row()
            action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))#显示菜单列表，pos为菜单栏坐标位置
            if action == delete_event:
                r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if r == QMessageBox.No:
                   return
                database =  Database()
                print(self.information[row]["rowid"])
                database.c.execute("delete from admin_log_time where rowid  = {0}".format(self.information[row]["rowid"])).fetchall()
                imag_path = "img_information/admin/{0}/log/{1}.jpg".format(str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
                os.remove(imag_path)
                database.conn.commit()
                database.conn.close()
                self.tableWidget.removeRow(row) 
                self.information.remove(self.information[row])#删除信息列表

            elif action == imageView_event:
                imag_path = "img_information/admin/{0}/log/{1}.jpg".format(str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
                print(imag_path)
                show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
                show_imag.exec_()



class AdminInformation(QDialog):
    def __init__(self,id_number):
        super().__init__()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.id_number = id_number
        self.setGeometry(300, 300,400, 380)
        self.setWindowTitle('用户信息')
        self.setWindowIcon(QIcon('resources/用户信息.png'))
        self.setWindowModality(Qt.ApplicationModal)
        

        self.Hlayout = QHBoxLayout()
        self.Vhlayout = QVBoxLayout()
        
        #self.linnedit.setFixedSize(400,15)
        
        self.grou = QGroupBox(self)
        self.img = ImageView("./resources/bg.jpg",Qt.black)
        self.qlabel1 = QLabel(self)
        self.qlabel1.setText("用户ID：{}".format(self.id_number))
        self.btn1 = QPushButton()
        self.btn1 = QPushButton(objectName="GreenButton")
       
        self.btn2 = QPushButton()
        self.btn2 = QPushButton(objectName="GreenButton")
        
        self.btn1.setText("人脸照片")
        self.btn1.clicked.connect(lambda:self.img_event(self.btn1.pos()))
        self.btn2.setText("修改密码")
        self.btn2.clicked.connect(self.update_pwd)
        self.btn3 = QPushButton()
        self.btn3 = QPushButton(objectName="GreenButton")
        self.btn3.clicked.connect(self.browse)
        self.btn3.setText("登录日志")
        self.Hlayout.addWidget(self.qlabel1)
        self.Hlayout.addWidget(self.btn1)
        self.Hlayout.addWidget(self.btn2)
        self.Hlayout.addWidget(self.btn3)
        self.grou.setLayout(self.Hlayout)
        self.Vhlayout.addWidget(self.grou)
        self.Vhlayout.addWidget(self.img)
        self.grou.setMaximumSize(600,40)
        self.setLayout(self.Vhlayout)
    def update_pwd(self):
        self.pwd_dialog = updtae_pwd(self.id_number)
        self.pwd_dialog.exec_()
    def browse(self):
        print("测试登录日志")
        result = Database().c.execute("select rowid,id_number,log_time from admin_log_time where id_number = {0}".format(self.id_number)).fetchall()
        if len(result)!= 0:
            
            self.result = SearchData(result,[ '用户ID', '登录时间',"图片" ])
            self.Vhlayout.itemAt(1).widget().deleteLater()
            self.Vhlayout.addWidget(self.result)
        else: 
            QMessageBox.critical(self, 'Wrong', '不存在用户')
            return
    def img_event(self,pos):
       print("测试",pos)
       pop_menu = QMenu() 
       pop_menu.addAction("查看图片")
       pop_menu.addAction("修改图片")
       action = pop_menu.exec_(self.mapToGlobal(pos))
       if action == pop_menu.actions()[0]:
           self.Vhlayout.itemAt(1).widget().deleteLater()
           img_path = "img_information/admin/{0}/{1}.jpg".format(str(self.id_number),str(self.id_number))
           show_imag = ShowImage(img_path,Qt.WhiteSpaceMode)
           self.Vhlayout.addWidget(show_imag)
       elif action == pop_menu.actions()[1]:
           path = self.get_path()
           if path:
              vector = CreatUser().get_vector(self.id_number,path,"admin")
              database = Database()
              database.c.execute("update admin set vector = ? where id_number = {0}".format(self.id_number),(vector,))
              database.conn.commit()
              database.conn.close()
    def get_path(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "c:\\", "Image files(*.jpg *.gif *.png)")
        if path == '':
            return
        elif os.path.getsize(path) > 1024000:
            QMessageBox.critical(self, 'Wrong', '文件应小于10mb')
            return
        data = open(path,"rb").read(32) 
        if not (data[6:10] in (b'JFIF',b'Exif')):
            QMessageBox.critical(self, 'Wrong', '文件非图片文件')
            return 
        rgbImage = PIL.Image.open(path)
        rgbImage  =  rgbImage .convert("RGB")
        rgbImage =  np.array(rgbImage )
        faces = models.detector(rgbImage)
        if len(faces) == 1:
            return path
        else:
            QMessageBox.critical(self, 'Wrong', '文件不存在人脸或多个人脸')
            return


#密码修改窗口
class updtae_pwd(QDialog):
    def __init__(self,id_number):
        super().__init__()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle('修改密码')
        self.setWindowIcon(QIcon('resources/修改密码.png'))
        self.id_number = id_number
        self.old_pwd_label = QLabel('旧密码:', self)
        self.new_pwd2_label = QLabel('新密码:', self)
        self.new_pwd3_label = QLabel('确认密码:', self)
        self.old_pwd_line = QLineEdit(self)
        self.new_pwd2_line = QLineEdit(self)
        self.new_pwd3_line = QLineEdit(self)

        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.pwd3_h_layout = QHBoxLayout()
        self.ensure_or = QHBoxLayout()
        self.pwd_h_layout.addWidget(self.old_pwd_label)
        self.pwd_h_layout.addWidget(self.old_pwd_line)

        self.pwd2_h_layout.addWidget(self.new_pwd2_label)
        self.pwd2_h_layout.addWidget(self.new_pwd2_line)

        self.pwd3_h_layout.addWidget(self.new_pwd3_label)
        self.pwd3_h_layout.addWidget(self.new_pwd3_line)

        self.pwd_v_layout = QVBoxLayout()
        self.pwd_v_layout.addLayout(self.pwd_h_layout)
        self.pwd_v_layout.addLayout(self.pwd2_h_layout)
        self.pwd_v_layout.addLayout(self.pwd3_h_layout)
        self.btn1_event = QPushButton()
        self.btn1 = QPushButton(objectName="GreenButton")
        self.btn1.setText("确认修改")
        self.btn2 = QPushButton()
        self.btn2 = QPushButton(objectName="GreenButton")
        self.btn2.setText("取消修改")
        self.ensure_or.addWidget(self.btn1)
        self.ensure_or.addWidget(self.btn2)
        self.pwd_v_layout.addLayout(self.ensure_or)
        self.btn1.clicked.connect(self.btn1_update_pwd)
        self.btn2.clicked.connect(self.btn2_event)
      
        self.setLayout(self.pwd_v_layout)


        
    def btn1_update_pwd(self):
        old_pwd =  self.old_pwd_line.text()
        new_pwd = self.new_pwd2_line.text()
        new_pwd_2 = self.new_pwd3_line.text()
        if new_pwd != new_pwd_2:
            QMessageBox.critical(self, 'Wrong', '两次密码不一致')
        
        elif len(new_pwd) < 6 and len(new_pwd) > 16 :
            QMessageBox.critical(self, 'Wrong', '密码长度不能小于6位或大于16位')
            return
        elif old_pwd == new_pwd:
            QMessageBox.critical(self, 'Wrong', '新旧密码不能一致')
            return
        else:
            database = Database()
            item = database.c.execute("select password ,salt from admin where id_number = {0}".format(self.id_number)).fetchone()
            old_pass_word = MyMd5().create_md5(old_pwd, item["salt"])
            if old_pass_word == item["password"]:
                new_pass_word = MyMd5().create_md5(new_pwd, item["salt"])
                database.c.execute("update admin set password = ? where id_number = {0}".format(self.id_number),(new_pass_word,))
                database.conn.commit()
                database.conn.close()
                QMessageBox.information(self, 'Success', '修改成功')
                self.close()
            else:
                QMessageBox.critical(self, 'Wrong', '旧密码错误')
    #取消修改
    def btn2_event(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)    
    ui = AdminInformation()
    ui.show()
    app.exec_()

