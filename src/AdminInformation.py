from .ShowLog import ShowLog
from .ImageView import ImageView
from .Database import Database
from .ImageView import ShowImage
from .Creatuser import CreatUser
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QGroupBox,QPushButton,\
QMessageBox, QMenu,QWidget
from .ImgPath import get_img_path
from .UpdatePwd import UpdatePwd
from .ShowUser import ShowAdminUser
class AdminInformation(QWidget):
    def __init__(self,id_number):
        super().__init__()
        self.id_number = id_number
        #self.setGeometry(400, 400,500, 480)
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
        if self.id_number == "12345678910" :
           self.btn4 = QPushButton()
           self.btn4 = QPushButton(objectName="GreenButton")
           self.btn4.setText("用户管理")
           self.btn4.clicked.connect(self.root)
           self.Hlayout.addWidget(self.btn4)
        self.grou.setLayout(self.Hlayout)
        self.Vhlayout.addWidget(self.grou)
        self.qlabel_ = QLabel(self)
        self.Vhlayout.addWidget(self.qlabel_)
        #self.Vhlayout.addWidget(self.img)
        self.grou.setMaximumSize(600,40)
        self.resize(480, 600)
        self.setLayout(self.Vhlayout)
    def update_pwd(self):
        self.pwd_dialog = UpdatePwd(self.id_number)
        self.pwd_dialog.exec_()
    def browse(self):
        self.result = ShowLog(self.id_number,[ '用户ID', '登录时间',"图片" ],
        "admin",['rowid','id_number','log_time'])
        self.Vhlayout.itemAt(1).widget().deleteLater()
        self.Vhlayout.addWidget(self.result)

    def img_event(self,pos):
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

           path = get_img_path(self)
           if path:
              creatuser = CreatUser()
              vector = creatuser.get_vector(path)
              creatuser.insert_img(self.id_number,path,"admin")
              database = Database()
              database.c.execute("update admin set vector = ? where id_number = {0}".format(self.id_number),(vector,))
            
              database.conn.close()
              QMessageBox.information(self, 'Success', '修改成功')
   
    def root(self):
        result = Database().c.execute("select id_number,password from admin ").fetchall()
        self.result = ShowAdminUser([ '用户ID', '密码',"图片" ],'admin',["id_number",'password'],result)
        self.Vhlayout.itemAt(1).widget().deleteLater()
        self.Vhlayout.addWidget(self.result)
        pass
#密码修改窗口

