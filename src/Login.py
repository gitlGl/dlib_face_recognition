
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

        self.lineeditInit()
        self.pushbuttonInit()
        self.layoutInit()
        self.config_rember_pwd = configRemberPwd()
        self.config_auto_login = configAotuLogin()
        if not self.config_rember_pwd.check():
            return
        self.remember_password.setChecked(True)
        result = self.config_rember_pwd.result
        if result:
            id = result[-36:]
            id = id[:-16]
            id = id.strip(' ')
            self.user_line.setText(id)
            self.pwd_line.setText(result[:-36])
        
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

        uesr_id = self.user_line.text()
        user_pwd = self.pwd_line.text()

        if not checkUserId(uesr_id):
           QMessageBox.critical(self, '警告', '用户名只能为数字，且不能超过20个数字')
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
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        len_ = len(uesr_id)
        id = uesr_id
        for i in range(len_,20):
            id = id+" "
        if self.remember_password.isChecked():
            
            if not self.config_rember_pwd.check():
                self.config_rember_pwd.setPwd(aes.encrypt(self.pwd_line.text()+id+time))
            self.config_rember_pwd.setFlag("1")
        if self.auto_login.isChecked():
            if not self.config_auto_login.check():
                self.config_auto_login.setStates(aes.encrypt(uuid.uuid1().hex[-12:]+id+time))#aes不能解密加密自身
            self.config_auto_login.setFlag("1")

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

class config():
    config = None#使用全局变量单例模式,保证数据一致性

    def __del__(self):
        if config.config != None:
            config.config = None#释放全局变量，降低内存占用
class  configRemberPwd(config):
    def __init__(self) -> None:
        if config.config == None:
            config.config = configparser.ConfigParser()
            # 打开 ini 文件
            config.config.read("cfg.ini", encoding="utf-8")
        if  config.config["rember_pwd"]['flag'] == '1':
            self.result = aes.decrypt(config.config["rember_pwd"]["pwd"])
    def check(self) -> bool:
        if config.config["rember_pwd"]["flag"] == "0":
            return False
        pre_time = datetime.datetime.strptime(self.result[-16:],"%Y-%m-%d-%H-%M")
        days = (datetime.datetime.now() - pre_time ).days
        if days > 7:
            return False
        return True
    def setFlag(self,flag):
        config.config["rember_pwd"]["flag"] = flag
        with open("cfg.ini", "w", encoding="utf-8") as f:
            config.config.write(f)

    def setPwd(self,pwd):
        config.config["rember_pwd"]["pwd"] = pwd
        with open("cfg.ini", "w", encoding="utf-8") as f:
            config.config.write(f)
    
  

class  configAotuLogin(config):
    """自动登录功能，只保存用户登录状态，不保存密码，更安全"""
    def __init__(self) -> None:
        if config.config == None:
            config.config = configparser.ConfigParser()
            # 打开 ini 文件
            config.config.read("cfg.ini", encoding="utf-8") 
        if  config.config["aotu_login"]['flag'] == '1':
            self.result = aes.decrypt(config.config["aotu_login"]["login_states"])
    def check(self) -> bool:
        if config.config["aotu_login"]["flag"] == "0":
            return False
        pre_time = datetime.datetime.strptime(self.result[-16:],"%Y-%m-%d-%H-%M")
        days = (datetime.datetime.now() - pre_time ).days
        if days > 7:
            return False
        
        if not self.result[:12] == uuid.uuid1().hex[-12:]:
            return False
        return True
    def get(self):
        return dict(config.config["aotu_login"])

    def setFlag(self,flag):
        config.config["aotu_login"]["flag"] = flag
        with open("cfg.ini", "w", encoding="utf-8") as f:
            config.config.write(f)
    def setId(self,id):
         with open("cfg.ini", "w", encoding="utf-8") as f:
            config.config.write(f)
    

    def setStates(self,states):
        config.config["aotu_login"]["login_states"] = states
        with open("cfg.ini", "w", encoding="utf-8") as f:
            config.config.write(f)
    
       




class aes():
    def encrypt(data):
        mac_address = uuid.uuid1().hex[-12:][1:6]+'abc'
        key = pad(mac_address.encode("utf8"),AES.block_size)
        cipher = AES.new(key,AES.MODE_ECB)
        plaintext = data.encode('utf8')
        msg = cipher.encrypt(pad(plaintext,AES.block_size))
        result = str(base64.b64encode(msg).decode('utf8'))
        return result

    def decrypt(data):
        mac_address = uuid.uuid1().hex[-12:][1:6]+'abc'
        key = pad(mac_address.encode("utf8"),AES.block_size)
        cipher = AES.new(key,AES.MODE_ECB)
        try:
            plaintext = base64.b64decode(data.encode("utf8"))
            msg = unpad(cipher.decrypt(plaintext),AES.block_size)
            result = str(msg.decode('utf8'))
            return result
        except:
            return False
