import sqlite3
class Database():
    def __init__(self):
        self.conn = sqlite3.connect('./resources/company.db',isolation_level=None)
        def dictFactory(cursor, row):#重定义row_factory函数查询返回数据类型是字典形式
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        self.conn.row_factory = dictFactory
        self.c = self.conn.cursor()

    def creatble(self):#528 李回复 2018035144217
        self.c.execute('''CREATE TABLE IF NOT EXISTS student
       ( 
        id_number        CHAR(50)    NOT NULL ,
   
        user_name       CHAR(50)    NOT NULL,
        gender           char(2)    NOT NULL, 
        password        char(20)    NOT NULL,
        img_path        char(60),
        vector          blob        ,
           
        salt            char(10)  NOT NULL ,
        cout              INT,
        PRIMARY KEY (id_number )
                 )without rowid;''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS student_log_time 
       ( 
        id_number              CHAR(50)    NOT NULL ,
        gender           bool,
 
        log_time datetime NOT NULL 
       
      
        );''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS admin
       ( 
        id_number            CHAR(50)    NOT NULL ,

       
        password        char(20)    NOT NULL,
        salt            char(10)  NOT NULL ,
        vector          blob        ,
        PRIMARY KEY (id_number )
                 )without rowid;''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS admin_log_time 
       ( 
        id_number             CHAR(50)    NOT NULL ,
      
        log_time datetime NOT NULL 
       
      
        );''')

     

    def insertUser(self, id_number, user_name,gender, password, img_path, vector,
                    salt):
        self.c.execute(
            "INSERT INTO student (id_number,user_name,gender,password ,img_path ,vector,salt) \
      VALUES (?,?, ?, ? , ?,?,?)",
            (id_number, user_name,gender, password, img_path, vector, salt))
      
        

    def delete(self, id):
        self.c.execute("delete from student where id_number = {0}".format(id))
        




