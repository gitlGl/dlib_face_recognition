#import sqlite3
import sys
import configparser
##########兼容sqlite3和mysql
type_database = 'sqlite3'
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
            self.conn = sqlite3.connect('resources/company.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.conn.row_factory = dictFactory
            self.c = self.conn.cursor()

           
        elif type_database is 'mysql':
            from .model import configRead
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
        #id_number 字段应使用外键约束保证数据一致性 

    def insertUser(self, id_number, user_name,gender, password, vector,
                    salt):
        self.c.execute(
            f"INSERT INTO student (id_number,user_name,gender,password ,vector,salt) \
      VALUES ({PH},{PH}, {PH}, {PH} , {PH},{PH})",
            (id_number, user_name,gender, password,  vector, salt))
        self.conn.commit()
    def __del__(self):
        self.conn.close()
        






