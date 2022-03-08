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
    def __init__(self) -> None:
        super().__init__()
        self.label = QLabel(self)
        self.label.resize(480,530)
        self.Q1 = Queue()  # open_capture
 
        self.setWindowModality(Qt.WindowModal)
        self.show()

        while self.Q2.qsize() != 0:
            if self.Q2.get():
                self.open_capture.close()
                psutil.Process(self.p.pid).kill()
                self.emitsingal.emit()


    def closeEvent(self, event):
        self.open_capture.close()
        psutil.Process(self.p.pid).kill()
        #self.p.terminate
        print("test")

    @pyqtSlot(QImage)
    def set_normal_img(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label.setScaledContents(True) 
    