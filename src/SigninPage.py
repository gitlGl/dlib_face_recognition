from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from src.GlobalVariable import database
from src.MyMd5 import MyMd5
from PyQt5.QtGui import QIcon
from .Creatuser import CreatUser
from .Check import getImgPath

class SigninPage(QWidget):
    def __init__(self):
        super(SigninPage, self).__init__()
        #self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('注册')
        self.setWindowIcon(QIcon('resources/注册.png'))
        self.signin_user_label = QLabel('输入用户:', self)
        self.signin_pwd_label = QLabel('输入密码:', self)
        self.signin_pwd2_label = QLabel('确认密码:', self)

        self.signin_user_line = QLineEdit(self)
        self.signin_pwd_line = QLineEdit(self)
        self.signin_pwd2_line = QLineEdit(self)
        self.signin_vector_button = QPushButton(" 图片:",self,objectName="GreenButton")
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
        self.vector_h_layout.addWidget(self.signin_vector_button)
        self.vector_h_layout.addWidget(self.signin_vector_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addLayout(self.vector_h_layout)
        self.all_v_layout.addWidget(self.signin_button)

        self.setLayout(self.all_v_layout)

    def lineeditInit(self):
        self.signin_pwd_line.setEchoMode(QLineEdit.Password)
        self.signin_pwd2_line.setEchoMode(QLineEdit.Password)

        self.signin_user_line.textChanged.connect(self.checkInputFunc)
        self.signin_pwd_line.textChanged.connect(self.checkInputFunc)
        self.signin_pwd2_line.textChanged.connect(self.checkInputFunc)
        self.signin_vector_line.textChanged.connect(self.checkInputFunc)
        self.signin_vector_button.clicked.connect(self.getPath)

    def checkInputFunc(self):
        if self.signin_user_line.text() and self.signin_pwd_line.text(
        ) and self.signin_pwd2_line.text() and self.signin_vector_line.text():
            self.signin_button.setEnabled(True)
        else:
            self.signin_button.setEnabled(False)

        #self.signin_vector_line.setText(path)
        #self.signin_vector_line.clear()
    def getPath(self):
        path = getImgPath(self)
        if path :
            self.path = path
            self.signin_vector_line.setText(path)
            return 
       

       

    def pushButtonInit(self):
        self.signin_button.setEnabled(False)
        self.signin_button.clicked.connect(self.checkSigninFunc)
 #响应注册请求
    def checkSigninFunc(self):
        

        #检查输入信息格式
        if (not self.signin_user_line.text().isdigit()) or (len(self.signin_user_line.text())>15):

            QMessageBox.critical(self, 'Wrong', 'Usernumber is only digit or is too long!')

            return
        if self.signin_pwd_line.text() != self.signin_pwd2_line.text():
            QMessageBox.critical(self, 'Wrong',
                                 'Two Passwords Typed Are Not Same!')

            return

        if len(self.signin_pwd_line.text()) < 6 or len(
                self.signin_pwd_line.text()) > 13:
            QMessageBox.critical(self, 'Wrong', ' Passwords is too short or too long!')

            return
    
        user_name = self.signin_user_line.text()
        user = database.c.execute(
            "select id_number from admin where id_number = {} ".format(
                user_name)).fetchall()
        if len(user) == 1:
            QMessageBox.critical(self, 'Wrong',
                                    'This Username Has Been Registered!')

            return
    

        user_name = self.signin_user_line.text()
        pass_word = self.signin_pwd_line.text()
        salt = MyMd5().createSalt()
        pass_word = MyMd5().createMd5(pass_word, salt,user_name)
        creatuser = CreatUser()
        vector = creatuser.getVector(self.path)
        creatuser.insertImg(user_name,self.path,"admin")

        database.c.execute(
            "INSERT INTO admin (id_number,password,salt,vector) \
VALUES (?, ?,?,?)", (user_name, pass_word, salt, vector))
        QMessageBox.information(self, 'Information',
                                'Register Successfully')

        
        self.signin_user_line.clear()
        self.signin_pwd_line.clear()
        self.signin_pwd2_line.clear()
        self.signin_vector_line.clear()
        
        self.close()
        return
            
