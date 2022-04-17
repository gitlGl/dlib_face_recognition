
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt
from click import password_option
from src.Database import Database
from src.MyMd5 import MyMd5
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from src.GlobalVariable import models
from .Creatuser import CreatStudentUser
import PIL.Image,os,datetime
import numpy as np
from src.FaceLoginPage import FaceLoginPage
from .ImgPath import get_img_path
from .Check import check_user_id, check_user_pwd,verifye_pwd

class LoginUi(QWidget):
    emitsingal = pyqtSignal(str)
    emit_close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('登录')
        self.setWindowIcon(QIcon('resources/登录.png'))
        self.resize(400, 300)

        self.user_label = QLabel('Username:', self)
        self.pwd_label = QLabel('Password:', self)
        self.user_line = QLineEdit(self)
        self.pwd_line = QLineEdit(self)
        self.login_button = QPushButton('账号密码登录', self,objectName="GreenButton")
        self.signin_button = QPushButton('注册', self,objectName="GreenButton")
        self.face_login_button = QPushButton("人脸识别登录", self,objectName="GreenButton")

        #self.grid_layout = QGridLayout()
        self.h_user_layout = QHBoxLayout()
        self.h_password_layout = QHBoxLayout()
        self.h_in_layout = QHBoxLayout()

        self.v_layout = QVBoxLayout()

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()
        self.signin_page = SigninPage()  # 实例化SigninPage()

    def layout_init(self):
        self.h_user_layout.addWidget(self.user_label)
        self.h_user_layout.addWidget(self.user_line)
        self.h_password_layout.addWidget(self.pwd_label)
        self.h_password_layout.addWidget(self.pwd_line)
        self.h_in_layout.addWidget(self.login_button)
        self.h_in_layout.addWidget(self.face_login_button)
        self.h_in_layout.addWidget(self.signin_button)

        self.v_layout.addLayout(self.h_user_layout)
        self.v_layout.addLayout(self.h_password_layout)
        self.v_layout.addLayout(self.h_in_layout)

        self.setLayout(self.v_layout)

    def lineedit_init(self):
        self.user_line.setPlaceholderText('Please enter your usernumber')
        self.pwd_line.setPlaceholderText('Please enter your password')
        self.pwd_line.setEchoMode(QLineEdit.Password)

        self.user_line.textChanged.connect(self.check_input_func)
        self.pwd_line.textChanged.connect(self.check_input_func)

    #检查输入是否完成
    def check_input_func(self):
        if self.user_line.text() and self.pwd_line.text():
            self.login_button.setEnabled(True)
        else:
            self.login_button.setEnabled(False)

    def pushbutton_init(self):
        self.login_button.setEnabled(False)
        self.signin_button.clicked.connect(self.show_signin_page_func)
        self.login_button.clicked.connect(self.check_login_func)
        self.face_login_button.clicked.connect(self.face_login)

        #切换注册页面
    def show_signin_page_func(self):

        self.signin_page.show()

    #响应登录请求
    def check_login_func(self):
        def clear():
            self.pwd_line.clear()
            self.user_line.clear()

        uesr_id = self.user_line.text()
        user_pwd = self.pwd_line.text()

        if not check_user_id(uesr_id):
           QMessageBox.critical(self, '警告', '用户名只能为数字，且不能超过100位')
           return
        elif not check_user_pwd(user_pwd):
            QMessageBox.critical(self,'警告', '密码长度大于6位小于13位')
            return
        else:
            result = verifye_pwd(uesr_id,user_pwd)
            if result:
                self.emitsingal.emit(result)
                self.close()
            else:
                QMessageBox.warning(self, '警告', '账号或密码错误，请重新输入', QMessageBox.Yes)
                clear()
 #self.emitsingal.emit(item["id_number"])
    def face_login(self):
        self.face_login_page = FaceLoginPage()
        self.face_login_page.emit_show_parent.connect(self.rev)
#接受人脸识别登录成功信号，接收发送给主页面
    @pyqtSlot(str)
    def rev(self,id_number):
       
        self.emitsingal.emit(id_number)

    def closeEvent(self, Event):
        pass

        # p = os.getpid()
        # print("KILL")
        # print("KILL")
        # #psutil.Process(p).kill()
        # print("KILL")


class SigninPage(QWidget):
    def __init__(self):
        super(SigninPage, self).__init__()
        #self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('注册')
        self.setWindowIcon(QIcon('resources/注册.png'))
        self.signin_user_label = QLabel('用户:', self)
        self.signin_pwd_label = QLabel('密码:', self)
        self.signin_pwd2_label = QLabel('密码:', self)

        self.signin_user_line = QLineEdit(self)
        self.signin_pwd_line = QLineEdit(self)
        self.signin_pwd2_line = QLineEdit(self)
        self.signin_vector_button = QPushButton("图片:", self,objectName="GreenButton")
        self.signin_vector_button.setFlat(True)

        self.signin_vector_button.setIcon(QIcon("./resources/文件.png"))

        self.signin_vector_line = QLineEdit(self)
        self.signin_button = QPushButton('Sign in', self,objectName="GreenButton")

        self.user_h_layout = QHBoxLayout()
        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.vector_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()
        self.resize(300, 200)

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()

    def layout_init(self):
        self.user_h_layout.addWidget(self.signin_user_label)
        self.user_h_layout.addWidget(self.signin_user_line)
        self.pwd_h_layout.addWidget(self.signin_pwd_label)
        self.pwd_h_layout.addWidget(self.signin_pwd_line)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_label)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_line)
        self.vector_h_layout.addWidget(self.signin_vector_button)
        self.vector_h_layout.addWidget(self.signin_vector_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addLayout(self.vector_h_layout)
        self.all_v_layout.addWidget(self.signin_button)

        self.setLayout(self.all_v_layout)

    def lineedit_init(self):
        self.signin_pwd_line.setEchoMode(QLineEdit.Password)
        self.signin_pwd2_line.setEchoMode(QLineEdit.Password)

        self.signin_user_line.textChanged.connect(self.check_input_func)
        self.signin_pwd_line.textChanged.connect(self.check_input_func)
        self.signin_pwd2_line.textChanged.connect(self.check_input_func)
        self.signin_vector_line.textChanged.connect(self.check_input_func)
        self.signin_vector_button.clicked.connect(self.get_path)

    def check_input_func(self):
        if self.signin_user_line.text() and self.signin_pwd_line.text(
        ) and self.signin_pwd2_line.text() and self.signin_vector_line.text():
            self.signin_button.setEnabled(True)
        else:
            self.signin_button.setEnabled(False)

        #self.signin_vector_line.setText(path)
        #self.signin_vector_line.clear()
    def get_path(self):
        path = get_img_path(self)
        if path :
            self.path = path
            self.signin_vector_line.setText(path)
            print(path)
            return 
       

       

    def pushbutton_init(self):
        self.signin_button.setEnabled(False)
        self.signin_button.clicked.connect(self.check_signin_func)
 #响应注册请求
    def check_signin_func(self):
        admin = Database()

        #检查输入信息格式
        if (not self.signin_user_line.text().isdigit()) or (len(self.signin_user_line.text())>15):

            QMessageBox.critical(self, 'Wrong', 'Usernumber is only digit or is too long!')

            return
        elif self.signin_pwd_line.text() != self.signin_pwd2_line.text():
            QMessageBox.critical(self, 'Wrong',
                                 'Two Passwords Typed Are Not Same!')

            return

        elif len(self.signin_pwd_line.text()) < 6 or len(
                self.signin_pwd_line.text()) > 13:
            QMessageBox.critical(self, 'Wrong', ' Passwords is too short!')

            return
        else:
            user_name = self.signin_user_line.text()
            user = admin.c.execute(
                "select id_number from admin where id_number = {} ".format(
                    user_name)).fetchall()
            if len(user) == 1:
                QMessageBox.critical(self, 'Wrong',
                                     'This Username Has Been Registered!')

                return
            else:

                user_name = self.signin_user_line.text()
                pass_word = self.signin_pwd_line.text()
                salt = MyMd5().create_salt()
                pass_word = MyMd5().create_md5(pass_word, salt)

                creat_user = CreatStudentUser()

                vector = creat_user.get_vector(user_name,
                                               self.path,
                                               "admin")

                admin.c.execute(
                    "INSERT INTO admin (id_number,password,salt,vector) \
      VALUES (?, ?,?,?)", (user_name, pass_word, salt, vector))
                QMessageBox.information(self, 'Information',
                                        'Register Successfully')
                admin.conn.commit()
                admin.conn.close()
               
                self.close()
               