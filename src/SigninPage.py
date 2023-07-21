from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox,QApplication
from PyQt5.QtCore import Qt
from .GlobalVariable import database
from .MyMd5 import MyMd5
from PyQt5.QtGui import QIcon
from .Creatuser import CreatUser
from .Check import getImgPath, checkPath,checkVerifye,createMd5
from .GlobalVariable import admin
from .Check import getImgPath, checkPath
import uuid
from .Check import aes
from .Database import PH
class SigninPage(QWidget):
    def __init__(self):
        super(SigninPage, self).__init__()
        # self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('注册')
        self.setWindowIcon(QIcon('resources/注册.svg'))
        self.signin_user_label = QLabel('输入用户:', self)
        self.signin_pwd_label = QLabel('输入密码:', self)
        self.signin_pwd2_label = QLabel('确认密码:', self)
        self.verifye_label = QLabel('验证码:', self)

        self.signin_user_line = QLineEdit(self)
        self.signin_pwd_line = QLineEdit(self)
        self.signin_pwd2_line = QLineEdit(self)
        self.verifye_line = QLineEdit(self)
        self.signin_vector_button = QPushButton(
            "图片:", self, objectName="GreenButton")
        self.signin_vector_button.setFlat(True)

        self.signin_vector_button.setIcon(QIcon("resources/文件.svg"))

        self.signin_vector_line = QLineEdit(self)
        self.signin_button = QPushButton('注册', self,objectName="GreenButton")

        self.user_h_layout = QHBoxLayout()
        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.verifye_lyout = QHBoxLayout()
        self.vector_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()
        self.resize(300, 238)

        self.lineeditInit()
        self.pushButtonInit()
        self.layoutInit()

    def layoutInit(self):

        self.user_h_layout.addWidget(self.signin_user_label)
        self.user_h_layout.addWidget(self.signin_user_line)

        self.pwd_h_layout.addWidget(self.signin_pwd_label)
        self.pwd_h_layout.addWidget(self.signin_pwd_line)

        self.pwd2_h_layout.addWidget(self.signin_pwd2_label)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_line)

        self.verifye_lyout.addSpacing(12)
        self.verifye_lyout.addWidget(self.verifye_label)
        self.verifye_lyout.addWidget(self.verifye_line)

        self.vector_h_layout.addSpacing(5)
        self.vector_h_layout.addWidget(self.signin_vector_button)
        self.vector_h_layout.addWidget(self.signin_vector_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addLayout(self.verifye_lyout)
        self.all_v_layout.addLayout(self.vector_h_layout)
        self.all_v_layout.addWidget(self.signin_button)

        self.setLayout(self.all_v_layout)

    def lineeditInit(self):
        self.signin_pwd_line.setEchoMode(QLineEdit.Password)
        self.signin_pwd2_line.setEchoMode(QLineEdit.Password)

        self.signin_user_line.textChanged.connect(self.checkInputFunc)
        self.signin_pwd_line.textChanged.connect(self.checkInputFunc)
        self.signin_pwd2_line.textChanged.connect(self.checkInputFunc)
        self.verifye_line.textChanged.connect(self.checkInputFunc)
        self.signin_vector_line.textChanged.connect(self.checkInputFunc)
        self.signin_vector_button.clicked.connect(self.getPath)

    def checkInputFunc(self):
        if self.signin_user_line.text() and self.signin_pwd_line.text(
        ) and self.signin_pwd2_line.text() and self.signin_vector_line.text(

        ) and self.verifye_line.text():
            self.signin_button.setEnabled(True)
        else:
            self.signin_button.setEnabled(False)

        # self.signin_vector_line.setText(path)
        # self.signin_vector_line.clear()
    def getPath(self):
        path = getImgPath(self)
        if path:
            self.signin_vector_line.setText(path)
            return 
       

    def pushButtonInit(self):
        self.signin_button.setEnabled(False)
        self.signin_button.clicked.connect(self.checkSigninFunc)
 # 响应注册请求

    def checkSigninFunc(self):
        user_name = self.signin_user_line.text()
        password = self.signin_pwd_line.text()
        password2 = self.signin_pwd2_line.text()
            

        #检查输入信息格式
        if not user_name.isnumeric() or len(user_name) > admin.id_length.value:
            QMessageBox.critical(self, '警告', f'用户名只能是数字且少于{admin.id_length.value}位!')
            return

        if password != password2:
            QMessageBox.critical(self, '警告', '两个密码不同!')
            return

        if not admin.password_min_length.value <= len(password) <= admin.password_max_length.value:
            QMessageBox.critical(self, '警告', f'密码长度必须在{admin.password_min_length.value}到{admin.password_max_length.value}之间!')
            return
        user = database.execute(
            "select id_number from admin where id_number = {} ".format(
                user_name))
        if len(user) == 1:
            QMessageBox.critical(self, '警告',
                                    '该用户已被注册!')

            return

      
        verifye = self.verifye_line.text()
        if not '_'  in verifye:
            QMessageBox.critical(None, '警告', '验证码错误')
            return
        path = self.signin_vector_line.text()
        if not checkPath(path,self):
            return
        
        self.signin_button.setText('注册中...')
        self.signin_button.setEnabled(False)
        QApplication.processEvents()
        
       
        creatuser = CreatUser()
        vector = creatuser.getVector(path)
        verifye_md5 = createMd5(verifye, uuid.uuid1().hex[-12:])
        vector_md5 = createMd5(vector, uuid.uuid1().hex[-12:])
        private_verifye = aes.encrypt(verifye_md5, verifye)
        private_vector = aes.encrypt(vector_md5, verifye)#使用验证码加密

      
        data = {'id':verifye.split("_")[1],'verifye': private_verifye, 'vector': private_vector,"flag":'resgister'
        ,"mac_address":uuid.uuid1().hex[-12:]}
        flag = checkVerifye(data)
        if  flag != True:
            QMessageBox.critical(self, '警告', flag)
            self.signin_button.setText('注册')
            self.signin_button.setEnabled(True)
            return
       
        salt = MyMd5.createSalt()
        password = MyMd5.createMd5(password, salt,user_name)
        
       
        creatuser.insertImg(user_name, path, "admin")

        database.execute(
            f"INSERT INTO admin (id_number,password,salt,vector) \
VALUES ({PH}, {PH},{PH},{PH})", (user_name, password, salt, vector))
        QMessageBox.information(self, '信息',
                                '注册成功!')
        self.signin_user_line.clear()
        self.signin_pwd_line.clear()
        self.signin_pwd2_line.clear()
        self.signin_vector_line.clear()
        self.close()
        return
