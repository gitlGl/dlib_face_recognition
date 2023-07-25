#import sqlite3
import configparser
##########兼容sqlite3和mysql
type_database = 'mysql' # 'sqlite3' or 'mysql
if type_database is 'sqlite3':
    print('sqlite3 loaded')
    import sqlite3
    PH = '?'
    Auto = 'AUTOINCREMENT'
    time =  "DATETIME DEFAULT (datetime('now','localtime'))"
elif type_database is 'mysql':
    print('mysql  loaded')
    import pymysql
    PH = '%s'
    Auto = 'AUTO_INCREMENT'
    time =  'DEFAULT CURRENT_TIMESTAMP'

#######
def configRead(filePath:str):
    cfg = configparser.ConfigParser() 
    cfg.read(filePath)
    if "sql" in cfg.sections():
        host=cfg.get('sql','host')
        port=cfg.getint('sql','port')
        user=cfg.get('sql','user')
        passwd=cfg.get('sql','password')
        dbName=cfg.get('sql','db_name')
        charset=cfg.get('sql','charset')
        return host,port,user,passwd,dbName,charset
    else:
        return None,None,None,None,None,None,None
class Database():
    def __init__(self):
        def dictFactory(cursor, row):#重定义row_factory函数查询返回数据类型是字典形式
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        if type_database is 'sqlite3':
            sqlite3.enable_callback_tracebacks(True)

            
            self.conn = sqlite3.connect('resources/data.db', isolation_level = None,
                                        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            
            self.conn.row_factory = dictFactory

            self.c = self.conn.cursor()
           
        
           
        elif type_database is 'mysql':
            host,port,user,password,dbName,charset = configRead("config.ini")
           
            self.conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                passwd=password,
                db=dbName,
                charset=charset,
                cursorclass=pymysql.cursors.DictCursor

            )
            self.conn.autocommit(False)
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
 
        log_time TIMESTAMP  {time}
      
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
      
        log_time TIMESTAMP {time}
        );''')
        self.creatIndex()
        #id_number 字段应使用外键约束保证数据一致性 

    def insertUser(self, id_number, user_name,gender, password, vector,
                    salt):
        self.c.execute(
            f"INSERT INTO student (id_number,user_name,gender,password ,vector,salt) \
      VALUES ({PH},{PH}, {PH}, {PH} , {PH},{PH})",
            (id_number, user_name,gender, password,  vector, salt))
        self.conn.commit()
    def creatIndex(self):
        if type_database is 'sqlite3':
                self.c.execute("CREATE INDEX IF NOT EXISTS idx_id_number_student ON student_log_time (id_number);")
                self.c.execute("CREATE INDEX IF NOT EXISTS idx_id_number_admin ON admin_log_time (id_number);")
                self.conn.commit() 
        elif type_database is 'mysql':
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
        






