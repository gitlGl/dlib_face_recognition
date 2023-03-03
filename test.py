# import datetime,sqlite3
# time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
# print(time)
# datetime.datetime.strptime(time,"%Y-%m-%d-%H-%M")

# conn = sqlite3.connect('./resources/company.db')
# def dict_factory(cursor, row):#重定义row_factory函数查询返回数据类型是字典形式
#             d = {}
#             for idx, col in enumerate(cursor.description):
#                 d[col[0]] = row[idx]
#             return d
# conn.row_factory = dict_factory

# c = conn.cursor()
# time = c.execute("select log_time from admin_log_time").fetchall ()[0]["log_time"]
# print(type(time))



import pickle
import pymysql,sqlite3,sqlite3paramstyle
from src.Creatuser import CreatUser
import numpy as np
print(pymysql.paramstyle)
print(sqlite3.paramstyle)
pymysql.paramstyle = "pyqmark"
c = pymysql
print(c.paramstyle)
print(pymysql.paramstyle)
#conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='study', charset='utf8')
conn = sqlite3paramstyle.connect('./resources/compan.db',isolation_level=None)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
username varchar(20),

createtime TIMESTAMP default (datetime('now', 'localtime'))

)'''
)
cursor.execute('insert into users(username) values ("jmk")')
conn.commit()
result = cursor.execute("select  createtime  from users ").fetchall()
print(result)
print(type(result[0][0]))
vector = CreatUser().get_vector("img_information/admin/12345678910/12345678910.jpg")
vector = str(vector)
print(vector)
vector = vector[2:-1]

print("select  obj  from test where obj = '{0}'".format(vector))
cursor.execute("select  obj  from test where obj = '{0}'".format(vector))

cursor.execute('insert into test(obj) values (%s)', (vector,))
print(type(vector))

cursor.execute('select  obj  from test where obj = ?', (vector,))
test = cursor.fetchall()[0][0]
pickle.loads(test)

cursor.execute('select  obj  from test where obj = %s', vector)
test = cursor.fetchall()
print(len(test))


cursor.execute('select * from test')
result = cursor.fetchall()
print(result)


# from PyQt5.QtWidgets import QApplication
# from src import main
# import sys
# from qss import StyleSheet
# from PyQt5.QtCore import QCoreApplication,QTimer
# from PyQt5.QtGui import QIcon,QFont
# from PyQt5 import QtCore
# from PyQt5.QtCore import QThread,pyqtSignal,QObject
# import numpy as np
# from PyQt5.QtGui import QImage
# from src.GlobalVariable import models
# class Work(QObject):
#     sinal = pyqtSignal()
#     def __init__(self,total_page=20):
#       super().__init__()

#     def tim(self):
#       print("timer")
#       print(QThread.currentThreadId(),self.tes)
#       self.time.stop()
#     def dowork(self):
#       self.time = QTimer()
#       self.time.timeout.connect(self.tim)
#       self.time.start(3)
#       print(QThread.currentThreadId(),self.tes)
#       self.sinal.emit()
#     def test(self):
#       print(QThread.currentThreadId())
#       self.tes = "tset"
      

# class cou(QObject):
#     def __init__(self,total_page=20):
#       super().__init__()
    
#       self.work =  Work()
      
#       self.threa = QThread()
#       self.work.moveToThread(self.threa)
      
#       self.threa.started.connect(self.work.dowork)
#       self.work.sinal.connect(self.sinal)
#     def sinal(self):
#       print("sinal")
      
      
   
    


# # app = QApplication(sys.argv)
# # window = cou()


# # print(QThread.currentThreadId())
# # window.work.test()
# # window.threa.start()


# # sys.exit(app.exec_())




