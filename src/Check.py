from PySide6.QtWidgets import QMessageBox
from .GlobalVariable import database
from .MyMd5 import MyMd5
import os
from PySide6.QtWidgets import QFileDialog,QMessageBox
from .GlobalVariable import models
#from .Creatuser import CreatUser
from enum import Enum
import cv2,re
import numpy as np
class user(Enum):
    id_length = 13
    password_max_length = 20
    password_min_length = 6
    name_length = 20

 #检查用户输入的数据是否合法
       
class verifyCellData():
    def idNumber(parent,id_number,row_info):
        if len(id_number) > 20 or (not id_number.isdigit()):
            return False
        result =  database.execute(
                    "select id_number from student where id_number = {} ".
                    format(id_number))
        if len( result) == 1 and id_number != row_info['id_number']:
            return False
        return True
    def userName(parent,user_name,row_info):
        lenth = len(user_name)
        if lenth > user.name_length.value or lenth == 0:
            
            return False
        return True
    def gneder(parent,gender,row_info):
        if gender == "男" or gender == "女":
            pass
        else:
            return False
        return True
   
    def password(parent,password,row_info):
        if (len(password) < user.password_min_length.value or len(
            password) > user.password_max_length.value):
            if (password != row_info['password']):
                return False
        pattern = r'^[a-zA-Z0-9@#$%^&+=]+$'
        if not re.match(pattern, password):
            return False
        return True
    user_name_info = lambda parent:QMessageBox.critical(parent, '警告', f'用户名为{user.name_length.value}个有效字符')
    gender_info = lambda parent: QMessageBox.critical(parent, '警告', '性别为男或女')
    id_number_info = lambda parent: QMessageBox.critical(parent, '警告', f'学号为{user.id_length.value}个有效字符,或已存在')
    password_info = lambda parent: QMessageBox.critical(parent, '警告', f'密码为{user.password_min_length.value}-{user.password_max_length.value}位,字母数字、特殊字符!')

#  #检查输入信息
#         lenth = len(user_name)
#         if lenth > user.name_length.value or lenth == 0:

#              QMessageBox.critical(self, '警告', f'用户名为{user.name_length.value}个有效字符')
#              return False
       
#         if gender == "男" or gender == "女":
#             pass
#         else:
#             QMessageBox.critical(self, '警告', 'gender is only 男 or 女')
#             return False

#         if len(id_number) > 20 or (not id_number.isdigit()):
#             QMessageBox.critical(self, '警告',
#                                  'id_number is only digit or is too long!')
#             return False

        
#         result =  database.execute(
#                     "select id_number from student where id_number = {} ".
#                     format(id_number))
#         if len( result) == 1 and id != id_number:
#             QMessageBox.critical(self, '警告', ' 这个学号已经存在')
#             return False
#         if (len(password) < user.password_min_length.value or len(
#             password) > user.password_max_length.value):
#             if (password != self.information["password"]):
#                 QMessageBox.critical(self, '警告',
#                                       f' 密码为{user.password_min_length.value}-{user.password_max_length.value}位!')      




def verifyePwd(user_id,user_pwd,tabel_name):
   
    user = database.execute(
                "select id_number,salt, password  from {0} where id_number = {1} "
                .format(tabel_name,user_id))
    if len(user) != 1:
        return False              

    item = user[0]
    pass_word = MyMd5.createMd5(user_pwd, item["salt"],user_id)
    if pass_word == item["password"]: 
        return True
    
    return False

def checkPath(path,parent=None):
    if path == '':
        return False
        
    if (not os.path.isfile(path)) or (os.path.getsize(path) >
                                                  1024000):  #文件小于10mb
        QMessageBox.critical(parent, '警告', '文件应小于10mb，或不存在文件')
        return False

    data = open(path,"rb").read(32)
    if not (data[6:10] in (b'JFIF',b'Exif')):#检查文件类型是否属于jpg文件
        QMessageBox.critical(parent, '警告', '文件非图片文件')
        return False

  
    rgbImage = getImg(path)
    
    faces = models.detector(rgbImage)
    if len(faces) != 1:
        QMessageBox.critical(parent, '警告', '文件不存在人脸或多个人脸')
        return False
    return path

def getImgPath(parent=None):
    path, _ = QFileDialog.getOpenFileName(
        parent, "选择文件", "c:\\", "Image files(*.jpg *.gif *.png)")
    if checkPath(path,parent):
        return path    
    return False
def getImg( img_path):
        raw_data = np.fromfile(
            img_path, dtype=np.uint8)  #先用numpy把图片文件存入内存：raw_data，把图片数据看做是纯字节数据
        rgbImage = cv2.imdecode(raw_data, cv2.IMREAD_COLOR)  #从内存数据读入图片

        #rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
        return rgbImage

# QMessageBox.information(parent, 'Information', '警告 username or Password')\
# messageBox = QMessageBox(QMessageBox.Warning, "警告", "向电网输出功率太大，请减小输出功率！")          
# messageBox.setWindowIcon(QtGui.QIcon(":/newPrefix/logo.ico"))
# Qyes = messageBox.addButton(self.tr("设置"), QMessageBox.YesRole)
# Qno = messageBox.addButton(self.tr("忽略"), QMessageBox.NoRole)
# messageBox.exec_()
# if messageBox.clickedButton() == Qyes:
#     print('ok')   
# else:
#     return