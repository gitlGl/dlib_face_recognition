import sys
import os
import psutil
from PyQt5.QtWidgets import QApplication, QWidget
from src import OpenCapture
from multiprocessing import Process, Queue
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSlot, QObject
from src import Ui
from PyQt5.QtGui import *
import time
import gc
from src import LoginUi
from src.Process import process_student_rg
class APP(QObject):

    def __init__(self):
        super().__init__()
        self.login_ui = LoginUi()
        self.login_ui.emitsingal.connect(self.init)
        self.login_ui.show()
        
    @pyqtSlot()
    def init(self):
        del self.login_ui
        gc.collect()
        self.creat_folder()
        self.Q1 = Queue()  # open_capture
        self.Q2 = Queue()
        self.open_capture = OpenCapture(self.Q1, self.Q2)
        self.ui = Ui(self.open_capture)
        self.ui.show()
        self.p = Process(target=process_student_rg, args=(self.Q1, self.Q2,self.ui.share))
        self.p.daemon = True
        self.ui.btn1.clicked.connect(self.open)
        self.ui.btn2.clicked.connect(self.open_normal)
        self.ui.btn3.clicked.connect(self.open_eye)             
       
    def creat_folder(self):
        if not os.path.exists("img_information"):  # 判断是否存在文件夹如果不存在则创建文件夹
            os.makedirs("img_information")

    def open_normal(self):
        if self.ui.btn2.isChecked():  # 两个按钮互斥判断另一个按钮
            self.ui.btn3.setChecked(False)
            self.ui.btn2.setEnabled(False)
            self.ui.btn3.setEnabled(True)
           
            while self.open_capture.timer1.isActive():
                self.open_capture.timer1.stop()
            while self.open_capture.timer2.isActive():
                self.open_capture.timer2.stop()
            while self.open_capture.timer1.isActive():
                self.open_capture.timer1.stop()
            while self.open_capture.timer2.isActive():
                self.open_capture.timer2.stop()
            self.ui.qlabel1.clear()   
            if self.open_capture.isRunning():
                if not self.open_capture.timer3.isActive():
                    self.open_capture.timer3.start(1000)

    def open_eye(self):
    
        if self.ui.btn3.isChecked(): 
            self.ui.btn2.setChecked(False)
            self.ui.btn3.setEnabled(False)
            self.ui.btn2.setEnabled(True)    
            if self.open_capture.isRunning():
                if self.open_capture.timer3.isActive():
                    self.open_capture.timer3.stop()
            if self.open_capture.isRunning():
                if not self.open_capture.timer1.isActive():
                    self.open_capture.timer1.start(200)
                    self.ui.qlabel1.setText("提示：请张嘴")
 
    def open(self):
        #self.open_capture.emit_img.connect(self.ui.set_normal_img)
        self.ui.btn1.clicked.disconnect(self.open)
        self.ui.btn1.clicked.connect(self.close)
        self.ui.btn1.setText("关闭摄像头")
        self.ui.btn1.setIcon(QIcon("./resources/摄像头.png"))
        self.open_capture.start()
        if not self.p.is_alive():
            self.p.start()

        if psutil.Process(self.p.pid).status() == "stopped":
                psutil.Process(self.p.pid).resume()    
          
            
        if self.ui.btn2.isChecked():
        
            if not self.open_capture.timer3.isActive():
                self.open_capture.timer1.start(1000)
                
        elif self.ui.btn3.isChecked():
            if not self.open_capture.timer1.isActive():
                self.open_capture.timer3.start(200)
                self.ui.qlabel1.setText("提示：请张嘴")

    def close(self):

        self.ui.btn1.clicked.connect(self.open)
        self.ui.btn1.clicked.disconnect(self.close)
        self.ui.btn1.setText("打开摄像头")
        self.ui.btn1.setIcon(QIcon("./resources/摄像头_关闭.png"))
        self.open_capture.close()  # 关闭摄像头
        
        while self.open_capture.timer3.isActive():
            self.open_capture.timer3.stop()

        while self.open_capture.timer1.isActive():
            self.open_capture.timer1.stop()
        while self.open_capture.timer2.isActive():
            self.open_capture.timer2.stop()
        while self.open_capture.timer1.isActive():
            self.open_capture.timer1.stop()
        while self.open_capture.timer2.isActive():
            self.open_capture.timer2.stop()
        self.ui.qlabel1.clear()
        self.ui.qlabel4.clear()
        if psutil.Process(self.p.pid).status() == "running":
            psutil.Process(self.p.pid).suspend()  # 挂起进程
        time.sleep(0.5)
     
           
 
if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = APP()
    #ex.ui.show()
    app.exec_()
