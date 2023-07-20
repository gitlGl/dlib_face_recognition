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
    
def log_slow_query(query, execution_time):
    with open('slow_queries.log', 'a') as f:
        f.write(f'Slow query: {query}\nExecution time: {execution_time} seconds\n\n')

def log_slow_queries(threshold):
    def decorator(func):
        def wrapper(self,query):
            start_time = time.time()
            result = func(self,query)
            execution_time = time.time() - start_time
            if execution_time > threshold:
                log_slow_query(func.__name__, execution_time)
            return result
        return wrapper
    return decorator

@log_slow_queries(1.0) # Set threshold to 1 second
def sqlite3_execute_query(self,query):
    self.c.execute(query)
    results = self.c.fetchall()
    self.conn.commit()
    return results

def mysql_execute_query(self,query):
    self.c.execute(query)
    results = self.c.fetchall()
    self.conn.commit()
    return results
database = Database()
if type_database == "sqlite3" :
    execute_query = sqlite3_execute_query
    database.execute = types.MethodType(execute_query,database)
elif type_database == "mysql" :
    execute_query = mysql_execute_query
    database.execute = types.MethodType(execute_query,database)
database.creatble()

# mysqld慢查询日志配置
# slow_query_log = ON
# long_query_time = 1
# log_output = FILE
# slow_query_log_file = C:\ProgramData\MySQL\MySQL Server X.X\data\slow_queries.log
