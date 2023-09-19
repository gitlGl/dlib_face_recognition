from enum import Enum
import dlib,os,configparser

import os

# 获取当前脚本文件的路径
current_file_path = os.path.abspath(__file__)

# 获取上两级目录的路径
base_dir = os.path.dirname(os.path.dirname(current_file_path))
resources_dir = base_dir + '\\resources\\'
img_dir = base_dir + '\\img_information\\'

predictor = dlib.shape_predictor(
    resources_dir + "shape_predictor_68_face_landmarks.dat")  # 4 获取人脸关键点检测模型
detector = dlib.get_frontal_face_detector()  # 获取人脸模型
encoder = dlib.face_recognition_model_v1(
            resources_dir + "dlib_face_recognition_resnet_model_v1.dat")

class user(Enum):
    id_length = 13
    password_max_length = 20
    password_min_length = 6
    name_length = 20
    reg_pwd = "[A-Za-z0-9!@#$%^&*()_+\\-=\\[\\]{};':\"\\\\|,.<>\\/?]*"


type_database = 'mysql' # 'sqlite3' or 'mysql
isVerifyeRemote = True
if isVerifyeRemote:
    ip = "localhost"
    port = 8888

file_name = base_dir +  "\\config.ini"
if not  os.path.exists(file_name):
      
    config = configparser.ConfigParser()    #实例化一个对象
    config["rember_pwd"] = {  'flag':'0','pwd':'' }     # 类似于操作字典的形式
    config["aotu_login"] = {'flag':'0','login_states':''}
    config['sql'] = {
            'host' : '127.0.0.1',
            'port' : '3306',
            'user' : 'user',
            'password' :'123456',
            'db_name' :'face_recognition',
            'charset' : 'utf8'
                    }
    config['setting'] = {
            'admin_threshold' : '0.5',
            'user_threshold' : '0.5',
            'EYE_AR_THRESH' : '0.05',
            'MAR_THRESH' : '0.5',
            'group_count' : '10',
            'count_max' : '30',
            'processes' : '3',
            'process_exit' : '100',
            'page_count' : '30'

            }
   

    with open(file_name, "w", encoding="utf-8") as f:
        config.write(f)   

def configRead(filePath:str):
    cfg = configparser.ConfigParser() 
    connect_user = {}
    cfg.read(filePath)
    if "sql" in cfg.sections():
        connect_user['host'] = cfg.get('sql','host')
        connect_user['port'] = cfg.getint('sql','port')
        connect_user['user'] = cfg.get('sql','user')
        connect_user['password'] = cfg.get('sql','password')
        connect_user['db'] = cfg.get('sql','db_name')
        connect_user['charset'] = cfg.get('sql','charset')
       
        return connect_user
    else:
        return None
    
if type_database == 'sqlite3':
    connect_user = file_name
else:
    connect_user = configRead(file_name)
    if connect_user is None:
        raise Exception("数据库配置文件错误")
    else:
        connect_user = connect_user



def configRead(filePath:str):
    cfg = configparser.ConfigParser() 
    cfg.read(filePath)
    if "setting" in cfg.sections():
        admin_threshold=cfg.getfloat('setting','admin_threshold')
        user_threshold=cfg.getfloat('setting','user_threshold')
        EYE_AR_THRESH=cfg.getfloat('setting','EYE_AR_THRESH')
        MAR_THRESH=cfg.getfloat('setting','MAR_THRESH')
        group_count=cfg.getint('setting','group_count')
        count_max=cfg.getint('setting','count_max')
        processes=cfg.getint('setting','processes')
        process_exit=cfg.getint('setting','process_exit')
        page_count=cfg.getint('setting','page_count')
        return admin_threshold,user_threshold,EYE_AR_THRESH,MAR_THRESH,\
               group_count,count_max,processes,process_exit,page_count
       
    else:
        return None,None,None,None,None,None,None

admin_threshold,user_threshold,EYE_AR_THRESH,MAR_THRESH,group_count,\
count_max,processes,process_exit,page_count = configRead(file_name)

# process_exit = 100#进程退出码
# group_count = 10#每组人数
# count_max = 30#是否开启多进程
# processes = 3#进程数
# admin_threshold = 0.5#管理员人脸识别阈值
# user_threshold = 0.5#用户人脸识别阈值
# EYE_AR_THRESH = 0.05#眼睛长宽比
# MAR_THRESH = 0.5#嘴巴长宽比    

