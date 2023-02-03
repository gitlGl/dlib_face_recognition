from PyQt5.QtWidgets import QMessageBox
from .Database import database
from .MyMd5 import MyMd5
import os
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from .GlobalVariable import models
from .Creatuser import CreatUser
def check_user_id(user_id):

    if not user_id.isdigit() or len(user_id) > 100:
        return False
    return True


def check_user_pwd(user_pwd):
    if len(user_pwd) < 6 or len(user_pwd) > 13:
            return False
    return True
def verifye_pwd(user_id,user_pwd,tabel_name):
   
    user = database.c.execute(
                "select id_number,salt, password  from {0} where id_number = {1} "
                .format(tabel_name,user_id)).fetchall()

    if len(user) != 1:
        return False              

    item = user[0]
    pass_word = MyMd5().createMd5(user_pwd, item["salt"])
    if pass_word == item["password"]: 
        return True
    
    return False

def checkPath(path,parent=None):
    if path == '':
        return False
        
    if os.path.getsize(path) > 1024000 :
        QMessageBox.critical(parent, 'Wrong', '文件应小于10mb')
        return False

    data = open(path,"rb").read(32)
    if not (data[6:10] in (b'JFIF',b'Exif')):#检查文件类型是否属于jpg文件
        QMessageBox.critical(parent, 'Wrong', '文件非图片文件')
        return False

  
    rgbImage = CreatUser().getImg(path)
    
    faces = models.detector(rgbImage)
    if len(faces) != 1:
        QMessageBox.critical(parent, 'Wrong', '文件不存在人脸或多个人脸')
        return False
    return path

def getImgPath(parent=None):
    path, _ = QFileDialog.getOpenFileName(
        parent, "选择文件", "c:\\", "Image files(*.jpg *.gif *.png)")
    if checkPath(path,parent):
        return path    
    return False
# QMessageBox.information(parent, 'Information', '警告 username or Password')