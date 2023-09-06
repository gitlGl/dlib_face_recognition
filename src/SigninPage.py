from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt,QRegularExpression
from .Database import database
from . import encryption
from PySide6.QtGui import QIcon
from . import CreatUser
from  . import Check
from .Database import PH
from .Setting import user,isVerifyeRemote
from .Check import *
from PySide6.QtGui import QRegularExpressionValidator
from .encryption import *
from PySide6.QtWidgets import QApplication
from .CreatUser import *
class SigninPage(QWidget):
    def __init__(self):
        super(SigninPage, self).__init__()
        #self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('注册')
        self.setWindowIcon(QIcon('resources/注册.svg'))
        self.signin_user_label = QLabel('输入用户:', self)
        self.signin_pwd_label = QLabel('输入密码:', self)
        self.signin_pwd2_label = QLabel('确认密码:', self)


        self.signin_user_line = QLineEdit(self)
        validator = QRegularExpressionValidator(QRegularExpression("[0-9]*"))
        self.signin_user_line.setValidator(validator)
        self.signin_user_line.setMaxLength(user.id_length.value)
        self.signin_user_line.setPlaceholderText("请输入数字,不大于{0}位".format(user.id_length.value))

        
        self.signin_pwd_line = QLineEdit(self)
        validator = QRegularExpressionValidator(QRegularExpression(user.reg_pwd.value))
        self.signin_pwd_line.setValidator(validator)
        self.signin_pwd_line.setMaxLength(20)
        self.signin_pwd_line.setPlaceholderText("请输入密码,不大于{0}位".format(user.password_max_length.value))

        self.signin_pwd2_line = QLineEdit(self)
        validator = QRegularExpressionValidator(QRegularExpression(user.reg_pwd.value))
        self.signin_pwd2_line.setValidator(validator)
        self.signin_pwd2_line.setMaxLength(20)

       
        self.signin_vector_button = QPushButton("图片:",self,objectName="GreenButton")
        self.signin_vector_button.setFlat(True)

        self.signin_vector_button.setIcon(QIcon("resources/文件.svg"))

        self.signin_vector_line = QLineEdit(self)
        self.signin_button = QPushButton('注册', self,objectName="GreenButton")

        self.user_h_layout = QHBoxLayout()
        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
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

        self.vector_h_layout.addSpacing(5)
        self.vector_h_layout.addWidget(self.signin_vector_button)
        self.vector_h_layout.addWidget(self.signin_vector_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
     
 
        if isVerifyeRemote:
            self.verifye_label = QLabel('验证码:', self)
            self.verifye_line = QLineEdit(self)
            validator = QRegularExpressionValidator(QRegularExpression("^[_0-9]*$"))
            self.verifye_line.setValidator( validator)
            self.verifye_lyout = QHBoxLayout()
            self.verifye_lyout.addSpacing(12)
            self.verifye_lyout.addWidget(self.verifye_label)
            self.verifye_lyout.addWidget(self.verifye_line)
            self.all_v_layout.addLayout(self.verifye_lyout)
            self.verifye_line.textChanged.connect(self.checkInputFunc)

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
            
            if isVerifyeRemote:
                if self.verifye_line.text():
                    self.signin_button.setEnabled(True)
                else: self.signin_button.setEnabled(False)
                    
            else:
                self.signin_button.setEnabled(True)
        else:
            self.signin_button.setEnabled(False)
       
        #self.signin_vector_line.setText(path)
        #self.signin_vector_line.clear()
    def getPath(self):
        path = Check.getImgPath(self)
        if path :
            self.signin_vector_line.setText(path)
            return 
       

    def pushButtonInit(self):
        self.signin_button.setEnabled(False)
        self.signin_button.clicked.connect(self.checkSigninFunc)
 #响应注册请求
    def checkSigninFunc(self):
        user_name = self.signin_user_line.text()
        password = self.signin_pwd_line.text()
        password2 = self.signin_pwd2_line.text()
        path = self.signin_vector_line.text()
            
        #检查输入信息格式
        if not user_name.isnumeric() or len(user_name) > user.id_length.value:
            Check.id_number_info(self)
            return

        if password != password2:
            QMessageBox.critical(self, '警告', '两个密码不同!')
            return

        if not user.password_min_length.value <= len(password) <= user.password_max_length.value:
            Check.password_info(self)
            return
        user_ = database.execute(
            "select id_number from admin where id_number = {} ".format(
                user_name))
        if len(user_) == 1:
            QMessageBox.critical(self, '警告',
                                    '该用户已被注册!')

            return
    
       
        if not Check.checkPath(path,self):
            return
        if isVerifyeRemote:
            if not self.verifyeSignin():
                return

        salt = encryption.createSalt()
        password = createMd5(password, salt,user_name)
        vector = CreatUser.getVector(path)
        CreatUser.insertImg(user_name,path,"admin")

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
            
    def verifyeSignin(self):
        verifye = self.verifye_line.text()
        if not '_'  in verifye:
            QMessageBox.critical(None, '警告', '验证码错误')
            return False
        path = self.signin_vector_line.text()
        if not checkPath(path,self):
            return False
        
        self.signin_button.setText('注册中...')
        self.signin_button.setEnabled(False)
        QApplication.processEvents()
        
        
        vector = getVector(path)
        verifye_md5 = createMd5Verifye(verifye, uuid.uuid1().hex[-12:])
        vector_md5 = createMd5Verifye(vector, uuid.uuid1().hex[-12:])
        private_verifye = aes.encrypt(verifye_md5, verifye)
        private_vector = aes.encrypt(vector_md5, verifye)#使用验证码加密

      
        data = {'id':verifye.split("_")[1],'verifye': private_verifye, 'vector': private_vector,"flag":'resgister'
        ,"mac_address":uuid.uuid1().hex[-12:]}
        flag = checkVerifye(data)
        if  flag != True:
            QMessageBox.critical(self, '警告', flag)
            self.signin_button.setText('注册')
            self.signin_button.setEnabled(True)
            return False
        return True
