from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMessageBox,QDialogButtonBox
from PyQt5.QtCore import pyqtSignal,Qt
from src.Database import Database
from src.MyMd5 import MyMd5
from PyQt5.QtCore import pyqtSlot,QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.GlobalVariable import models
from .Creatuser import CreatUser
import PIL.Image,os,shutil
import numpy as np
from src.FaceLoginPage import FaceLoginPage


class UpdateData(QDialog):
    def __init__(self,information= None):
        super(UpdateData, self).__init__()
        self.path = None
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
        #self.ensure_button = QPushButton('确定修改', self,objectName="GreenButton")

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
        
        self.buttonBox = QDialogButtonBox(self)
        #self.buttonBox.setGeometry(QRect(-20, 340, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept_)
        self.buttonBox.rejected.connect(self.reject_)
        self.layout_init()
    #
    def accept_(self):
        self.accept()#返回1
    def reject_(self):
        self.reject()#返回0
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
        self.all_v_layout.addWidget(self.buttonBox)

        self.setLayout(self.all_v_layout)
        self.vector_button.clicked.connect(self.get_path)
    
    def delete(self,id):
        path = "img_information/student/{0}/".format(str(id))
        data = Database()
     
        data.delete(id)
        if not os.path.exists(path):
            shutil.rmtree(path)

    def update(self,id):
        user_name = self.user_name_line.text()
        id_number = self.id_number_line.text()
        gender = None
        if  self.gender_line.text() == "男":
            gender = 1
        elif  self.gender_line.text() =="女":
            gender =0
        else:
            QMessageBox.critical(self, 'Wrong', 'gender is only 男 or 女')
            return

        if len(id_number)>20 or (not id_number.isdigit()):
            QMessageBox.critical(self, 'Wrong', 'id_number is only digit or is too long!')
            return


        elif len (user_name) >13:
             QMessageBox.critical(self, 'Wrong', 'User_number is only digit or is too long!')

        else :
            if self.path == None:
                data = Database()
                sql = "UPDATE student SET id_number = {0},user_name = '{1}',gender = {2} WHERE id_number = {3}"\
                .format(id_number,user_name,gender,id)
                print(sql)
                data.c.execute(sql)
                data.conn.commit()
                data.conn.close()
                ##更改用户文件信息
                old_path = "img_information/student/{0}/".format(str(id))
                new_path = "img_information/student/{0}/".format(str(id_number))
                if not os.path.exists(old_path):  #判断是否存在文件夹如果不存在则创建为文件夹
                    os.makedirs(new_path)
                    os.makedirs("img_information/student/{0}/log".format(str(id_number)))
                    #shutil.rmtree("img_information/student/{0}".format(str(id)))
                else :
                    os.rename("img_information/student/{0}/{1}.jpg".format(str(id),str(id)),"img_information/student/{0}/{1}.jpg".format(str(id),str(id_number)))
                    os.rename(old_path,new_path)
            else :
                data = Database()
                old_path = "img_information/student/{0}/".format(str(id))
                new_path = "img_information/student/{0}/".format(str(id_number))
                if not os.path.exists(old_path):  #判断是否存在文件夹如果不存在则创建为文件夹
                    if not os.path.exists("img_information/student/{0}/log".format(str(id_number))):
                        os.makedirs("img_information/student/{0}/log".format(str(id_number)))
                else:
                    shutil.rmtree("img_information/student/{0}".format(str(id)))
                    os.makedirs("img_information/student/{0}/log".format(str(id_number)))

                vector = CreatUser().get_vector(id_number,self.path,"student")
                data.c.execute("update student set id_number= ?,user_name = ?,gender = ? ,vector = ? where id_number = {0}"
                .format(id),(id_number,user_name,gender,vector))
                data.conn.commit()
                data.conn.close()
                print("sucess")
           
             
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
            self.path = path
            return
        else:
            QMessageBox.critical(self, 'Wrong', '文件不存在人脸或多个人脸')
            self.vector_line.clear()
            return