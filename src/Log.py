from src.Database import database
import datetime,cv2,os
class  studentlog():
    def __init__(self, vector,img):
      
        #用户信息
        item = database.c.execute(
                "SELECT  id_number,gender,img_path,cout,user_name from student where vector = ?",
                (vector, )).fetchall() # 取出返回所有数据，fetchall返回类型是[()]
        
                
        if(len(item) == 1):
            self.item = item[0]
            self.insertTime()
            self.insertImg(img)
            self.insertCout()
           
    #记录识别成功时间
    def insertTime(self):
        
        database.c.execute(
            "INSERT INTO student_log_time (id_number,gender,log_time ) \
      VALUES (?, ?,?)",
            (self.item["id_number"], self.item["gender"],datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))

       
        

        # test = self.database.c.execute(
        #     "SELECT database. user_name , database_log_time.log_time  FROM database \
        #      INNER JOIN database_log_time ON database.id_number = database_log_time.id_number\
        #      where log_time > '2022-03-03 23:24:05.835987' ORDER BY database_log_time.log_time").fetchall()
        # print(test)

    #记录识别成功时照片
    def insertImg(self, img):
        """
        向数据库插入识时照片
        """
        path = self.item["img_path"]
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        cv2.imwrite(
            path + "/" + self.getTime()+ ".jpg",
            img)
    def getTime(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
    #记录识别成功次数
    def insertCout(self):
        if self.item["cout"] == None:
            cout = 1
            database.c.execute(
            "UPDATE student SET cout = {0} WHERE id_number = {1}".format(cout,self.item["id_number"]),)
            
            return
           
    
        cout = self.item["cout"] + 1
        database.c.execute(
        "UPDATE student SET cout = {0} WHERE id_number = {1}".format(cout,self.item["id_number"]),)
       
        return
           
class  adminlog():
    def __init__(self, vector,img):
      
        
        #用户信息
        item = database.c.execute(
                "SELECT  id_number from admin where vector = ?",
                (vector, )).fetchall() # 取出返回所有数据，fetchall返回类型是[()]
        print(len(item))
        # while(True):
        #     item = self.database.c.execute(
        #         "SELECT  id_number,gender,img_path,cout,user_name from student where vector = ?",
        #         (vector, )).fetchall()
        #     if(len(item) == 1):
                # break
        if(len(item) == 1):
            self.item = item[0]
            self.inserImg(img)
            self.insertTime()
        else:
            pass #应该输出异常日志

    def insertTime(self):
        
        database.c.execute(
            "INSERT INTO admin_log_time (id_number,log_time ) \
      VALUES (?,?)",
            (self.item["id_number"], datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))

       
       

    def inserImg(self, img):
    
        path ="img_information/" +"admin/" +str(self.item["id_number"])+"/log"
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        cv2.imwrite(
            path + "/" + self.get_Time() + ".jpg",
            img)
    def get_Time(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))