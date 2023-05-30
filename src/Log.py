from .GlobalVariable import database
import datetime,cv2,os
class  studentlog():
    def __init__(self, vector,img):
      
        #用户信息
        item = database.c.execute(
                "SELECT  id_number,gender,count,user_name from student where vector = ? limit 1",
                (vector, )).fetchall() # 取出返回所有数据，fetchall返回类型是[()]
        
        print(len(item))
        if(len(item) == 1):
            self.item = item[0]
            self.insertTime()
            self.insertImg(img)
            self.insertCout()
            database.conn.commit()
           
    #记录识别成功时间
    def insertTime(self):
        database.c.execute(
            "INSERT INTO student_log_time (id_number,gender,log_time ) \
      VALUES (?, ?,?)",
            (self.item["id_number"], self.item["gender"],datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))

       
        


    #记录识别成功时照片
    def insertImg(self, img):
        """
        向数据库插入识时照片
        """
        path ="img_information/" +"student/" +str(self.item["id_number"])+"/log"
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        cv2.imwrite(
            path + "/" + self.getTime()+ ".jpg",
            img)
    def getTime(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
    #记录识别成功次数
    def insertCout(self):
        if self.item["count"] == None:
            count = 1
            database.c.execute(
            "UPDATE student SET count = {0} WHERE id_number = {1}".format(count,self.item["id_number"]),)
            
            return
           
    
        count = self.item["count"] + 1
        database.c.execute(
        "UPDATE student SET count = {0} WHERE id_number = {1}".format(count,self.item["id_number"]),)
       
        return
           
class  adminlog():
    def __init__(self, vector,img):
      
        
        #用户信息
        item = database.c.execute(
                "SELECT  id_number from admin where vector = ? limit 1",
                (vector, )).fetchall() # 取出返回所有数据，fetchall返回类型是[()]
        print(len(item))
     
        if(len(item) == 1):
            self.item = item[0]
            self.inserImg(img)
            self.insertTime()
            database.conn.commit()
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