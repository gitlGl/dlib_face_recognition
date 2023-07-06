import dlib
from enum import Enum
from .Database import Database
class models():
    def __init__(self):
        pass
    predictor = dlib.shape_predictor(
        "resources/shape_predictor_68_face_landmarks.dat")  # 4 获取人脸关键点检测模型
    detector = dlib.get_frontal_face_detector()  # 获取人脸模型
    encoder = dlib.face_recognition_model_v1(
                "resources/dlib_face_recognition_resnet_model_v1.dat")
    
class user(Enum):
    id_length = 10
    password_max_length = 20
    password_min_length = 6
    name_length = 20

class admin(Enum):
    id_length = 13
    password_max_length = 20
    password_min_length = 6
    


database = Database()
database.creatble()