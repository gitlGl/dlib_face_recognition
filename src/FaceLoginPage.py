from pickle import NONE
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from src.Database import Database
from src.MyMd5 import MyMd5
from src.OpenCapture import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSlot,QTimer,Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from multiprocessing import Process, Queue
#from src.Process import process_admin_rg, process_student_rg
import multiprocessing  
import psutil

from .Face import AdminRgFace
import cv2
from .GlobalVariable import *
class FaceLoginPage(QWidget):
    emit_show_parent = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self.label = QLabel(self)
        self.label.resize(480,530)
        self.setWindowModality( Qt.ApplicationModal )
        self.face_rg = AdminRgFace()
        self.capture = Capture()
        self.capture.emit_img.connect(self.set_normal_img)
        self.capture.start()        
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_result)
        self.timer.start(500)
        self.show()
     
    def get_result(self):
        self.timer.stop()
        rgbImage = cv2.cvtColor(self.capture.frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(rgbImage, cv2.COLOR_RGB2GRAY)
        location_faces = models.detector(gray)
        if len(location_faces) == 1:
            raw_face = models.predictor(gray, location_faces[0])
            result = self.face_rg.rg_face(self.capture.frame, rgbImage, raw_face)
            if result: 
              
                self.capture.close()
                self.emit_show_parent.emit()
                self.close     
        self.timer.start(500)
    def closeEvent(self, event):
        if self.timer.isActive():
            print("tingzhi")   
            self.timer.stop()   
        self.capture.close()
    @pyqtSlot(QImage)
    def set_normal_img(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label.setScaledContents(True) 
    




# class FaceLoginPage(QWidget):
#     emit_show_parent = pyqtSignal()
#     def __init__(self) -> None:
#         super().__init__()
#         self.label = QLabel(self)
#         self.label.resize(480,530)
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.get_result)
     
#         self.Q1 = Queue()  # capture
#         self.Q2 = Queue()
#         self.share = multiprocessing.Value("b",False)
#         self.capture = OpenCapture(self.Q1, self.Q2)
#         self.p = Process(target=process_admin_rg, args=(self.Q1,self.share))
#         self.p.daemon = True
#         self.p.start()
       
#         self.capture.emit_img.connect(self.set_normal_img)
#         self.capture.start()
#         self.capture.timer3.start(1000)
#         self.timer.start(500)
#         self.setWindowModality( Qt.ApplicationModal )
#         self.show()
     
#     def get_result(self):
#         self.timer.stop()
#         print("int")
#         if self.share.value == True:
#             self.emit_show_parent.emit()
#             self.capture.close()
#             psutil.Process(self.p.pid).kill()
#             print("kill")


#         self.timer.start(500)
#     def closeEvent(self, event):
#         if self.capture.timer3.isActive():
#             self.capture.timer3.stop()
#         if self.timer.isActive():
#             print("tingzhi")   
#             self.timer.stop()   
#         self.capture.close()
#         psutil.Process(self.p.pid).kill()



#     @pyqtSlot(QImage)
#     def set_normal_img(self, image):
#         self.label.setPixmap(QPixmap.fromImage(image))
#         self.label.setScaledContents(True) 
    
