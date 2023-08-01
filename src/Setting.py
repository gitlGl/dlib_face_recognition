from enum import Enum
import dlib,time,types,os,configparser
from enum import Enum
from .Database import Database,type_database

predictor = dlib.shape_predictor(
    "resources/shape_predictor_68_face_landmarks.dat")  # 4 获取人脸关键点检测模型
detector = dlib.get_frontal_face_detector()  # 获取人脸模型
encoder = dlib.face_recognition_model_v1(
            "resources/dlib_face_recognition_resnet_model_v1.dat")

class user(Enum):
    id_length = 13
    password_max_length = 20
    password_min_length = 6
    name_length = 20
    reg_pwd = "[A-Za-z0-9!@#$%^&*()_+\\-=\\[\\]{};':\"\\\\|,.<>\\/?]*"



file_name = "config.ini"
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
count_max,processes,process_exit,page_count = configRead("config.ini")

# process_exit = 100#进程退出码
# group_count = 10#每组人数
# count_max = 30#是否开启多进程
# processes = 3#进程数
# admin_threshold = 0.5#管理员人脸识别阈值
# user_threshold = 0.5#用户人脸识别阈值
# EYE_AR_THRESH = 0.05#眼睛长宽比
# MAR_THRESH = 0.5#嘴巴长宽比    


    
def log_slow_query(sql, execution_time):
    with open('slow_queries.log', 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}:{sql}\nExecution time: {execution_time} seconds\n\n")

def log_slow_queries(threshold):
    def decorator(func):
        def wrapper(self,query,args :tuple = ()):
            start_time = time.perf_counter()
            result = func(self,query,args)
            execution_time = self.end_time - start_time
            if execution_time > threshold:
                log_slow_query(self.sql, execution_time)
                
            return result
        return wrapper
    return decorator

def log_query(self,sql):
    self.end_time = time.perf_counter()
    self.sql = sql
    print(sql)
                        
    

@log_slow_queries(0.0001) # Set threshold to 0.01 second
def sqlite3_execute_query(self,query:str,args :tuple = ()):
    self.c.execute(query,args)
    #self.conn.commit()
    return self.c.fetchall()
   

def mysql_execute_query(self,query,args :tuple = ()):
    self.c.execute(query,args)
    return self.c.fetchall()
   
database = Database()

if type_database == "sqlite3" :
    execute_query = sqlite3_execute_query
    database.execute = types.MethodType(execute_query,database)
    database.log_query = types.MethodType(log_query,database)
    database.conn.set_trace_callback(database.log_query)
elif type_database == "mysql" :
    execute_query = mysql_execute_query
    database.execute = types.MethodType(execute_query,database)
database.creatble()

# mysqld慢查询日志配置
# slow_query_log = ON
# long_query_time = 1
# log_output = FILE
# slow_query_log_file = C:\ProgramData\MySQL\MySQL Server X.X\data\slow_queries.log
