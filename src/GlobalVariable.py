import dlib,time,types
from enum import Enum
from .Database import Database,type_database

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
    self.conn.commit()
    return self.c.fetchall()
   

def execute_transaction(self,query:str,args :tuple = ()):
    self.c.execute(query,args)
    return self.c.fetchall()

def mysql_execute_query(self,query,args :tuple = ()):
    self.c.execute(query,args)
    return self.c.fetchall()
   
database = Database()
database.execute_transaction = types.MethodType(execute_transaction,database)
if type_database == "sqlite3" :
    execute_query = sqlite3_execute_query
    database.execute = types.MethodType(execute_query,database)
    #database.execute_transaction = types.MethodType(execute_transaction,database)
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
