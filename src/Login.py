
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox,QCheckBox,QLineEdit, QApplication
from PySide6.QtCore import Signal,QRegularExpression,Slot
from .Database import database
from .Setting import user,isVerifyeRemote,file_name
from PySide6.QtCore import Slot,QUrl
import datetime
from .FaceLoginPage import FaceLoginPage
from . import Check
from .SigninPage import SigninPage
import configparser
import configparser
from .Database import PH
from PySide6.QtGui import  QRegularExpressionValidator,QIcon
from .encryption import *
from .logger import logger
from .Setting import resources_dir
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
#from PySide6 import QString
import pickle
if isVerifyeRemote:
    from .Setting import ip,port
class LoginUi(QWidget):
    emitsingal = Signal(str)
    emit_close = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('登录')
        self.setWindowIcon(QIcon( resources_dir + '登录.svg'))
        self.resize(400, 300)
        self.user_label = QLabel('Username:', self)
        self.pwd_label = QLabel('Password:', self)
        self.user_line = QLineEdit(self)
        validator =QRegularExpressionValidator(QRegularExpression("[0-9]*"))
        self.user_line.setValidator(validator)
        self.user_line.setMaxLength(20)
        self.user_line.setPlaceholderText("请输入数字,不大于{0}位".format(user.id_length.value))

        self.pwd_line = QLineEdit(self)
        validator = QRegularExpressionValidator(QRegularExpression(user.reg_pwd.value))
        self.pwd_line.setValidator(validator)
        self.pwd_line.setMaxLength(20)
        self.pwd_line.setPlaceholderText("请输入密码,不大于{0}位".format(user.password_max_length.value))

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

        self.user_id = self.user_line.text()
        self.user_pwd = self.pwd_line.text()

        if not self.user_id.isdigit() or len(self.user_id) > user.id_length.value:
           Check.id_number_info(self)
           return
        if len(self.user_pwd) < user.password_min_length.value or len(
        self.user_pwd) > user.password_max_length.value:
            Check.password_info(self)
            return
    
        result = Check.verifyePwd(self.user_id,self.user_pwd,"admin")
        if not result:
            QMessageBox.warning(self, '警告', '账号或密码错误，请重新输入')
            
            clear()
            return
        if isVerifyeRemote :
            self.manager = QNetworkAccessManager()

            url = f"http://{ip}:{port}"  # 请求的URL
            self.request = QNetworkRequest(QUrl(url))
            self.request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")

            # 发送POST请求
            data = pickle.dumps({'flag':'login',"mac_address":uuid.uuid1().hex[-12:],"id_number":self.user_id})
            self.reply = self.manager.post(self.request, data)

            self.reply.finished.connect(lambda: self.handle_response(self.reply))
          
            self.login_button.setText("登录中...")
            QApplication.processEvents()
            self.login_button.setEnabled(False)
        

        else : self.insertUser()
 
    def insertUser(self):    
        database.execute(f"INSERT INTO admin_log_time (id_number ) \
VALUES ({PH})", (self.user_id, ))
        
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        
        if self.remember_password.isChecked():
            
            if not self.config_rember_pwd.check(self.user_id): 
                self.config_rember_pwd.setPwd(aes.encrypt(str({"password":self.user_pwd,"id_number":self.user_id,"time":time}),
                                                    aes.Key))
            self.config_rember_pwd.setFlag("1")
        if self.auto_login.isChecked():
            if not self.config_auto_login.check(self.user_id):
                self.config_auto_login.setStates(aes.encrypt(str({"mac_address":aes.mac_address,"id_number":self.user_id,"time":time}),
                                                              aes.Key))#aes不能解密加密自身
            self.config_auto_login.setFlag("1")

        self.emitsingal.emit(self.user_id)
        self.close()


    
    def handle_response(self,reply):
        if reply.error().value:  
            logger.error(reply.error())
            QMessageBox.critical(self, '警告', "网络错误")
            self.login_button.setText("登录")
            self.login_button.setEnabled(True)
            return

        data = reply.readAll()
        flag = pickle.loads(data) 
        print("Response:",flag)
        if not flag:
            logger.error(reply.error())
            QMessageBox.critical(self, '警告', "账号与设备不匹配")
            self.login_button.setText("登录")
            self.login_button.setEnabled(True)
            return
        self.insertUser()
        
        #reply.deleteLater()

    
 #self.emitsingal.emit(item["id_number"])
    def faceLogin(self):
        self.face_login_page = FaceLoginPage(self.user_line.text())
        self.face_login_page.emit_show_parent.connect(self.rev)
#接受人脸识别登录成功信号，接收发送给主页面
    @Slot(str)
    def rev(self,id_number):
        self.face_login_page.close()
        if id_number == True:
            self.emitsingal.emit(id_number)
            return
        QMessageBox.critical(self, '警告', "网络错误或服务器错误")

class config():
    config = None#使用全局变量单例模式,保证数据一致性
   
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
            config.config.read(file_name, encoding="utf-8")
       
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

    def check(self,user_id,pwd=None) -> bool:
        if not self.checkFlag():
            return False
        if self.result['id_number'] != user_id or self.result['password'] != pwd:
            return False
        if self.checkTime():
            return True
        return False
    def setFlag(self,flag):
        config.config["rember_pwd"]["flag"] = flag
        with open(file_name, "w", encoding="utf-8") as f:
            config.config.write(f)

    def setPwd(self,pwd):
        config.config["rember_pwd"]["pwd"] = pwd
        with open(file_name, "w", encoding="utf-8") as f:
            config.config.write(f)
    
  

class  configAotuLogin(config):
    """自动登录功能，只保存用户登录状态，不保存密码，更安全"""
    def __init__(self) -> None:
        super().__init__()
        self.result = False
        if config.config == None:
            config.config = configparser.ConfigParser()
            # 打开 ini 文件
            config.config.read(file_name, encoding="utf-8") 
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
        with open(file_name, "w", encoding="utf-8") as f:
            config.config.write(f)

    def setStates(self,states):
        config.config["aotu_login"]["login_states"] = states
        with open(file_name, "w", encoding="utf-8") as f:
            config.config.write(f)
    

