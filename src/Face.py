from .GlobalVariable import database
from .Log import adminlog, studentlog
from .GlobalVariable import models
import numpy as np
from threading import Timer
import pickle

class Face():  #基类，包含人脸编码，人脸识别
    def __init__(self):

        pass

    #为人脸编码
    def encodeFace(self, rgbImage, raw_face):
        return np.array(
            models.encoder.compute_face_descriptor(rgbImage, raw_face))

    #计算人脸相似度，flaot值越小越相似
    def compareFaces(self, face_encoding, test_encoding, axis=0):
        return np.linalg.norm(face_encoding - test_encoding, axis=axis)#计算欧式距离

    #与数据库人脸对比，相似度小于0.5则认为是同一个人

    #每一段时间重置face_data值


#用于学生进入图书馆是别
class StudentRgFace(Face):
    def __init__(self):
        super().__init__()
        self.face_data = np.random.random(128).astype('float64')#初始化人脸编码，这个变量保存上一个人脸编码
        self.former_result = ""
        self.refreshthread = Timer(60, self.reset)
        self.refreshthread.setDaemon(True)
        self.refreshthread.start()
       
        self.list_vector = []
        database.c.execute("SELECT vector from student")
        #使用列表生成进行序列化
        self.list_vector = [pickle.loads(i['vector']) for i in database.c.fetchall()]
        
        database.c.execute("SELECT id_number from student")
        self.list_idnumber = database.c.fetchall()

    def reset(self):
        self.face_data = np.random.random(128).astype('float64')
        self.refreshthread = Timer(60, self.reset)
        self.refreshthread.setDaemon(True)
        self.refreshthread.start()

    def rg(self, img, rgbImage, raw_face,
           share):  #优化识别流程，识别成功后避免同一人频繁识别，频繁记录数据
        face_data = self.encodeFace(rgbImage, raw_face)
        flag = self.compareFaces(face_data, self.face_data, axis=0)#计算欧式距离
        if flag < share.value:
            return self.former_result
        
        result = self.rgFace(face_data, share.value)
        if result == "请先注册用户":
            return result
        print("result", result)
        if result == "验证失败":
            return result
        log = studentlog(self.list_idnumber[result]["id_number"], img)
        self.face_data = face_data#保存这次识别人脸编码，下次识别时比较是否是同一人
        self.former_result = "验证成功：" + log.item["user_name"]
        return "验证成功：" + log.item["user_name"]
        
    def rgFace(self, face_data, share):
        if len(self.list_vector) == 0:
            return "请先注册用户"
        distances = self.compareFaces(np.array(self.list_vector), face_data, axis=1)#计算欧式距离
        min_distance_index = np.argmin(distances)
        print("距离", distances[min_distance_index])
        if distances[min_distance_index] < share:
            
            return min_distance_index
        
        return "验证失败"


class AdminRgFace(Face):
    def __init__(self):
        super().__init__()
        self.value = 0.5

    def rgFace(self, img, rgbImage, raw_face):
        face_data = self.encodeFace(rgbImage, raw_face)
        list_vector = []
        database.c.execute("SELECT vector from admin")# 查询数据库中的数据:
        
        #使用列表生成进行序列化
        list_vector = [pickle.loads(i['vector']) for i in database.c.fetchall()]

        database.c.execute("SELECT id_number from admin")
        list_id_number = database.c.fetchall()
        if len(list_vector) == 0:
            return False
        distances = self.compareFaces(np.array(list_vector), face_data, axis=1)
        min_distance = np.argmin(distances)
        print("距离", distances[min_distance])
        if distances[min_distance] < self.value:
            
            log = adminlog(list_id_number[min_distance]["id_number"], img)
            id_number = list_id_number[min_distance]["id_number"]#返回管理员的id_number
            return id_number
            
        return False

# import numpy as np  
# import faiss  

# # 向量个数  
# num_vec = 5000  
# # 向量维度  
# vec_dim =   128
# # 搜索topk  
# topk = 5

# # 随机生成一批向量数据  
# vectors = np.random.rand(num_vec, vec_dim).astype('float32')


# # 创建索引  
# faiss_index = faiss.IndexFlatL2(vec_dim)  # 使用欧式距离作为度量 
# print(type(vectors))

# # 添加数据  
# faiss_index.add(vectors)  

# # 查询向量 假设有5个  
# query_vectors = np.random.rand(5, vec_dim).astype('float32')
# print(type(query_vectors))
# print(query_vectors)

# # 搜索结果  
# # 分别是 每条记录对应topk的距离和索引  
# # ndarray类型 。shape：len(query_vectors)*topk  
# res_distance, res_index = faiss_index.search(query_vectors, topk)  
# print("索引:",res_index)  
# print("距离:",res_distance)
# print(vectors[res_index[0]])

# # def creat_faiss(self):
# #         student = Database()
# #         self.list_vector = []
# #         for i in student.c.execute("SELECT vector from student"):#查询数据库中所有人脸编码
# #             i = np.loads(i["vector"])
# #             self.list_vector.append(i)
       
# #         if len(self.list_vector) == 0:
# #             return "请先注册用户"
# #         vec_dim = 128
# #         self.faiss_index = faiss.IndexFlatL2(vec_dim)  # 使用欧式距离作为度量  
# #         self.faiss_index.add(np.array(self.list_vector).astype('float32'))
# class AdminRgFace(Face):
#     def __init__(self):
#         super().__init__()
#         self.face_data = np.random.random(128).astype('float32')
#         self.refreshthread = Timer(10, self.reset)
#         self.refreshthread.setDaemon(True)
#         self.refreshthread.start()
#     def rg_face(self,img, rgbImage, raw_face,share):
#         face_data = self.encodeface(rgbImage, raw_face)
#         flag = self.compare_faces(face_data, self.face_data, axis=0)
#         if flag < 0.6:return ""
#         else:
#             admin = Database()
#             list_vector = []
#             for i in admin.c.execute("SELECT vector from admin"):
#                 i = np.loads(i[0])
#                 list_vector.append(i)
#             if len(list_vector) == 0:
#                 return False
#             distances = self.compare_faces(np.array(list_vector), face_data, axis=1)
#             min_distance = np.argmin(distances)
#             print("距离",distances[min_distance])
#             if distances[min_distance] < 0.4:
#                 share.value = True
#                 self.face_data = face_data
#                 tembyte = np.ndarray.dumps(list_vector[min_distance])
#                 adminlog(tembyte,img,admin)
#                 admin.conn.close()
#                 return "验证成功"
#             else:
#                 return  "验证失败"

#     def reset(self):
#         self.face_data = np.random.random(128).astype('float32')
#         self.refreshthread = Timer(10, self.reset)
#         self.refreshthread.setDaemon(True)
#         self.refreshthread.start()
