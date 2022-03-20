from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from src.Database import Database
from src.MyMd5 import MyMd5
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.GlobalVariable import models
from .Creatuser import CreatStudentUser
import PIL.Image
import numpy as np
from src.FaceLoginPage import FaceLoginPage


class UpdateData(QDialog):
    def __init__(self,information= None):
        super(UpdateData, self).__init__()
        self.information =information
      
        self.id_label = QLabel('学号:', self)
        self.user_label = QLabel('姓名:', self)
        self.gender_label = QLabel('性别:', self)

        self.id_number_line = QLineEdit(self)
        self.user_name_line = QLineEdit(self)
        self.gender_line = QLineEdit(self)
        self.vector_button = QPushButton("照片:", self,objectName="GreenButton")
        self.vector_button.setFlat(True)

        self.vector_button.setIcon(QIcon("./resources/文件.png"))

        self.vector_line = QLineEdit(self)
        self.ensure_button = QPushButton('确定修改', self,objectName="GreenButton")

        self.user_h_layout = QHBoxLayout()
        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.vector_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()
        self.resize(300, 200)
        if information is not None:
            self.id_number_line.setText(self.information["id_number"])
            self.user_name_line.setText(information["user_name"])
            self.gender_line.setText(information["gender"])
        

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()

    def layout_init(self):
        self.user_h_layout.addWidget(self.id_label)
        self.user_h_layout.addWidget(self.id_number_line)
        self.pwd_h_layout.addWidget(self.user_label)
        self.pwd_h_layout.addWidget(self.user_name_line)
        self.pwd2_h_layout.addWidget(self.gender_label)
        self.pwd2_h_layout.addWidget(self.gender_line)
        self.vector_h_layout.addWidget(self.vector_button)
        self.vector_h_layout.addWidget(self.vector_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addLayout(self.vector_h_layout)
        self.all_v_layout.addWidget(self.ensure_button)

        self.setLayout(self.all_v_layout)

    def lineedit_init(self):

        self.id_number_line.textChanged.connect(self.check_input_func)
        self.user_name_line.textChanged.connect(self.check_input_func)
        self.gender_line.textChanged.connect(self.check_input_func)
        self.vector_line.textChanged.connect(self.check_input_func)
        self.vector_button.clicked.connect(self.get_path)

    def check_input_func(self):
        if self.id_number_line.text() and self.user_name_line.text(
        ) and self.gender_line.text() and self.vector_line.text():
            self.ensure_button.setEnabled(True)
        else:
            self.ensure_button.setEnabled(False)
    def pushbutton_init(self):
        self.ensure_button.setEnabled(False)

    
    def update(self):
        if (not self.signin_user_line.text().isdigit()) or (len(self.signin_user_line.text())>15):
            QMessageBox.critical(self, 'Wrong', 'Usernumber is only digit or is too long!')
            return

    def get_path(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "c:\\", "Image files(*.jpg *.gif *.png)")
        if path == '':
            return
        self.vector_line.setText(path)
        rgbImage = PIL.Image.open(path)
        rgbImage  =  rgbImage .convert("RGB")
        rgbImage =  np.array(rgbImage )
        faces = models.detector(rgbImage)
        if len(faces) == 1:
            return
        else:
            QMessageBox.critical(self, 'Wrong', '文件不存在人脸或多个人脸')
            self.vector_line.clear()
            return
