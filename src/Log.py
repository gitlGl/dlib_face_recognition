from .GlobalVariable import database
import datetime,cv2,os
from .Database import PH
class  studentlog():
    def __init__(self, id_number,img):
      
        #用户信息
        item =  database.execute(
                f"SELECT  id_number,gender,count,user_name from student where id_number = {PH} ",
                (id_number, ))# 取出返回所有数据，fetchall返回类型是[()]
        
        
        self.item = item[0]
        self.insertTime()
        self.insertImg(img)
        self.insertCout()
        
           
    #记录识别成功时间
    def insertTime(self):
        database.execute(
            f"INSERT INTO student_log_time (id_number,gender ) VALUES ({PH}, {PH})",
            (self.item["id_number"],self.item["gender"],))

       
        


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
            database.execute(
            "UPDATE student SET count = {0} WHERE id_number = {1}".format(count,self.item["id_number"]),)
            
            return
           
    
        count = self.item["count"] + 1
        database.execute(
        "UPDATE student SET count = {0} WHERE id_number = {1}".format(count,self.item["id_number"]),)
       
        return
           
class  adminlog():
    def __init__(self, id_number,img):
      
        
        #用户信息
        item =   database.execute(
                f"SELECT  id_number from admin where id_number = {PH} ",
                (id_number, ))# 取出返回所有数据，fetchall返回类型是[()]
        
        self.item = item[0]
        self.inserImg(img)
        self.insertTime()
        

    def insertTime(self):
        
        database.execute(
            f"INSERT INTO admin_log_time (id_number) \
      VALUES ({PH})",
            (self.item["id_number"],))

       
       

    def inserImg(self, img):
    
        path ="img_information/" +"admin/" +str(self.item["id_number"])+"/log"
        if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        cv2.imwrite(
            path + "/" + self.get_Time() + ".jpg",
            img)
    def get_Time(self):   
        return str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))