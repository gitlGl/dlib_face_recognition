from .Database import database
from .Log import adminlog, studentlog
from .Setting import encoder
import numpy as np
from threading import Timer
import pickle
from . import Setting


def encodeFace(rgbImage, raw_face):
    return np.array(
        encoder.compute_face_descriptor(rgbImage, raw_face))

def compareFaces(face_encoding, test_encoding, axis=0):
    return np.linalg.norm(face_encoding - test_encoding, axis=axis)#计算欧式距离

    #与数据库人脸对比，相似度小于0.5则认为是同一个人
    #每一段时间重置face_data值


#用于学生进入图书馆是别
class StudentRgFace():
    def __init__(self):
       
        self.face_data = np.random.random(128).astype('float64')#初始化人脸编码，这个变量保存上一个人脸编码
        self.former_result = ""
        self.refreshthread = Timer(60, self.reset)
        self.refreshthread.setDaemon(True)
        self.refreshthread.start()
       
        self.list_vector = []
        results = database.execute("SELECT vector from student")
        #使用列表生成进行序列化
        self.list_vector = [pickle.loads(i['vector']) for i in results]
        
        self.list_idnumber = database.execute("SELECT id_number from student")
       

    def reset(self):
        self.face_data = np.random.random(128).astype('float64')
        self.refreshthread = Timer(60, self.reset)
        self.refreshthread.setDaemon(True)
        self.refreshthread.start()

    def rg(self, img, rgbImage, raw_face,
           share):  #优化识别流程，识别成功后避免同一人频繁识别，频繁记录数据
        face_data = encodeFace(rgbImage, raw_face)
        flag = compareFaces(face_data, self.face_data, axis=0)#计算欧式距离
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
        distances = compareFaces(np.array(self.list_vector), face_data, axis=1)#计算欧式距离
        min_distance_index = np.argmin(distances)
        print("距离", distances[min_distance_index])
        if distances[min_distance_index] < share:
            
            return min_distance_index
        
        return "验证失败"


class AdminRgFace():
    def __init__(self):
        super().__init__()
        
    def rgFace(self, img, rgbImage, raw_face):
        face_data = encodeFace(rgbImage, raw_face)
        list_vector = []
        results = database.execute("SELECT vector from admin")# 查询数据库中的数据:
        
        #使用列表生成进行序列化
        list_vector = [pickle.loads(i['vector']) for i in results]

        list_id_number = database.execute("SELECT id_number from admin")
       
        if len(list_vector) == 0:
            return False
        distances = compareFaces(np.array(list_vector), face_data, axis=1)
        min_distance = np.argmin(distances)
        print("距离", distances[min_distance])
        if distances[min_distance] < Setting.admin_threshold:
            
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

