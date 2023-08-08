from . import encryption
import numpy as np
from .Setting import predictor,detector,encoder
import os,re,sqlite3
from .Database import database
import cv2, pickle
from .Setting import user 
from . import encryption
from .Database import PH


def getImg(img_path):
    raw_data = np.fromfile(
        img_path, dtype=np.uint8)  #先用numpy把图片文件存入内存：raw_data，把图片数据看做是纯字节数据
    rgbImage = cv2.imdecode(raw_data, cv2.IMREAD_COLOR)  #从内存数据读入图片

    #rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
    return rgbImage

def insertImg(id_number, img_path, fuck):
    path = "img_information/" + fuck + "/" + str(id_number)
    if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)
    rgbImage =  getImg(img_path)
    cv2.imwrite(
        "img_information/" + fuck + "/" + str(id_number) + "/" +
        str(id_number) + ".jpg", rgbImage)

def getVector(img_path):
    """
    读取照片，获取人脸编码信息，把照片存储起来
    返回128维人脸编码信息
    """
    rgbImage =  getImg(img_path)
    face = detector(rgbImage)[0]
    frame = predictor(rgbImage, face)
    face_data = np.array(
        encoder.compute_face_descriptor(rgbImage, frame))
    face_data = pickle.dumps(face_data)
    return face_data

def checkInsert(row,row_user_data,list_problem):
#判断用户名是否符合格式要求
        if type(row_user_data[0]) == float:
            row_user_data[0] = int(row_user_data[0])

        if (not str(row_user_data[0]).isdigit()) or len(
            str(row_user_data[0])) == user.id_length.value:
            list_problem.append(
                f"第{0}行第1列,用户id为{user.id_length.value}位数字 ".format(row) +
                                str(row_user_data[0]))
            return
        user_ = database.execute(
            "select id_number from student where id_number = {} ".
            format(str(row_user_data[0])))
        if len(user_) == 1:
            list_problem.append("第{0}行第1列,用户已存在: ".format(row) +
                                str(row_user_data[0]))
            return

        row_user_data[0] = str(row_user_data[0])

        #判断用户姓名是否符合格式要求
        lenth = len(str(row_user_data[1]))
        if lenth > 16 or lenth == 0:

            list_problem.append("第{0}行第2列,姓名为16个字符以下: ".format(row) +
                                str(row_user_data[1]))
            return
        row_user_data[1] = str(row_user_data[1])

        #判断用户性别格式
        if str(row_user_data[2]) != "男" and str(row_user_data[2]) != "女":
            list_problem.append("第{0}行第3列,性别为男或女: ".format(row) +
                                str(row_user_data[2]))
            return
        row_user_data[2] = str(row_user_data[2])
        #判断密码是否符合格式要求

        lenth = len(str(row_user_data[3]))
        if lenth > user.password_max_length.value or lenth < user.password_min_length.value:
            list_problem.append("第{0}行第4列,密码为6-13位数字，字母，特殊符号字符: ".format(row) +
                                            str(row_user_data[3]))
            return
        pattern = user.reg_pwd.value
        if not re.match(pattern, str(row_user_data[3])):
            list_problem.append("第{0}行第4列,密码为6-13位数字，字母，特殊符号字符: ".format(row) +
                                            str(row_user_data[3]))
            return

        row_user_data[3] = str(row_user_data[3])

        #判断路径是否存在
        row_user_data[4] = str(row_user_data[4])
        path = row_user_data[4]
        if (not os.path.isfile(path)) or (os.path.getsize(path) >
                                            1024000):  #文件小于10mb
            string = "第{0}行第5列，不存在该路径或文件或文件过大，文件小于10mb ".format(
                row) + str(row_user_data[4])
            list_problem.append(string)
            return
        if not path.endswith('.jpg'):
            string = "第{0}行第4列，文件为jpg图片".format(row) + str(row_user_data[4])
            list_problem.append(string)
            return

        data = open(path, "rb").read(32)
        if not (data[6:10] in (b'JFIF', b'Exif')):
            string = "第{0}行第4列，文件为jpg图片".format(row) + str(row_user_data[4])
            list_problem.append(string)
            return

            ##opencv 不支持中文路径,用python图片库读取图片

        rgbImage =  getImg(row_user_data[4])
        #rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
        faces = detector(rgbImage)
        if len(faces) != 1:
            string = "第{0}行第5列，文件不存在人脸或多个人脸 ".format(row) + str(row_user_data[4])
            list_problem.append(string)
            return

        list2 = ["id_number", "user_name", "gender", "password", "img_path"]
        dic_user = dict(zip(list2, row_user_data))

        img_path = dic_user.pop("img_path")
        dic_user["salt"] = encryption.createSalt()
        dic_user["password"] = encryption.createMd5(
            dic_user["password"],dic_user["salt"],
            dic_user["id_number"])
        dic_user["vector"] = getVector(img_path)
        return tuple(dic_user.values()),img_path,dic_user["id_number"]
       
       


def insert(list_problem, row_user_data,row,lock = None):
    try:
        database.execute(
            f"INSERT INTO student (id_number,user_name,gender,password ,salt,vector) \
    VALUES ({PH},{PH}, {PH}, {PH} , {PH},{PH})",row_user_data)
           
    except sqlite3.IntegrityError:
        list_problem.append("第{0}行第1列,表中数据学号可能重复，请检查: ".format(row) +
                                str(row_user_data[0]))
        return False
    return True
        
def insertProcess(list_problem, row_user_data,row,lock = None):
    lock.acquire()
    try:
        database.execute(
            f"INSERT INTO student (id_number,user_name,gender,password ,salt,vector) \
    VALUES ({PH},{PH}, {PH}, {PH} , {PH},{PH})",row_user_data)
           
    except sqlite3.IntegrityError:
        list_problem.append("第{0}行第1列,表中数据学号可能重复，请检查: ".format(row) +
                                str(row_user_data[0]))
        lock.release()
        return False
    lock.release()
    return True






# def get_path():
#     path, _ = QFileDialog.getOpenFileName(
#         None, "选择文件", "c:\\", "Image files(*.jpg *.gif *.svg)")
#     if path == '':
#         return False
#     elif os.path.getsize(path) > 1024000 :
#         QMessageBox.critical(None, '警告', '文件应小于10mb')
#         return False
#     data = open(path,"rb").read(32)
#     if not (data[6:10] in (b'JFIF',b'Exif')):#检查文件类型是否属于jpg文件
#         QMessageBox.critical(None, '警告', '文件非图片文件')
#         return False
#     rgbImage = PIL.Image.open(path)
#     rgbImage  =  rgbImage .convert("RGB")
#     rgbImage =  np.array(rgbImage )
#     faces = models.detector(rgbImage)
#     if len(faces) == 1:
#         return path
#     else:
#         QMessageBox.critical(None, '警告', '文件不存在人脸或多个人脸')
#         return False
