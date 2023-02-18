
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox,QCheckBox
from PyQt5.QtCore import pyqtSignal
from src.GlobalVariable import database
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
import datetime,uuid
from src.FaceLoginPage import FaceLoginPage
from .Check import checkUserId, checkUserPwd,verifyePwd
from .SigninPage import SigninPage
import configparser,base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
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
        self.remember_password = QCheckBox("记住密码")
        self.face_login_button = QPushButton("人脸识别登录", self,objectName="GreenButton")

        #self.grid_layout = QGridLayout()
        self.h_user_layout = QHBoxLayout()
        self.h_password_layout = QHBoxLayout()
        self.h_in_layout = QHBoxLayout()

        self.v_layout = QVBoxLayout()

        self.lineeditInit()
        self.pushbuttonInit()
        self.layoutInit()
        self.config = configRemberPwd()
        if not self.config.checkFlag():
            return
        self.remember_password.setChecked(True)
        dic = self.config.get()
        
        result = self.config.decrypt(dic["pwd"])
        if result:
            self.user_line.setText(dic["id"])
            self.pwd_line.setText(self.config.decrypt(dic["pwd"]))
        
    def layoutInit(self):
        self.h_user_layout.addWidget(self.user_label)
        self.h_user_layout.addWidget(self.user_line)
        self.h_password_layout.addWidget(self.pwd_label)
        self.h_password_layout.addWidget(self.pwd_line)
        self.h_in_layout.addWidget(self.login_button)
        self.h_in_layout.addStretch(1)
        self.h_in_layout.addWidget(self.face_login_button)
        self.h_in_layout.addStretch(1)
        self.h_in_layout.addWidget(self.remember_password)
        self.h_in_layout.addStretch(1)
        self.h_in_layout.addWidget(self.signin_button)
        self.h_in_layout.addStretch(1)

        self.v_layout.addLayout(self.h_user_layout)
        self.v_layout.addLayout(self.h_password_layout)
        self.v_layout.addLayout(self.h_in_layout)

        self.setLayout(self.v_layout)

    def lineeditInit(self):
        self.user_line.setPlaceholderText('Please enter your usernumber')
        self.pwd_line.setPlaceholderText('Please enter your password')
        self.pwd_line.setEchoMode(QLineEdit.Password)

        self.user_line.textChanged.connect(self.checkInputFunc)
        self.pwd_line.textChanged.connect(self.checkInputFunc)

    #检查输入是否完成
    def checkInputFunc(self):
        if self.user_line.text() and self.pwd_line.text():
            self.login_button.setEnabled(True)
        else:
            self.login_button.setEnabled(False)

    def pushbuttonInit(self):
        self.login_button.setEnabled(False)
        self.signin_button.clicked.connect(self.showSigninPageFunc)
        self.login_button.clicked.connect(self.checkLoginFunc)
        self.face_login_button.clicked.connect(self.faceLogin)
        self.remember_password.clicked.connect(self.setConfigFlag)
        #切换注册页面
    def showSigninPageFunc(self):
        self.signin_page = SigninPage()  # 实例化SigninPage()
        self.signin_page.show()

    def setConfigFlag(self):
        if self.remember_password.isChecked():
            self.config.setFlag("1")
        else:
            self.config.setFlag("0")
            self.config.setPwdId('','')
        
        
    #响应登录请求
    def checkLoginFunc(self):
        def clear():
            self.pwd_line.clear()
            self.user_line.clear()

        uesr_id = self.user_line.text()
        user_pwd = self.pwd_line.text()

        if not checkUserId(uesr_id):
           QMessageBox.critical(self, '警告', '用户名只能为数字，且不能超过100位')
           return
        if not checkUserPwd(user_pwd):
            QMessageBox.critical(self,'警告', '密码长度大于6位小于13位')
            return
    
        result = verifyePwd(uesr_id,user_pwd,"admin")
        if not result:
            QMessageBox.warning(self, '警告', '账号或密码错误，请重新输入', QMessageBox.Yes)
            clear()
            return
        
        database.c.execute("INSERT INTO admin_log_time (id_number,log_time ) \
VALUES (?,?)", (uesr_id, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))
        database.conn.commit()
        if self.remember_password.isChecked():
            self.config.setPwdId(self.user_line.text(),self.config.encrypt(self.pwd_line.text()))
        self.emitsingal.emit(uesr_id)
        self.close()
           
 #self.emitsingal.emit(item["id_number"])
    def faceLogin(self):
        self.face_login_page = FaceLoginPage()
        self.face_login_page.emit_show_parent.connect(self.rev)
#接受人脸识别登录成功信号，接收发送给主页面
    @pyqtSlot(str)
    def rev(self,id_number):
       
        self.emitsingal.emit(id_number)

    

class  configRemberPwd():
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        # 打开 ini 文件
        self.config.read("cfg.ini", encoding="utf-8") 
    def checkFlag(self) -> bool:
        if self.config["rember_pwd"]["flag"] == "0":
            return False
        return True
    def get(self):
        return dict(self.config["rember_pwd"])

    def setFlag(self,flag):
        self.config["rember_pwd"]["flag"] = flag
        with open("cfg.ini", "w", encoding="utf-8") as f:
            self.config.write(f)

    def setPwdId(self,id,pwd):
        self.config["rember_pwd"]["id"] = id
        self.config["rember_pwd"]["pwd"] = pwd
        with open("cfg.ini", "w", encoding="utf-8") as f:
            self.config.write(f)
    
    def encrypt(self,data):
        mac_address = uuid.uuid1().hex[-12:]
        key = pad(mac_address.encode("utf8"),AES.block_size)
        cipher = AES.new(key,AES.MODE_ECB)
        plaintext = data.encode('utf8')
        msg = cipher.encrypt(pad(plaintext,AES.block_size))
        result = str(base64.b64encode(msg).decode('utf8'))
        return result

    def decrypt(self,data):
        mac_address = uuid.uuid1().hex[-12:]
        key = pad(mac_address.encode("utf8"),AES.block_size)
        cipher = AES.new(key,AES.MODE_ECB)
        try:
            plaintext = base64.b64decode(data.encode("utf8"))
            msg = unpad(cipher.decrypt(plaintext),AES.block_size)
            result = str(msg.decode('utf8'))
            return result
        except:
            return False
       


