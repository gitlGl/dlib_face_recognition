from src.MyMd5 import MyMd5
import numpy as np
from src.Database import Database
from src.GlobalVariable import models
import xlrd ,os,PIL.Image
from src.Database import Database
class CreatUser():
    def __init__(self):
        pass

    def get_pass_word(self, salt, password="12345"):
        return MyMd5().create_md5(password, salt)

    def get_vector(self, id_number, img_path, fuck):
        """
        读取照片，获取人脸编码信息，把照片存储起来
        返回128维人脸编码信息
        """
        file_path = img_path
    
  
        path = "img_information/" + fuck + "/" + str(id_number)     
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
            
            ##opencv 不支持中文路径,用python图片库读取图片
        rgbImage = PIL.Image.open(file_path)
        rgbImage.save( "img_information/" + fuck + "/" + str(id_number) + "/" +
            str(id_number) + ".jpg")
        rgbImage  =  rgbImage .convert("RGB")
        rgbImage =  np.array(rgbImage )
  
        #rgbImage  =  rgbImage.convert("RGB")
        #rgbImage =  np.array(rgbImage )
        face = models.detector(rgbImage)[0]
        frame = models.predictor(rgbImage, face)
        face_data = np.array(
            models.encoder.compute_face_descriptor(rgbImage, frame))
        face_data = np.ndarray.dumps(face_data)
        print(type(face_data))
        return face_data


class CreatStudentUser(CreatUser):
    def __init__(self):
        super().__init__()

    def creat_user(self, path):
        book = xlrd.open_workbook(path)
        sheets = book.sheets()
        list_problem = []
        student = Database()

        for sheet in sheets:
            rows = sheet.nrows
            for i in range(1, rows):
                list1 = sheet.row_values(rowx=i)
                #判断用户名是否符合格式要求
              
                if str(list1[0]).isdigit() and len(str(list1[0])) == 13:
                    user = student.c.execute(
                        "select id_number from student where id_number = {} "
                        .format(str(list1[0]))).fetchall()
                    if len(user) == 1:
                        list_problem.append("第{0}行第1列,用户已存在: ".format(i) +
                                            str(list1[0]))
                        continue
                    else:
                        list1[0] = str(list1[0])
                   
                else:
                    list_problem.append("第{0}行第1列，用户名为13位数字 ".format(i) +
                                        str(list1[0]))
                    continue

                #判断用户姓名是否符合格式要求
                lenth = len(str(list1[1]))
                if lenth < 16 and lenth != 0:
                    list1[1] = str(list1[1])

                else:
                    list_problem.append("第{0}行第2列,姓名为16个字符以下: ".format(i) +
                                        str(list1[1]))
                    continue
                
                #判断用户性别格式
                if str(list1[2]) == "男" or str(list1[2]) == "女":
                    list1[2] = str(list1[2])
                else:
                    list_problem.append("第{0}行第3列,性别为男或女: ".format(i) +
                                        str(list1[2]))
                    continue

                #判断密码是否符合格式要求
                lenth = len(str(list1[3]))
                if lenth < 13 and lenth >= 6:
                    list1[3] = str(list1[3])

               
                else:
                    list_problem.append("第{0}行第4列,密码为6-13位字符: ".format(i) +
                                        str(list1[3]))
                    continue

           

                      #判断路径是否存在
                list1[4] = str(list1[4])
                path = list1[4]
               
                if  os.path.isfile(path) and os.path.getsize(path) < 1024000:#文件小于10mb
                    if path.endswith('.jpg') :
                        pass
                    else:
                        string = "第{0}行第4列，文件为jpg图片".format(i) + str( list1[4])
                        list_problem.append(string)
                        continue
                    data = open(path,"rb").read(32)
                    if not (data[6:10] in (b'JFIF',b'Exif')):
                        string = "第{0}行第4列，文件为jpg图片".format(i) + str( list1[4])
                        list_problem.append(string)
                        continue
    
                        ##opencv 不支持中文路径,用python图片库读取图片
                    rgbImage = PIL.Image.open(list1[4])
                    rgbImage  =  rgbImage .convert("RGB")
                    rgbImage =  np.array(rgbImage )
                    faces = models.detector(rgbImage)
                    if len(faces) == 1:
                        pass
                    else:
                        string = "第{0}行第5列，文件不存在人脸或多个人脸 ".format(i) + str(
                            list1[4])
                        list_problem.append(string)
                        continue

                else:
                    string = "第{0}行第5列，不存在该路径或文件或文件过大，文件小于10mb ".format(i) + str(list1[4])
                    list_problem.append(string)
                    continue


                list2 = ["id_number","user_name","gender", "password", "img_path"]
                dic = dict(zip(list2, list1))
                information = self.set_information(dic)
                self.insert_user(information)
        student.conn.close()
        return list_problem

    def set_information(self, part_information):
        information = {}
        information["user_name"] = part_information["user_name"]
        if part_information["gender"] == "男":
            information["gender"] = 1
        else:
            information["gender"] = 0 

        information['salt'] = MyMd5().create_salt()
        information["img_path"] = self.get_img_log_path(
            part_information["id_number"])
        information["id_number"] = part_information["id_number"]
        information["password"] = self.get_pass_word(
            part_information["password"], information["salt"])
        information["vector"] = self.get_vector(part_information["id_number"],
                                                part_information["img_path"],
                                                "student")
        return information

    def insert_user(self, information):
        Database().insert_user(information["id_number"],
                               information["user_name"],
                               information["gender"],
                               information["password"],
                               information["img_path"], information["vector"],
                               information["salt"])

    def get_img_log_path(self, id_number=123456):
        path = "img_information/student/{0}/log".format(str(id_number))
        if not os.path.exists(path):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        return path


# def get_path():
#     path, _ = QFileDialog.getOpenFileName(
#         None, "选择文件", "c:\\", "Image files(*.jpg *.gif *.png)")
#     if path == '':
#         return False
#     elif os.path.getsize(path) > 1024000 :
#         QMessageBox.critical(None, 'Wrong', '文件应小于10mb')
#         return False
#     data = open(path,"rb").read(32)
#     if not (data[6:10] in (b'JFIF',b'Exif')):#检查文件类型是否属于jpg文件
#         QMessageBox.critical(None, 'Wrong', '文件非图片文件')
#         return False
#     rgbImage = PIL.Image.open(path)
#     rgbImage  =  rgbImage .convert("RGB")
#     rgbImage =  np.array(rgbImage )
#     faces = models.detector(rgbImage)
#     if len(faces) == 1:
#         return path
#     else:
#         QMessageBox.critical(None, 'Wrong', '文件不存在人脸或多个人脸')
#         return False
  