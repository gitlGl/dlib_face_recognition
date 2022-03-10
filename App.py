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
class APP(QWidget):

    def __init__(self):
        super().__init__()
 


    def closeEvent(self,Event):
        pass
        
        p = psutil.Process(os.getpid())
        print(p.children())
        for i in p.children():
            i.kill()
        p.kill()

 
if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = APP()
    ui = Ui(ex)
    #ex.ui.show()
    app.exec_()
    if hasattr(ui,"open_capture"):
        ui.open_capture.close()

