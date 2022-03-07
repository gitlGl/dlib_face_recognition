
from src.Creatuser import CreatUser
from src.MyMd5 import MyMd5
import sys
from PyQt5.QtWidgets import QApplication,QWidget
import random
class timerexec():

    def __init__(self):
        print('这是构造函数')

    def __del__(self):
        print('这是析构函数')

class test(QWidget):
    def __init__(self):
        super().__init__()
        # self.id = random.randint(1, 20)
       
        # #self.vector = CreatUser().get_vector(self.id)
        # dic = {"id_number":self.id,"user_name":"lin","password":"123456","img_path":None }
        # CreatUser(dic)
        # a = timerexec()

    def te(self,str):
        def t():
            print("test")
        print(type(str))
        print ("" is type(str))
        t()
        

if __name__ == '__main__':
  

    app = QApplication(sys.argv)
    
    test1 = test()
    test1.te(str)
    
    
    app.exec()


