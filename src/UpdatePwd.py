from .Database import Database
from .MyMd5 import MyMd5
from PyQt5.QtCore import Qt,pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QPushButton,\
QMessageBox, QLineEdit,QDialog
class UpdatePwd(QDialog):
    def __init__(self,id_number):
        super().__init__()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle('修改密码')
        self.setWindowIcon(QIcon('resources/修改密码.png'))
        self.id_number = id_number
        self.old_pwd_label = QLabel('旧密码:', self)
        self.new_pwd2_label = QLabel('新密码:', self)
        self.new_pwd3_label = QLabel('确认密码:', self)
        self.new_pwd3_label.setStyleSheet(" font-size:9px;font-weight:350;")
        self.old_pwd_line = QLineEdit(self)
        self.new_pwd2_line = QLineEdit(self)
        self.new_pwd3_line = QLineEdit(self)

        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.pwd3_h_layout = QHBoxLayout()
        self.ensure_or = QHBoxLayout()
        self.pwd_h_layout.addWidget(self.old_pwd_label)
        self.pwd_h_layout.addWidget(self.old_pwd_line)

        self.pwd2_h_layout.addWidget(self.new_pwd2_label)
        self.pwd2_h_layout.addWidget(self.new_pwd2_line)

        self.pwd3_h_layout.addWidget(self.new_pwd3_label)
        self.pwd3_h_layout.addWidget(self.new_pwd3_line)

        self.pwd_v_layout = QVBoxLayout()
        self.pwd_v_layout.addLayout(self.pwd_h_layout)
        self.pwd_v_layout.addLayout(self.pwd2_h_layout)
        self.pwd_v_layout.addLayout(self.pwd3_h_layout)
        self.btn1_event = QPushButton()
        self.btn1 = QPushButton(objectName="GreenButton")
        self.btn1.setText("确认修改")
        self.btn2 = QPushButton()
        self.btn2 = QPushButton(objectName="GreenButton")
        self.btn2.setText("取消修改")
        self.ensure_or.addWidget(self.btn1)
        self.ensure_or.addWidget(self.btn2)
        self.pwd_v_layout.addLayout(self.ensure_or)
        self.btn1.clicked.connect(self.btn1_update_pwd)
        self.btn2.clicked.connect(self.btn2_event)
      
        self.setLayout(self.pwd_v_layout)
 
    def btn1_update_pwd(self):
        old_pwd =  self.old_pwd_line.text()
        new_pwd = self.new_pwd2_line.text()
        new_pwd_2 = self.new_pwd3_line.text()
        if new_pwd != new_pwd_2:
            QMessageBox.critical(self, 'Wrong', '两次密码不一致')
            return
        
        if len(new_pwd) < 6 and len(new_pwd) > 16 :
            QMessageBox.critical(self, 'Wrong', '密码长度不能小于6位或大于16位')
            return

        if old_pwd == new_pwd:
            QMessageBox.critical(self, 'Wrong', '新旧密码不能一致')
            return

    
        database = Database()
        item = database.c.execute("select password ,salt from admin where id_number = {0}".format(self.id_number)).fetchone()
        old_pass_word = MyMd5().create_md5(old_pwd, item["salt"])
        if old_pass_word != item["password"]:
             QMessageBox.critical(self, 'Wrong', '旧密码错误')
             return
        new_pass_word = MyMd5().create_md5(new_pwd, item["salt"])
        database.c.execute("update admin set password = ? where id_number = {0}".format(self.id_number),(new_pass_word,))
        database.conn.commit()
        database.conn.close()
        QMessageBox.information(self, 'Success', '修改成功')
        self.close()
        return
    
    #取消修改
    def btn2_event(self):
        self.close()


