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
        
        self.ui.btn1.clicked.connect(self.open_eye)
        self.ui.btn2.clicked.connect(self.open_normal)
        self.ui.btn3.clicked.connect(self.open)
       
    def creat_folder(self):
        if not os.path.exists("img_information"):  # 判断是否存在文件夹如果不存在则创建文件夹
            os.makedirs("img_information")

    
#完善批量创建用户功能

# 开启眨眼识别

    def open_eye(self):
        """
        btn2按钮按下
        """
        if self.ui.btn2.isChecked():  # 两个按钮互斥判断另一个按钮
            self.ui.btn2.setChecked(False)
            if self.open_capture.isRunning():
                if self.open_capture.timer3.isActive():
                    self.open_capture.timer3.stop()
                    while self.Q1.qsize() != 0:  # 清空队列
                        pass
                    while self.Q2.qsize() != 0:
                        self.Q2.get()
            if self.ui.btn1.isChecked():
                if self.open_capture.isRunning():
                    if psutil.Process(self.p.pid).status() == "stopped":
                        psutil.Process(self.p.pid).resume()
                        if not self.open_capture.timer1.isActive():
                            self.open_capture.timer1.start(200)
                            self.ui.qlabel1.setText("提示：请张嘴")
                            return
                    if not self.open_capture.timer1.isActive():
                        self.open_capture.timer1.start(200)
                        self.ui.qlabel1.setText("提示：请张嘴")
        else:  # 判断被按下的的按钮
            if self.ui.btn1.isChecked():
                if self.open_capture.isRunning():
                    if psutil.Process(self.p.pid).status() == "stopped":
                        psutil.Process(self.p.pid).resume()
                        if not self.open_capture.timer1.isActive():
                            self.open_capture.timer1.start(200)
                            self.ui.qlabel1.setText("提示：请张嘴")
                            return
                    if not self.open_capture.timer1.isActive():
                        self.open_capture.timer1.start(200)
                        self.ui.qlabel1.setText("提示：请张嘴")
           # 两个按钮同时是False的状态
        if ((self.ui.btn1.isChecked() is False) and (self.ui.btn2.isChecked() is False)):

            while self.open_capture.timer1.isActive():
                self.open_capture.timer1.stop()
            while self.open_capture.timer2.isActive():
                self.open_capture.timer2.stop()
            while self.open_capture.timer1.isActive():
                self.open_capture.timer1.stop()
            while self.open_capture.timer2.isActive():
                self.open_capture.timer2.stop()
            self.ui.qlabel1.clear()   
            if self.p.is_alive():
                if psutil.Process(self.p.pid).status() == "running":
            
                    while self.Q1.qsize() != 0:  # 清空队列
                        pass
                    while self.Q2.qsize() != 0:
                        self.Q2.get()
                    psutil.Process(self.p.pid).suspend()  # 挂起进程

    def open_normal(self):
        """
        btn2按钮按下
        两个按钮互斥
        """
        if self.ui.btn1.isChecked():  # 两个按钮互斥判断另一个按钮
            self.ui.btn1.setChecked(False)
            if self.open_capture.isRunning():  # 彻底关闭定时器
                while self.open_capture.timer1.isActive():
                    self.open_capture.timer1.stop()
                while self.open_capture.timer2.isActive():
                    self.open_capture.timer2.stop()
                while self.open_capture.timer1.isActive():
                    self.open_capture.timer1.stop()
                while self.open_capture.timer2.isActive():
                    self.open_capture.timer2.stop()
                self.ui.qlabel1.clear()   
                while self.Q1.qsize() != 0:  # 清空队列 
                    pass
                while self.Q2.qsize() != 0:
                    self.Q2.get()
            if self.ui.btn2.isChecked():
                if self.open_capture.isRunning():
                    if psutil.Process(self.p.pid).status() == "stopped":
                        psutil.Process(self.p.pid).resume()
                        if not self.open_capture.timer3.isActive():
                            self.open_capture.timer3.start(1000)
                            return
                    if not self.open_capture.timer3.isActive():
                        self.open_capture.timer3.start(1000)
        else:  # 判断被按下的的按钮
            if self.ui.btn2.isChecked():
                if self.open_capture.isRunning():
                    if psutil.Process(self.p.pid).status() == "stopped":
                        psutil.Process(self.p.pid).resume()
                        if not self.open_capture.timer3.isActive():
                            self.open_capture.timer3.start(1000)
                            return
                    if not self.open_capture.timer3.isActive():
                        self.open_capture.timer3.start(1000)
   # 两个按钮同时是False的状态
        if ((self.ui.btn1.isChecked() is False) and (self.ui.btn2.isChecked() is False)):
            while self.open_capture.timer3.isActive():
                self.open_capture.timer3.stop()
                while self.Q1.qsize() != 0:  # 清空队列
                    pass
                while self.Q2.qsize() != 0:
                    self.Q2.get()

                if psutil.Process(self.p.pid).status() == "running":
                    psutil.Process(self.p.pid).suspend()  # 挂起进程

    def open(self):
        #self.open_capture.emit_img.connect(self.ui.set_normal_img)
        self.ui.btn3.clicked.disconnect(self.open)
        self.ui.btn3.clicked.connect(self.close)
        self.ui.btn3.setText("关闭摄像头")
        self.ui.btn3.setIcon(QIcon("./resources/摄像头.png"))
        self.open_capture.start()
        if not self.p.is_alive():
            self.p.start()
            if ((self.ui.btn1.isChecked() is False) and (self.ui.btn2.isChecked() is False)):
                psutil.Process(self.p.pid).suspend()  # 挂起进程

        if self.ui.btn1.isChecked():
            if psutil.Process(self.p.pid).status() == "stopped":
                psutil.Process(self.p.pid).resume()
                if not self.open_capture.timer1.isActive():
                    self.open_capture.timer1.start(200)
                    self.ui.qlabel1.setText("提示：请张嘴")
                    return
            if not self.open_capture.timer1.isActive():
                self.open_capture.timer1.start(200)
                self.ui.qlabel1.setText("提示：请张嘴")
        if self.ui.btn2.isChecked():
            if psutil.Process(self.p.pid).status() == "stopped":
                psutil.Process(self.p.pid).resume()
                if not self.open_capture.timer3.isActive():
                    self.open_capture.timer3.start(1000)
                    return
            if not self.open_capture.timer3.isActive():
                self.open_capture.timer3.start(1000)

    def close(self):

        self.ui.btn3.clicked.connect(self.open)
        self.ui.btn3.clicked.disconnect(self.close)
        #self.open_capture.emit_img.disconnect(self.ui.set_normal_img)
        self.ui.btn3.setText("打开摄像头")
        self.ui.btn3.setIcon(QIcon("./resources/摄像头_关闭.png"))
        self.open_capture.close()  # 关闭摄像头
        self.open_capture.terminate()  # 关闭线程
        self.open_capture.wait()
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
    
        while self.Q1.qsize() != 0:  # 清空队列
            pass
        while self.Q2.qsize() != 0:
            self.Q2.get()
        if psutil.Process(self.p.pid).status() == "running":
            psutil.Process(self.p.pid).suspend()  # 挂起进程
        self.ui.qlabel1.clear()
        self.ui.qlabel.clear()
     
           
 
if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = APP()
    #ex.ui.show()
    app.exec_()
