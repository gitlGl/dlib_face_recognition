import sqlite3

import datetime
class StudentDb():

    def __init__(self):
        self.conn = sqlite3.connect('./resources/company.db')
        self.c = self.conn.cursor()
        self.creatble()
    
    def creatble(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS student
       ( 
        id_number       INT   NOT NULL ,
        user_name       CHAR(50)    NOT NULL,
        password        char(20)    NOT NULL,
        img_path        char(40),
        vector          blob        ,
           
        salt            char(10)  NOT NULL ,
        cout              INT,
        PRIMARY KEY (id_number )
                 )without rowid;''')
                 
        self.c.execute('''CREATE TABLE IF NOT EXISTS student_log_time
       ( 
        id_number            INT   NOT NULL ,
       
        log_time datetime NOT NULL 
       
      
        );''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS admin
       ( 
        id_number            INT   NOT NULL ,
       
        password        char(20)    NOT NULL,
        salt            char(10)  NOT NULL ,
        PRIMARY KEY (id_number )
                 )without rowid;''')
       
        self.conn.commit()

    def insert_user(self, id_number, user_name, password, img_path, vector, salt):
        self.c.execute(
            "INSERT INTO student (id_number,user_name,password ,img_path ,vector,salt) \
      VALUES (?, ?, ? , ?,?,?)",
            (id_number, user_name, password, img_path, vector, salt))
        self.conn.commit()

    def delete(self, id):
        self.c.execute("delete from student where id_number = {0}".format(id))
        self.conn.commit()


   
      


      