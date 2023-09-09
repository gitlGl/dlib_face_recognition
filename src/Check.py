from PySide6.QtWidgets import QMessageBox
from .Database import database
from . import encryption
import os
from PySide6.QtWidgets import QFileDialog,QMessageBox
from .Setting import detector
import re
from .Setting import user,ip,port
from . import CreatUser
import http.client,pickle
from .logger import logger

def idNumber(id_number,row_info):
    if len(id_number) > user.id_length.value or (not id_number.isdigit()):
        return False
    result =  database.execute(
                "select id_number from student where id_number = {} ".
                format(id_number))
    if len( result) == 1 and id_number != row_info['id_number']:
        return False
    return True
def userName(user_name,row_info):
    lenth = len(user_name)
    if lenth > user.name_length.value or lenth == 0:
        
        return False
    return True
def gneder(gender,row_info):
    if gender == "男" or gender == "女":
        pass
    else:
        return False
    return True

def password(password,row_info):
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


def verifyePwd(user_id,user_pwd,tabel_name):

    user = database.execute(
                "select id_number,salt, password  from {0} where id_number = {1} "
                .format(tabel_name,user_id))
    if len(user) != 1:
        return False              

    item = user[0]
    pass_word = encryption.createMd5(user_pwd, item["salt"],user_id)
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


    rgbImage = CreatUser.getImg(path)
    
    faces = detector(rgbImage)
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
 

 #客户端请求
def Req(data):
    conn = http.client.HTTPConnection(ip, port,timeout=5)
    data_tem = pickle.dumps(data)
    conn.request("POST", "", data_tem)
    response = conn.getresponse()
    rev_data = response.read()
    conn.close()
    return pickle.loads(rev_data)
#校对验证码
def checkVerifye(data):
    try:
        if Req(data):
            return True
    
        else:
            return '验证码错误'
    except Exception as e:
        logger.error(e)
        return '网络错误或服务器错误'
    
