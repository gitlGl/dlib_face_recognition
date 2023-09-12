##########兼容sqlite3和mysql
from .Setting import type_database,connect_user
import types,time
if type_database == 'sqlite3':
    print('sqlite3 loaded')
    import sqlite3
    PH = '?'
    Auto = 'AUTOINCREMENT'
    time_ =  "DATETIME DEFAULT (datetime('now','localtime'))"
elif type_database == 'mysql':
    print('mysql  loaded')
    import pymysql
    PH = '%s'
    Auto = 'AUTO_INCREMENT'
    time_ =  'DEFAULT CURRENT_TIMESTAMP'
#######


class Database():
    def __init__(self):
        def dictFactory(cursor, row):#重定义row_factory函数查询返回数据类型是字典形式
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        if type_database == 'sqlite3':
            sqlite3.enable_callback_tracebacks(True)
            self.conn = sqlite3.connect(connect_user, isolation_level = None,
                                        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.conn.row_factory = dictFactory
            self.c = self.conn.cursor()
        elif type_database == 'mysql':
            self.conn = pymysql.connect(**connect_user,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.conn.autocommit(True)
            self.c = self.conn.cursor()

        
    def creatble(self):#528 李回复 2018035144217
        self.c.execute('''CREATE TABLE IF NOT EXISTS student
       ( 
        id_number        CHAR(50)    UNIQUE NOT NULL ,
        user_name       CHAR(50)    NOT NULL,
        gender           char(4)    NOT NULL, 
        password        char(50)    NOT NULL,
        vector          blob        NOT NULL,
        salt            char(10)  NOT NULL ,
       count              INT,
        PRIMARY KEY (id_number )
                 );''')

        self.c.execute(f'''CREATE TABLE IF NOT EXISTS student_log_time 
       ( 
         id INTEGER PRIMARY KEY {Auto},
        id_number              CHAR(50)    NOT NULL ,
        gender           char(4)    NOT NULL,
 
        log_time TIMESTAMP  {time_}
      
        );''')
        #id_number 字段应使用外键约束保证数据一致性

        self.c.execute('''CREATE TABLE IF NOT EXISTS admin
       ( 
        id_number            CHAR(50)  UNIQUE  NOT NULL ,

        password        char(50)    NOT NULL,
        salt            char(10)  NOT NULL ,
        vector          blob       NOT NULL,
        PRIMARY KEY (id_number )
                 );''')
    
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS admin_log_time 
       ( 
        id INTEGER PRIMARY KEY {Auto},
        id_number             CHAR(50)    NOT NULL ,
      
        log_time TIMESTAMP {time_}
        );''')
        self.creatIndex()
        #id_number 字段应使用外键约束保证数据一致性 

    
    def creatIndex(self):
        if type_database == 'sqlite3':
                self.c.execute("CREATE INDEX IF NOT EXISTS idx_id_number_student ON student_log_time (id_number);")
                self.c.execute("CREATE INDEX IF NOT EXISTS idx_id_number_admin ON admin_log_time (id_number);")
                self.conn.commit() 
        elif type_database == 'mysql':
            self.c.execute('''
                        SELECT COUNT(*) FROM information_schema.statistics
                        WHERE table_schema = 'face_recognition'
                        AND table_name = 'student_log_time'
                        AND index_name = 'idx_id_number';
''')
            if self.c.fetchone()['COUNT(*)'] == 0:
                self.c.execute("CREATE INDEX  idx_id_number ON student_log_time (id_number(50));")
            self.c.execute('''
                        SELECT COUNT(*) FROM information_schema.statistics
                        WHERE table_schema = 'face_recognition'
                        AND table_name = 'admin_log_time'
                        AND index_name = 'idx_id_number';
''')

            if self.c.fetchone()['COUNT(*)'] == 0:
                self.c.execute("CREATE INDEX idx_id_number ON admin_log_time (id_number(50));")
            
        self.conn.commit()
    def __del__(self):
        self.conn.close()
        



def log_slow_query(sql, execution_time):
    with open('slow_queries.log', 'a',encoding= 'utf-8') as f:
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
def sqlite3_execute_query(self,query:str,args :tuple = None):
    self.c.execute(query,args)
    #self.conn.commit()
    return self.c.fetchall()
   

def mysql_execute_query(self,query,args :tuple = None):
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



