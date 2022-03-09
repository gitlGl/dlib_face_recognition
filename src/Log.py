
import datetime
import cv2
import os
class  studentlog():
    def __init__(self, vector,img,database):
      
        self.database = database
        #用户信息
        self.item = self.database.c.execute(
                "SELECT  * from student where vector = ?",
                (vector, )).fetchall()[0] # 取出返回所有数据，fetchall返回类型是[()]
        self.insert_time()
        self.insert_img(img)
        self.insert_cout()
        self.database.conn.close()      
    #记录识别成功时间
    def insert_time(self):
        
        self.database.c.execute(
            "INSERT INTO student_log_time (id_number,log_time ) \
      VALUES (?, ?)",
            (self.item[0], datetime.datetime.now()))

       
        self.database.conn.commit()

        # test = self.database.c.execute(
        #     "SELECT database. user_name , database_log_time.log_time  FROM database \
        #      INNER JOIN database_log_time ON database.id_number = database_log_time.id_number\
        #      where log_time > '2022-03-03 23:24:05.835987' ORDER BY database_log_time.log_time").fetchall()
        # print(test)

    #记录识别成功时照片
    def insert_img(self, img):
        """
        向数据库插入识时照片
        """
        path = self.item[3]
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        cv2.imwrite(
            path + "/" + self.get_time().replace(":", "-") + ".jpg",
            img)
    def get_time(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S "))
    #记录识别成功次数
    def insert_cout(self):
        if self.item[6] == None:
            cout = 1
            self.database.c.execute(
            "UPDATE student SET cout = {0} WHERE id_number = {1}".format(cout,self.item[0]),)
            self.database.conn.commit()
           
        else:
            cout = self.item[6] + 1
            self.database.c.execute(
            "UPDATE student SET cout = {0} WHERE id_number = {1}".format(cout,self.item[0]),)
            self.database.conn.commit()
           
class  adminlog():
    def __init__(self, vector,img,database):
      
        self.database = database
        #用户信息
        self.item = self.database.c.execute(
                "SELECT  * from admin where vector = ?",
                (vector, )).fetchall()[0] # 取出返回所有数据，fetchall返回类型是[()]
        self.insert_img(img)
    def insert_img(self, img):
    
        path ="img_information/" +"admin/" +str(self.item[0])+"/log"
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        cv2.imwrite(
            path + "/" + self.get_time().replace(":", "-") + ".jpg",
            img)
    def get_time(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S "))