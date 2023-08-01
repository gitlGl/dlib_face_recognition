from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, \
QVBoxLayout, QHBoxLayout, QMessageBox
from .Setting import database
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from . import encryption
from . import Check
from .Setting import user
import re
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

class UpdatePwd(QDialog):
    def __init__(self, id_number):
        super().__init__()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint
                            | Qt.WindowCloseButtonHint)
        self.setWindowTitle('修改密码')
        self.setWindowIcon(QIcon('resources/修改密码.svg'))
        self.id_number = id_number
        self.old_pwd_label = QLabel('旧密码:', self)
        self.new_pwd2_label = QLabel('新密码:', self)
        self.new_pwd3_label = QLabel('确认密码:', self)
        #self.new_pwd3_label.setStyleSheet("font-size:9pt;font-weight:35;")
        self.old_pwd_line = QLineEdit(self)
        validator = QRegularExpressionValidator(QRegularExpression(user.reg_pwd.value))
        self.old_pwd_line.setValidator(validator)
        self.old_pwd_line.setMaxLength(20)
        self.old_pwd_line.setPlaceholderText("密码不大于{0}位".format(user.password_max_length.value))

       
        self.new_pwd2_line = QLineEdit(self)
        validator = QRegularExpressionValidator(QRegularExpression(user.reg_pwd.value))
        self.new_pwd2_line.setValidator(validator)
        self.new_pwd2_line.setMaxLength(20)

        self.new_pwd3_line = QLineEdit(self)
        validator = QRegularExpressionValidator(QRegularExpression(user.reg_pwd.value))
        self.new_pwd3_line.setValidator(validator)
        self.new_pwd3_line.setMaxLength(20)

        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.pwd3_h_layout = QHBoxLayout()
        self.ensure_or = QHBoxLayout()
        self.pwd_h_layout.addSpacing(12)
        self.pwd_h_layout.addWidget(self.old_pwd_label)
        
        self.pwd_h_layout.addWidget(self.old_pwd_line)

        self.pwd2_h_layout.addSpacing(12)
        
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
        self.btn1.clicked.connect(self.btn1UpdatePwd)
        self.btn2.clicked.connect(self.btn2Event)

        self.setLayout(self.pwd_v_layout)

    def btn1UpdatePwd(self):
        old_pwd = self.old_pwd_line.text()
        new_pwd = self.new_pwd2_line.text()
        new_pwd_2 = self.new_pwd3_line.text()
        if new_pwd != new_pwd_2:
            QMessageBox.critical(self, '警告', '两次密码不一致')
            return

        if len(new_pwd) < user.password_min_length.value and len(
            new_pwd) > user.password_max_length.value:
            QMessageBox.critical(self, '警告', 
                                 f'密码长度不能小于{user.password_min_length.value}位或大于{user.password_max_length.value}位')
            return
        pattern =  user.reg_pwd.value
        if not re.match(pattern, new_pwd):
            Check.password_info(self)
            return
            
        if old_pwd == new_pwd:
            QMessageBox.critical(self, '警告', '新旧密码不能一致')
            return

        item = database.execute(
            "select salt from admin where id_number = {0}".format(
                self.id_number))[0]
        result = Check.verifyePwd(self.id_number, old_pwd, "admin")
        if not result:
            QMessageBox.critical(self, '警告', '旧密码错误')
            return
        new_pass_word = encryption.createMd5(new_pwd, item["salt"],
                                          self.id_number)
       
        database.execute(
            f"update admin set password = '{new_pass_word}' where id_number = {self.id_number}")
               
        QMessageBox.information(self, 'Success', '修改成功')
        self.close()
        return

    #取消修改
    def btn2Event(self):
        self.close()
