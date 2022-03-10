import random
from src.MyMd5 import MyMd5
from PyQt5.QtWidgets import QFileDialog
import face_recognition
import numpy as np
from src.Database import Database
import os, cv2
from src.GlobalVariable import models
import xlrd
from pathlib import Path
from PyQt5.QtCore import pyqtSignal
from src.Database import Database
from PyQt5.QtCore import pyqtSlot, QObject
class CreatUser():
    def __init__(self):
        pass
    def get_pass_word(self, salt, password="12345"):
        return MyMd5().create_md5(password, salt)

    def get_vector(self, id_number,img_path,fuck):
        """
        读取照片，获取人脸编码信息，把照片存储起来
        返回128维人脸编码信息
        """
        file_path =  img_path
        path =  "img_information/" + fuck+"/" +str(id_number) 

        img = cv2.imread(file_path)
        if img is None:
            return
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)    
        cv2.imwrite(
            "img_information/" +fuck + "/"+str(id_number) + "/" + str(id_number) +
            ".jpg", img)
        rgbImage = face_recognition.load_image_file(file_path)
        face = models.detector(rgbImage)[0]
        frame = models.predictor(rgbImage, face)
        face_data = np.array(
            models.encoder.compute_face_descriptor(rgbImage,frame))
        face_data = np.ndarray.dumps(face_data)
        return face_data

class CreatStudentUser(CreatUser):
    def __init__(self):
        super().__init__()

    def creat_user(self,path):
        book = xlrd.open_workbook(path)
        sheets = book.sheets()
        list_problem = []
        student =Database()

        for sheet in sheets:
            rows = sheet.nrows
            for i in range(1,rows):
                list1 =  sheet.row_values(rowx=i)
                #判断用户名是否符合格式要求
                if type(list1[0]) is str:
                    if list1[0].isdigit() and len(list1[0]) == 13:
                        user = student.c.execute("select id_number from student where id_number = {} ".format(int(list1[0]))).fetchall()
                        if len(user) == 1:
                            list_problem.append("第{0}行第1列,用户已存在: ".format(i) + str(list1[0]))
                            continue    
                        else: list1[0] = int(list1[0])    
                    else: 
                        list_problem.append("第{0}行第1列,用户名为文本格式13位数字 ".format(i) + str(list1[0]))
                        continue
                else:  
                    list_problem.append("第{0}行第1列，用户名为文本格式13位数字 ".format(i) + str(list1[0]))
                    continue
                #判断用户姓名是否符合格式要求
                lenth = len(str(list1[1]))
                if lenth < 16 and lenth != 0:
                    list1[1] = str(list1[1])
                    
                else:
                    list_problem.append("第{0}行第2列,姓名为16个字符以下: ".format(i) + str(list1[1]))
                    continue

                lenth = len(str(list1[2]))
                if lenth < 13 and lenth >= 6:
                    list1[2] = str(list1[2])

                #判断密码是否符合格式要求    
                else:
                    list_problem.append("第{0}行第3列,密码为6-13位字符: ".format(i) + str(list1[2]))
                    continue

                list1[3] = str(list1[3])
                path =  Path(list1[3])
                #判断路径是否存在
                if path.is_file():
                    rgbImage = face_recognition.load_image_file(path)
                    faces = models.detector(rgbImage)
                    if len (faces) == 1:
                        pass
                    else:
                        string = "第{0}行第4列，文件不存在人脸或多个人脸 ".format(i)+str(list1[3])
                        list_problem.append(string)
                  
                else:
                    string = "第{0}行第4列，不存在该路径或文件 ".format(i)+str(list1[3])
                    list_problem.append(string)
                    continue

                list2 = ["id_number","user_name","password","img_path" ]
                dic = dict(zip(list2,list1))
                information =  self.set_information(dic)
                self.insert_user(information)   
        student.conn.close()    
        return list_problem       
           

    def set_information(self, part_information):
        information = {}
        information["user_name"] = part_information["user_name"]
        information['salt'] = MyMd5().create_salt()
        information["img_path"] = self.get_img_path(part_information["id_number"])
        information["id_number"] = part_information["id_number"]
        information["password"] = self.get_pass_word(part_information["password"],information["salt"])
        information["vector"] = self.get_vector(part_information["id_number"],part_information["img_path"],"student")
        return information

    def insert_user(self,information):
        Database().insert_user(information["id_number"], information["user_name"], information["password"], 
        information["img_path"], information["vector"],
                           information["salt"])

    def get_img_path(self, id_number = 123456):
        path = "img_information/student/{0}/log".format(str(id_number))
        if not os.path.exists(path):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        return path