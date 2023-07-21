from PySide6.QtWidgets import QMessageBox
from .GlobalVariable import database
from .MyMd5 import MyMd5
import os
from PySide6.QtWidgets import QFileDialog,QMessageBox
from .GlobalVariable import models
from .Creatuser import CreatUser
from .GlobalVariable import user
def checkUserId(user_id):

    if not user_id.isdigit() or len(user_id) > 20:
        return False
    return True


def checkUserPwd(user_pwd):
    if len(user_pwd) < user.password_min_length.value or len(
        user_pwd) > user.password_max_length.value:
            return False
    return True
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

  
    rgbImage = CreatUser().getImg(path)
    
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