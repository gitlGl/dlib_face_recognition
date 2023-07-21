
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox,QCheckBox
from PySide6.QtCore import Signal
from .GlobalVariable import database
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
import datetime,uuid
from .FaceLoginPage import FaceLoginPage
from .Check import checkUserId, checkUserPwd,verifyePwd
from .SigninPage import SigninPage
import configparser,base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import configparser
from .Database import PH
#from PySide6 import QString
class LoginUi(QWidget):
    emitsingal = Signal(str)
    emit_close = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('登录')
        self.setWindowIcon(QIcon( 'resources/登录.svg'))
        self.resize(400, 300)
        self.user_label = QLabel('Username:', self)
        self.pwd_label = QLabel('Password:', self)
        self.user_line = QLineEdit(self)
        self.pwd_line = QLineEdit(self)
        self.login_button = QPushButton('登录', self,objectName="GreenButton")
        self.signin_button = QPushButton('注册', self,objectName="GreenButton")
        self.remember_password = QCheckBox("记住密码")
        self.auto_login = QCheckBox("自动登录")
        self.face_login_button = QPushButton("人脸识别登录", self,objectName="GreenButton")

        #self.grid_layout = QGridLayout()
        self.h_user_layout = QHBoxLayout()
        self.h_password_layout = QHBoxLayout()
        self.h_in_layout = QHBoxLayout()

        self.v_layout = QVBoxLayout()
        self.config_rember_pwd = configRemberPwd()
        self.config_auto_login = configAotuLogin()
        self.lineeditInit()
        self.pushbuttonInit()
        self.layoutInit()
       
    def initRemberPwd(self):
        if  not self.config_rember_pwd.checkFlag():
            return False

        else:
            self.remember_password.setChecked(True)
        if not self.config_rember_pwd.checkTime():
            self.remember_password.setChecked(False)
            return True
        
        self.user_line.setText(self.config_rember_pwd.result["id_number"])
        self.pwd_line.setText(self.config_rember_pwd.result['password'])
        return False
    def initAutoLogin(self):
        if not self.config_auto_login.checkFlag():
            return False
        if not self.config_auto_login.checkTime():
            self.auto_login.setChecked(False)
            return True
        return False
    def layoutInit(self):
        self.h_user_layout.addWidget(self.user_label)
        self.h_user_layout.addWidget(self.user_line)
        self.h_password_layout.addWidget(self.pwd_label)
        self.h_password_layout.addWidget(self.pwd_line)
    

        self.h_in_layout.addStretch(1)
        self.h_in_layout.addWidget(self.login_button)
        self.h_in_layout.addStretch(1)
        self.h_in_layout.addWidget(self.face_login_button)
        self.h_in_layout.addStretch(1)
        self.h_in_layout.addWidget(self.remember_password)
        self.h_in_layout.addStretch(1)
        self.h_in_layout.addWidget(self.auto_login)
        self.h_in_layout.addStretch(1)
        self.h_in_layout.addWidget(self.signin_button)
        self.h_in_layout.addStretch(1)
        self.v_layout.addStretch(1)
        self.v_layout.addLayout(self.h_user_layout)
        self.v_layout.addStretch(1)
        self.v_layout.addLayout(self.h_password_layout)
        self.v_layout.addStretch(1.5)
        if self.initRemberPwd()  or self.initAutoLogin():
            qlbel = QLabel("记住密码或自动登录超时或未知错误")
            qlbel.setStyleSheet("font-size:12px;color:red")
            self.h_tips = QHBoxLayout()
            self.config_auto_login.setStates('')
            self.config_auto_login.setFlag('0')
            self.config_rember_pwd.setFlag("0")
            self.config_rember_pwd.setPwd('')
            self.h_tips.addStretch(1)
            self.h_tips.addWidget(qlbel)
            self.h_tips.addStretch(1)
            self.v_layout.addLayout(self.h_tips)
            self.v_layout.addStretch(1.5)
        self.v_layout.addLayout(self.h_in_layout)
        self.v_layout.addStretch(1)
        self.setLayout(self.v_layout)

    def lineeditInit(self):
        self.user_line.setPlaceholderText('请输入用户名')
        self.pwd_line.setPlaceholderText('请输入用户密码')
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
        self.remember_password.clicked.connect(self.setRemberConfigFlag)
        #切换注册页面
    def showSigninPageFunc(self):
        self.signin_page = SigninPage()  # 实例化SigninPage()
        self.signin_page.show()

    def setRemberConfigFlag(self):
        if not self.remember_password.isChecked():
            self.config_rember_pwd.setFlag("0")
            self.config_rember_pwd.setPwd('')

           
        
    #响应登录请求
    def checkLoginFunc(self):
        def clear():
            self.pwd_line.clear()
            self.user_line.clear()

        user_id = self.user_line.text()
        user_pwd = self.pwd_line.text()

        if not checkUserId(user_id):
           QMessageBox.critical(self, '警告', '用户名只能为数字，且不能超过20个数字')
           return
        if not checkUserPwd(user_pwd):
            QMessageBox.critical(self,'警告', '密码长度大于6位小于13位')
            return
    
        result = verifyePwd(user_id,user_pwd,"admin")
        if not result:
            QMessageBox.warning(self, '警告', '账号或密码错误，请重新输入')
            clear()
            return
        
        database.execute(f"INSERT INTO admin_log_time (id_number ) \
VALUES ({PH})", (user_id, ))
        
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        
        if self.remember_password.isChecked():
            
            if not self.config_rember_pwd.check(user_id): 
                self.config_rember_pwd.setPwd(aes.encrypt(str({"password":user_pwd,"id_number":user_id,"time":time}),
                                                    aes.Key))
            self.config_rember_pwd.setFlag("1")
        if self.auto_login.isChecked():
            if not self.config_auto_login.check(user_id):
                self.config_auto_login.setStates(aes.encrypt(str({"mac_address":aes.mac_address,"id_number":user_id,"time":time}),
                                                              aes.Key))#aes不能解密加密自身
            self.config_auto_login.setFlag("1")

        self.emitsingal.emit(user_id)
        self.close()
           
 #self.emitsingal.emit(item["id_number"])
    def faceLogin(self):
        self.face_login_page = FaceLoginPage()
        self.face_login_page.emit_show_parent.connect(self.rev)
#接受人脸识别登录成功信号，接收发送给主页面
    @Slot(str)
    def rev(self,id_number):
       
        self.emitsingal.emit(id_number)

class config():
    config = None#使用全局变量单例模式,保证数据一致性
    file_name = "config.ini"
    def __init__(self):
        if  os.path.exists(self.file_name):
            return
        config = configparser.ConfigParser()    #实例化一个对象
        config["rember_pwd"] = {  'flag':'0','pwd':'' }     # 类似于操作字典的形式
        config["aotu_login"] = {'flag':'0','login_states':''}
        with open(self.file_name, "w", encoding="utf-8") as f:
            config.write(f)

    def __del__(self):
        if config.config != None:
            config.config = None#释放全局变量，降低内存占用
class  configRemberPwd(config):
    def __init__(self) -> None:
        super().__init__()
        self.result = False
        if config.config == None:
            config.config = configparser.ConfigParser()
            # 打开 ini 文件
            config.config.read(self.file_name, encoding="utf-8")
        if  config.config["rember_pwd"]['flag'] == '1':
            result = aes.decrypt(config.config["rember_pwd"]["pwd"],
                                      aes.Key)
            if result:
                self.result = eval(result)
    def checkFlag(self):
        return config.config["rember_pwd"]["flag"] == "1"
    def checkTime(self):
        if self.result:
            pre_time = datetime.datetime.strptime(self.result['time'],"%Y-%m-%d-%H-%M")
            days = (datetime.datetime.now() - pre_time ).days
            if days > 3:
                return False
            return True

    def check(self,user_id) -> bool:
        if not self.checkFlag():
            return False
        if self.result['id_number'] != user_id:
            return False
        if self.checkTime():
            return True
        return False
    def setFlag(self,flag):
        config.config["rember_pwd"]["flag"] = flag
        with open(self.file_name, "w", encoding="utf-8") as f:
            config.config.write(f)

    def setPwd(self,pwd):
        config.config["rember_pwd"]["pwd"] = pwd
        with open(self.file_name, "w", encoding="utf-8") as f:
            config.config.write(f)
    
  

class  configAotuLogin(config):
    """自动登录功能，只保存用户登录状态，不保存密码，更安全"""
    def __init__(self) -> None:
        super().__init__()
        self.result = False
        if config.config == None:
            config.config = configparser.ConfigParser()
            # 打开 ini 文件
            config.config.read(self.file_name, encoding="utf-8") 
        if  config.config["aotu_login"]['flag'] == '1':
            result = aes.decrypt(config.config["aotu_login"]["login_states"],
                                      aes.Key)
            if result:
                self.result = eval(result)
    def checkFlag(self):
        return config.config["aotu_login"]["flag"] == "1"
    def checkTime(self):
        if self.result:
            pre_time = datetime.datetime.strptime(self.result['time'],"%Y-%m-%d-%H-%M")
            days = (datetime.datetime.now() - pre_time ).days
            if days > aes.days:
                return False
            return True
    def checkPwd(self):
        if self.result:
            return self.result['mac_address'] == aes.mac_address

    def check(self,user_id) -> bool:
        if not self.checkFlag():
            return False
        if self.result['id_number'] != user_id:
            return False
        if not self.checkTime():
            return False
        if not self.checkPwd():
            return False
        return True
    def autoCHeck(self):
        if not self.checkFlag():
            return False
        if not self.checkTime():
            return False
        if not self.checkPwd():
            return False
        return True
        

    def setFlag(self,flag):
        config.config["aotu_login"]["flag"] = flag
        with open(self.file_name, "w", encoding="utf-8") as f:
            config.config.write(f)

    def setStates(self,states):
        config.config["aotu_login"]["login_states"] = states
        with open(self.file_name, "w", encoding="utf-8") as f:
            config.config.write(f)
    
class aes():
    Key = uuid.uuid1().hex[-12:][1:6]+'abc'
    mac_address = uuid.uuid1().hex[-12:]
    days = 3
    def encrypt(data,mac_address):
       
        key = pad(mac_address.encode("utf8"),AES.block_size)
        cipher = AES.new(key,AES.MODE_ECB)
        plaintext = data.encode('utf8')
        msg = cipher.encrypt(pad(plaintext,AES.block_size))
        result = str(base64.b64encode(msg).decode('utf8'))
        return result

    def decrypt(data,mac_address):
       
        key = pad(mac_address.encode("utf8"),AES.block_size)
        cipher = AES.new(key,AES.MODE_ECB)
        try:
            plaintext = base64.b64decode(data.encode("utf8"))
            msg = unpad(cipher.decrypt(plaintext),AES.block_size)
            result = str(msg.decode('utf8'))
            return result
        except:
            return False
