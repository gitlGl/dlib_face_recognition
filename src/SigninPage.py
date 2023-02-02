from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from src.Database import database
from src.MyMd5 import MyMd5
from PyQt5.QtGui import QIcon
from .Creatuser import CreatUser
from .Check import get_img_path

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
            return 
       

       

    def pushbutton_init(self):
        self.signin_button.setEnabled(False)
        self.signin_button.clicked.connect(self.check_signin_func)
 #响应注册请求
    def check_signin_func(self):
        

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
        salt = MyMd5().create_salt()
        pass_word = MyMd5().create_md5(pass_word, salt)
        creatuser = CreatUser()
        vector = creatuser.get_vector(self.path)
        creatuser.insert_img(user_name,self.path,"admin")

        database.c.execute(
            "INSERT INTO admin (id_number,password,salt,vector) \
VALUES (?, ?,?,?)", (user_name, pass_word, salt, vector))
        QMessageBox.information(self, 'Information',
                                'Register Successfully')
        
        self.close()
        return
            
