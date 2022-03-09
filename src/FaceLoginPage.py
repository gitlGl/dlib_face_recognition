import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from src.Studentdb import StudentDb
from src.MyMd5 import MyMd5
from src.OpenCapture import OpenCapture
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSlot,QTimer,Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from multiprocessing import Process, Queue
from src.Process import process_student_rg
import multiprocessing  
import psutil


class FaceLoginPage(QWidget):
    emit_show_parent = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self.label = QLabel(self)
        self.label.resize(480,530)
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_result)
        self.timer.start(1000)
        self.Q1 = Queue()  # open_capture
        self.Q2 = Queue()
        self.share = multiprocessing.Value("f",0.4)
        self.open_capture = OpenCapture(self.Q1, self.Q2)
        self.p = Process(target=process_student_rg, args=(self.Q1, self.Q2,self.share))
        self.p.start()
        self.open_capture.emit_img.connect(self.set_normal_img)
        self.open_capture.start()
        self.open_capture.timer3.start(1000)
        self.setWindowModality( Qt.ApplicationModal )
        self.show()
     
    def get_result(self):
        print("int")
        if  self.Q2.qsize() != 0:
            result =  self.Q2.get()
            print(result)
            if not result== "验证失败":
                if not result == "请先注册用户":
                    if self.open_capture.timer3.isActive():
                        self.open_capture.timer3.stop()
                    if self.timer.isActive():   
                        self.timer.stop()
                    self.open_capture.close()
                    psutil.Process(self.p.pid).kill()
                    self.emit_show_parent.emit()

    def closeEvent(self, event):
        if self.open_capture.timer3.isActive():
            self.open_capture.timer3.stop()
        if self.timer.isActive():
            print("tingzhi")   
            self.timer.stop()   
        self.open_capture.close()
        psutil.Process(self.p.pid).kill()
        #self.p.terminate


    @pyqtSlot(QImage)
    def set_normal_img(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label.setScaledContents(True) 
    