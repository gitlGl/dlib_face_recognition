
from ast import Return
import gc
from src.Studentdb import StudentDb
from src.Log import Log
from src.GlobalVariable import models
import numpy as np
from threading import Timer


class Face():

    def __init__(self):
        
        pass
    #为人脸编码
    def encodeface(self, rgbImage, raw_face):
        return np.array(
            models.encoder.compute_face_descriptor(rgbImage, raw_face))

    #计算人脸相似度，flaot值越小越相似
    def compare_faces(self, face_encoding, test_encoding, axis=0):
        return np.linalg.norm(face_encoding - test_encoding, axis=axis)

    #与数据库人脸对比，相似度小于0.5则认为是同一个人
    def rg_face(self,face_data,share):


        student = StudentDb()
        list = []
        for i in student.c.execute("SELECT vector from student"):
            i = np.loads(i[0])
            list.append(i)
        if len(list) == 0:
            return "请先注册用户" 
        distances = self.compare_faces(np.array(list), face_data, axis=1)
        min_distance = np.argmin(distances)
        print("距离",distances[min_distance])
        if distances[min_distance] < share:
            tembyte = np.ndarray.dumps(list[min_distance])
            student.conn.close() 
            return tembyte
        else:
            return  False

    
    #每一段时间重置face_data值
    
class StudentRgFace(Face):
        def __init__(self):
            super().__init__()
            self.face_data = np.random.random(128).astype('float32')
            self.former_result = ""
            self.refreshthread = Timer(10, self.reset)
            self.refreshthread.setDaemon(True)   
            self.refreshthread.start()
        def reset(self):
            self.face_data = np.random.random(128).astype('float32')
            self.refreshthread = Timer(10, self.reset)
            self.refreshthread.setDaemon(True) 
            self.refreshthread.start() 
        def rg(self, img, rgbImage, raw_face,share):#优化识别流程，识别成功后避免同一人频繁识别，频繁记录数据
            face_data = self.encodeface(rgbImage, raw_face)
            flag = self.compare_faces(face_data, self.face_data, axis=0)
            if flag < share.value:
                return self.former_result
            else:
                result = self.rg_face(face_data,share.value)
                if result == "请先注册用户":
                    return "请先注册用户"
                elif result:
                    self.face_data = face_data
                    
                    student = StudentDb()
                    log = Log(result,img,student)
                    student.conn.close()
                    self.former_result = "验证成功：" + log.item[1]
                    return "验证成功：" + log.item[1]
                else:
                    return "验证失败"
