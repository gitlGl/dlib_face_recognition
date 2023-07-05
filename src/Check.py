from PyQt5.QtWidgets import QMessageBox
from .GlobalVariable import database
from .MyMd5 import MyMd5
import os
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from .GlobalVariable import models
from .Creatuser import CreatUser
import http.client,pickle
import hashlib
import base64,uuid
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
def checkUserId(user_id):

    if not user_id.isdigit() or len(user_id) > 20:
        return False
    return True


def checkUserPwd(user_pwd):
    if len(user_pwd) < 6 or len(user_pwd) > 13:
            return False
    return True
def verifyePwd(user_id,user_pwd,tabel_name):
   
    database.c.execute(
                "select id_number,salt, password  from {0} where id_number = {1} "
                .format(tabel_name,user_id))
    user = database.c.fetchall()

    if len(user) != 1:
        return False              

    item = user[0]
    pass_word = MyMd5().createMd5(user_pwd, item["salt"],user_id)
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
# QMessageBox.information(parent, 'Information', '警告 username or Password')


#校对验证码
def checkVerifye(data):
    try:
        if Req(data):
            return True
    
        else:
            return '验证码错误'
    except:
        return '网络错误'


#客户端请求
def Req(data):
    conn = http.client.HTTPConnection("localhost", 8888,timeout=5)
    data_tem = pickle.dumps(data)
    conn.request("POST", "", data_tem)
    response = conn.getresponse()
    rev_data = response.read()
    conn.close()
    return pickle.loads(rev_data)

def createMd5(password, id_number):#随机盐加三位用户id混淆
    md5 = hashlib.md5()
    if type(password) != str:

        md5.update(password )
        return md5.hexdigest()
    md5.update((password + id_number[-4:-1]).encode("utf-8"))
    return md5.hexdigest()

class aes():
    Key = uuid.uuid1().hex[-12:][1:6] + "abc"
    mac_address = uuid.uuid1().hex[-12:]
    days = 3
    
    def encrypt(data,mac_address):
       
        key = pad(mac_address.encode("utf8"),AES.block_size)
        cipher = AES.new(key,AES.MODE_ECB)
        plaintext = data.encode('utf8')
        msg = cipher.encrypt(pad(plaintext,AES.block_size))
        result = str(base64.b64encode(msg).decode('utf8'))
        return result

    def decrypt(data,mac_address):
        key = pad(mac_address.encode("utf8"),AES.block_size)
        cipher = AES.new(key,AES.MODE_ECB)
        try:
            plaintext = base64.b64decode(data.encode("utf8"))
            msg = unpad(cipher.decrypt(plaintext),AES.block_size)
            result = str(msg.decode('utf8'))
            return result
        except:
            return False
