from .ShowLog import ShowLog
from .ImageView import ImageView
from .GlobalVariable import database
from .ImageView import ShowImage
from .Creatuser import CreatUser
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QGroupBox,QPushButton,\
QMessageBox, QMenu,QWidget
from .Check import getImgPath
from .UpdateUser import UpdatePwd
from .ShowUser import ShowUser
from .Database import PH
class AdminInformation(QWidget):
    def __init__(self,id_number):
        super().__init__()
        self.id_number = id_number
        #self.setGeometry(400, 400,500, 480)
        self.resize(480, 600)
        self.setWindowTitle('用户信息')
        self.setWindowIcon(QIcon('resources/用户信息.svg'))
        self.setWindowModality(Qt.ApplicationModal)
        

        self.Hlayout = QHBoxLayout()
        self.Vhlayout = QVBoxLayout()
        
        #self.linnedit.setFixedSize(400,15)
        
        self.grou = QGroupBox(self)
        self.img = ImageView("resources/bg.jpg",Qt.black)
        self.id_label = QLabel(self)
        self.id_label.setText("用户ID：{}".format(self.id_number))
        self.face_picture_btn1 = QPushButton()
        self.face_picture_btn1 = QPushButton(objectName="GreenButton")
       
        self.update_pwd_btn = QPushButton()
        self.update_pwd_btn = QPushButton(objectName="GreenButton")
        
        self.face_picture_btn1.setText("人脸照片")
        self.face_picture_btn1.clicked.connect(lambda:self.imgEvent(self.face_picture_btn1.pos()))
        self.update_pwd_btn.setText("修改密码")
        self.update_pwd_btn.clicked.connect(self.updatePwd)
        self.login_log_btn = QPushButton()
        self.login_log_btn = QPushButton(objectName="GreenButton")
        self.login_log_btn.clicked.connect(self.browse)
        self.login_log_btn.setText("登录日志")
        self.Hlayout.addWidget(self.id_label)
        self.Hlayout.addWidget(self.face_picture_btn1)
        self.Hlayout.addWidget(self.update_pwd_btn)
        self.Hlayout.addWidget(self.login_log_btn)
        if self.id_number == "12345678910" :
           self.user_admin_btn = QPushButton()
           self.user_admin_btn = QPushButton(objectName="GreenButton")
           self.user_admin_btn.setText("用户管理")
           self.user_admin_btn.clicked.connect(self.root)
           self.Hlayout.addWidget(self.user_admin_btn)
        self.grou.setLayout(self.Hlayout)
        self.Vhlayout.addWidget(self.grou)
        self.qlabel_ = QLabel(self)
        self.Vhlayout.addWidget(self.qlabel_)
        #self.Vhlayout.addWidget(self.img)
        self.grou.setMaximumSize(600,40)
        self.resize(480, 600)
        self.setLayout(self.Vhlayout)
    def updatePwd(self):
        self.pwd_dialog = UpdatePwd(self.id_number)
        self.pwd_dialog.exec_()
    def browse(self):
        self.result = ShowLog(self.id_number,[ '用户ID', '登录时间',"图片" ],
        "admin",['id','id_number','log_time'])
        item = self.Vhlayout.itemAt(1)
        item.widget().deleteLater()
        self.Vhlayout.removeItem(item)
        self.Vhlayout.addWidget(self.result)

    def imgEvent(self,pos):
       pop_menu = QMenu() 
       pop_menu.addAction("查看图片")
       pop_menu.addAction("修改图片")
       action = pop_menu.exec_(self.mapToGlobal(pos))
       if action == pop_menu.actions()[0]:
           item = self.Vhlayout.itemAt(1)
           item.widget().deleteLater()
           self.Vhlayout.removeItem(item)
           img_path = "img_information/admin/{0}/{1}.jpg".format(str(self.id_number),str(self.id_number))
           show_imag = ShowImage(img_path,Qt.WhiteSpaceMode)
           self.Vhlayout.addWidget(show_imag)
       elif action == pop_menu.actions()[1]:

           path = getImgPath(self)
           if path:
              creatuser = CreatUser()
              vector = creatuser.getVector(path)
              creatuser.insertImg(self.id_number,path,"admin")
              database.execute("update admin set vector = {0} where id_number = {1}".format(PH,self.id_number),(vector,))
              QMessageBox.information(self, 'Success', '修改成功')
   
    def root(self):
        result = database.execute("select id_number,password from admin ")
        show_admin_User = ShowUser('admin',result)
        item = self.Vhlayout.itemAt(1)
        item.widget().deleteLater()
        self.Vhlayout.removeItem(item)
        self.Vhlayout.addWidget(show_admin_User)
        pass
#密码修改窗口

