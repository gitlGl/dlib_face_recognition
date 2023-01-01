
import datetime,cv2,os
class  studentlog():
    def __init__(self, vector,img,database):
      
        self.database = database
        #用户信息
        item = self.database.c.execute(
                "SELECT  id_number,gender,img_path,cout,user_name from student where vector = ?",
                (vector, )).fetchall() # 取出返回所有数据，fetchall返回类型是[()]
        print(len(item))
        
                
        if(len(item) == 1):
            self.item = item[0]
            self.insert_time()
            self.insert_img(img)
            self.insert_cout()
            self.database.conn.close()
        else:
            pass #应该输出异常日志
    #记录识别成功时间
    def insert_time(self):
        
        self.database.c.execute(
            "INSERT INTO student_log_time (id_number,gender,log_time ) \
      VALUES (?, ?,?)",
            (self.item["id_number"], self.item["gender"],datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))

       
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
        path = self.item["img_path"]
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        cv2.imwrite(
            path + "/" + self.get_time()+ ".jpg",
            img)
    def get_time(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
    #记录识别成功次数
    def insert_cout(self):
        if self.item["cout"] == None:
            cout = 1
            self.database.c.execute(
            "UPDATE student SET cout = {0} WHERE id_number = {1}".format(cout,self.item["id_number"]),)
            self.database.conn.commit()
            return
           
    
        cout = self.item["cout"] + 1
        self.database.c.execute(
        "UPDATE student SET cout = {0} WHERE id_number = {1}".format(cout,self.item["id_number"]),)
        self.database.conn.commit()
        return
           
class  adminlog():
    def __init__(self, vector,img,database):
      
        self.database = database
        #用户信息
        item = self.database.c.execute(
                "SELECT  id_number from admin where vector = ?",
                (vector, )).fetchall() # 取出返回所有数据，fetchall返回类型是[()]
        print(len(item))
        print(item)
        # while(True):
        #     item = self.database.c.execute(
        #         "SELECT  id_number,gender,img_path,cout,user_name from student where vector = ?",
        #         (vector, )).fetchall()
        #     if(len(item) == 1):
                # break
        if(len(item) == 1):
            self.item = item[0]
            self.insert_img(img)
            self.insert_time()
        else:
            pass #应该输出异常日志

    def insert_time(self):
        
        self.database.c.execute(
            "INSERT INTO admin_log_time (id_number,log_time ) \
      VALUES (?,?)",
            (self.item["id_number"], datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))

       
        self.database.conn.commit()

    def insert_img(self, img):
    
        path ="img_information/" +"admin/" +str(self.item["id_number"])+"/log"
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        cv2.imwrite(
            path + "/" + self.get_time() + ".jpg",
            img)
    def get_time(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))