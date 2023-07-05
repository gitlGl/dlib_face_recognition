
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox,QCheckBox
from PyQt5.QtCore import pyqtSignal
from .GlobalVariable import database
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
import datetime,uuid
from .FaceLoginPage import FaceLoginPage
from .Check import checkUserId, checkUserPwd,verifyePwd
from .SigninPage import SigninPage
import configparser
import os
from .Check import Req,aes
import configparser
from .Database import PH
#from PyQt5 import QString
class LoginUi(QWidget):
    emitsingal = pyqtSignal(str)
    emit_close = pyqtSignal()

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
        #self.setEnabled(False)

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
        self.auto_login.setChecked(True)
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
            QMessageBox.warning(self, '警告', '账号或密码错误，请重新输入')
            clear()
            return
       
        self.login_button.setText("登录中...")
        QApplication.processEvents()
        self.login_button.setEnabled(False)
        try:
            if not  Req({'flag':'login',"mac_address":uuid.uuid1().hex[-12:]}):
                QMessageBox.critical(self, '警告', "设备与账号不匹配")
                self.login_button.setText("登录")
                self.login_button.setEnabled(True)
                return
        except:
            QMessageBox.critical(self, '警告', "网络错误")
            self.login_button.setText("登录")
            self.login_button.setEnabled(True)
            return
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        database.c.execute(f"INSERT INTO admin_log_time (id_number,log_time ) \
VALUES ({PH},{PH})", (uesr_id, time))
        database.conn.commit()
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        
        if self.remember_password.isChecked():
            
            if not self.config_rember_pwd.check():
                self.config_rember_pwd.setPwd(aes.encrypt(str({"password":self.pwd_line.text(),"id_number":uesr_id,"time":time}),
                                                         uuid.uuid1().hex[-12:][1:6]+'abc' ))
            self.config_rember_pwd.setFlag("1")
        if self.auto_login.isChecked():
            if not self.config_auto_login.check():
                self.config_auto_login.setStates(aes.encrypt(str({"mac_address":uuid.uuid1().hex[-12:],"id_number":uesr_id,"time":time}),
                                                             uuid.uuid1().hex[-12:][1:6]+'abc'))#aes不能解密加密自身
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
        self.face_login_page.close()
        if not id_number.isdigit():
            QMessageBox.critical(self, '警告', id_number, QMessageBox.Yes)
            return
        self.emitsingal.emit(id_number)

class config():
    config = None#使用全局变量单例模式,保证数据一致性
    file_name = "config.ini"
    def __init__(self):
        if  os.path.isfile(self.file_name):
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
                                      uuid.uuid1().hex[-12:][1:6]+'abc')
            if result:
                self.result = eval(result),
            print(self.result)
    def checkFlag(self):
        return config.config["rember_pwd"]["flag"] == "1"
    def checkTime(self):
        if self.result:
            pre_time = datetime.datetime.strptime(self.result['time'],"%Y-%m-%d-%H-%M")
            days = (datetime.datetime.now() - pre_time ).days
            if days > 3:
                return False
            return True

    def check(self) -> bool:
        if not self.checkFlag():
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
            self.result = eval(aes.decrypt(config.config["aotu_login"]["login_states"], 
                                      uuid.uuid1().hex[-12:][1:6]+'abc'))
    def checkFlag(self):
        return config.config["aotu_login"]["flag"] == "1"
    def checkTime(self):
        if self.result:
            pre_time = datetime.datetime.strptime(self.result['time'],"%Y-%m-%d-%H-%M")
            days = (datetime.datetime.now() - pre_time ).days
            if days > 3:
                return False
            return True
    def checkPwd(self):
        if self.result:
            return self.result['mac_address'] == uuid.uuid1().hex[-12:]

    def check(self) -> bool:
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
    
       





