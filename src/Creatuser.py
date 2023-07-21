from .MyMd5 import MyMd5
import numpy as np
from .GlobalVariable import models
import xlrd, os
from .GlobalVariable import database
import cv2, pickle
from PySide6.QtCore import Signal,QObject
from PySide6.QtWidgets import QApplication
from .GlobalVariable import user ,admin 


class CreatUser(QObject):
    sig_progress = Signal(int)
    sig_end = Signal(list)
    def __init__(self):
        super().__init__()
    def getImg(self, img_path):
        raw_data = np.fromfile(
            img_path, dtype=np.uint8)  #先用numpy把图片文件存入内存：raw_data，把图片数据看做是纯字节数据
        rgbImage = cv2.imdecode(raw_data, cv2.IMREAD_COLOR)  #从内存数据读入图片

        #rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
        return rgbImage

    def insertImg(self, id_number, img_path, fuck):
        path = "img_information/" + fuck + "/" + str(id_number)
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        rgbImage = self.getImg(img_path)
        cv2.imwrite(
            "img_information/" + fuck + "/" + str(id_number) + "/" +
            str(id_number) + ".jpg", rgbImage)

    def getVector(self, img_path):
        """
        读取照片，获取人脸编码信息，把照片存储起来
        返回128维人脸编码信息
        """
        rgbImage = self.getImg(img_path)
        face = models.detector(rgbImage)[0]
        frame = models.predictor(rgbImage, face)
        face_data = np.array(
            models.encoder.compute_face_descriptor(rgbImage, frame))
        face_data = pickle.dumps(face_data)
        return face_data

    def creatUser(self, path):
        book = xlrd.open_workbook(path)
        sheets = book.sheets()
        list_problem = []

        for sheet in sheets:
            rows = sheet.nrows
            for i in range(1, rows):
                QApplication.processEvents()
                self.sig_progress.emit(int(i/rows*100)) 
                list1 = sheet.row_values(rowx=i)
                #判断用户名是否符合格式要求
                if type(list1[0]) == float:
                    list1[0] = int(list1[0])

                if (not str(list1[0]).isdigit()) or len(
                    str(list1[0])) == user.id_length.value:
                    list_problem.append(
                        f"第{0}行第1列,用户id为{user.id_length.value}位数字 ".format(i) +
                                        str(list1[0]))
                    continue
                user_ = database.execute(
                    "select id_number from student where id_number = {} ".
                    format(str(list1[0])))
                if len(user_) == 1:
                    list_problem.append("第{0}行第1列,用户已存在: ".format(i) +
                                        str(list1[0]))
                    continue

                list1[0] = str(list1[0])

                #判断用户姓名是否符合格式要求
                lenth = len(str(list1[1]))
                if lenth > 16 or lenth == 0:

                    list_problem.append("第{0}行第2列,姓名为16个字符以下: ".format(i) +
                                        str(list1[1]))
                    continue
                list1[1] = str(list1[1])

                #判断用户性别格式
                if str(list1[2]) != "男" and str(list1[2]) != "女":
                    list_problem.append("第{0}行第3列,性别为男或女: ".format(i) +
                                        str(list1[2]))
                    continue
                list1[2] = str(list1[2])
                #判断密码是否符合格式要求

                lenth = len(str(list1[3]))
                if lenth > user.password_max_length.value or lenth < user.password_min_length.value:
                    list_problem.append("第{0}行第4列,密码为6-13位字符: ".format(i) +
                                        str(list1[3]))
                    continue

                list1[3] = str(list1[3])

                #判断路径是否存在
                list1[4] = str(list1[4])
                path = list1[4]
                if (not os.path.isfile(path)) or (os.path.getsize(path) >
                                                  1024000):  #文件小于10mb
                    string = "第{0}行第5列，不存在该路径或文件或文件过大，文件小于10mb ".format(
                        i) + str(list1[4])
                    list_problem.append(string)
                    continue
                if not path.endswith('.jpg'):
                    string = "第{0}行第4列，文件为jpg图片".format(i) + str(list1[4])
                    list_problem.append(string)
                    continue

                data = open(path, "rb").read(32)
                if not (data[6:10] in (b'JFIF', b'Exif')):
                    string = "第{0}行第4列，文件为jpg图片".format(i) + str(list1[4])
                    list_problem.append(string)
                    continue

                    ##opencv 不支持中文路径,用python图片库读取图片

                rgbImage = self.getImg(list1[4])
                #rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
                faces = models.detector(rgbImage)
                if len(faces) != 1:
                    string = "第{0}行第5列，文件不存在人脸或多个人脸 ".format(i) + str(list1[4])
                    list_problem.append(string)
                    continue

                list2 = [
                    "id_number", "user_name", "gender", "password", "img_path"
                ]
                dic = dict(zip(list2, list1))
                information = self.setInformation(dic)
                self.insertUser(information)
        self.sig_progress.emit(100)
        self.sig_end.emit(list_problem)

        return list_problem

    def setInformation(self, part_information):
        information = {}
        information["user_name"] = part_information["user_name"]
        information["gender"] = part_information["gender"]
        information['salt'] = MyMd5.createSalt()
        information["id_number"] = part_information["id_number"]
        information["password"] = MyMd5.createMd5(
            part_information["password"], information["salt"],
            part_information["id_number"])
        information["vector"] = self.getVector(part_information["img_path"])
        self.insertImg(part_information["id_number"],
                       part_information["img_path"], "student")
        return information

    def insertUser(self, information):
        database.insertUser(information["id_number"], information["user_name"],
                            information["gender"], information["password"],
                            information["vector"], information["salt"])




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
