
import datetime
import cv2
import os

class Log():

    def __init__(self, vector,img,student):
        self.student = student
        self.item = self.student.c.execute(
                "SELECT  * from student where vector = ?",
                (vector, )).fetchall()[0] # 取出返回所有数据，fetchall返回类型是[()]
        self.insert_time()
        self.insert_img(img)
        self.insert_cout()
        self.student.conn.close()      

    def insert_time(self):
        
        self.student.c.execute(
            "INSERT INTO student_log_time (id_number,log_time ) \
      VALUES (?, ?)",
            (self.item[0], datetime.datetime.now()))

       
        self.student.conn.commit()

        # test = self.student.c.execute(
        #     "SELECT student. user_name , student_log_time.log_time  FROM student \
        #      INNER JOIN student_log_time ON student.id_number = student_log_time.id_number\
        #      where log_time > '2022-03-03 23:24:05.835987' ORDER BY student_log_time.log_time").fetchall()
        # print(test)

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

    def insert_cout(self):
        if self.item[6] == None:
            cout = 1
            self.student.c.execute(
            "UPDATE student SET cout = {0} WHERE id_number = {1}".format(cout,self.item[0]),)
            self.student.conn.commit()
           
        else:
            cout = self.item[6] + 1
            self.student.c.execute(
            "UPDATE student SET cout = {0} WHERE id_number = {1}".format(cout,self.item[0]),)
            self.student.conn.commit()
           
