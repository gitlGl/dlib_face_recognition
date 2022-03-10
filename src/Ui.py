import psutil
from .Creatuser import CreatStudentUser
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from src.Process import *
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import pyqtSlot,QTimer,Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import multiprocessing
from src.Help import Help
from PyQt5.QtWidgets import  QDialog
from multiprocessing import Process, Queue
from src.OpenCapture import OpenCapture
from src.Login import LoginUi
import os
class Ui(QWidget):
    def __init__(self):
        super().__init__()
        #self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setStyleSheet('QWidget{background:transparent}')
     
        
        #self.setFixedSize(480, 600)

        #self.setStyleSheet ("border:2px groove gray;border-radius:10px;padding:2px 2px;")
        self.groupbox_1 = QGroupBox()                       # 1
        self.groupbox_2 = QGroupBox()
        self.groupbox_1.setFixedSize(460,35)
        self.groupbox_2.setFixedSize(460,35)
        self.Vlayout = QVBoxLayout()
        self.Hlayout = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.allvlaout = QVBoxLayout()

        self.btn1 = QPushButton()
        self.btn2 = QCheckBox()
        self.btn3 = QCheckBox()
        self.btn4 = QPushButton()
        self.btn5 = QPushButton()
        self.btn1.setText("打开摄像头")
        self.btn1.setIcon(QIcon("./resources/摄像头_关闭.png"))
        self.btn2.setText("普通识别")
        self.btn3.setText("活体识别")
        self.btn4.setIcon(QIcon("./resources/文件.png"))
        self.btn4.setText("批量创建用户")
        self.btn5.setText("帮助")
        self.btn5.clicked.connect(self.help)
        self.btn5.setIcon(QIcon("./resources/帮助.png"))
        self.btn1.setStyleSheet("border:0px")
        self.btn4.setStyleSheet("border:0px;")
        self.btn5.setStyleSheet("border:0px;")
        self.btn4.clicked.connect(self.creat_student_user)


        self.btn1.clicked.connect(self.open)
        self.btn2.clicked.connect(self.open_normal)
        self.btn3.clicked.connect(self.open_eye)    
        # self.btn1.setFixedSize(100,20)
        # self.btn2.setFixedSize(100,20)
        self.qlabel1 = QLabel()
        self.qlabel2 = QLabel()
        self.qlabel3 = QLabel()
        self.qlabel4 = QLabel()
        self.qlabel3.setFixedSize(30,20)
        self.qlabel3.setFont(QFont("Arial",10))
        self.qlabel3.setAlignment(Qt.AlignCenter)
        self.qlabel3.setText("0.4")
        self.slider =  QSlider(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMaximum(12)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        self.slider.setValue(8)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.valueChange)
        self.slider.setFixedSize(100,20)
        self.slider.height()
      
       
       
        self.Hlayout.addWidget(self.btn1)
        self.Hlayout.addWidget(self.btn2)
        self.Hlayout.addWidget(self.btn3)
        self.Hlayout.addWidget(self.btn4)
        self.Hlayout.addWidget(self.btn5)
        self.groupbox_1.setLayout(self.Hlayout)

        self.Hlayout2.addWidget(self.qlabel1)
        self.Hlayout2.addWidget(self.qlabel2)
        self.Hlayout2.addWidget(self.slider)
        self.Hlayout2.addWidget(self.qlabel3)
        self.groupbox_2.setLayout(self.Hlayout2)
        
       
        self.Vlayout.addWidget(self.groupbox_1)
        self.Vlayout.addWidget(self.groupbox_2)
        self.Vlayout.addWidget(self.qlabel4)

        self.allvlaout.addLayout(self.Vlayout)
        self.resize(480, 600)
        self.setLayout(self.allvlaout)
        self.login_ui = LoginUi()
        self.login_ui.emitsingal.connect(self.show_parent)
        self.login_ui.show()
    @pyqtSlot()
    def show_parent(self):
     
        del self.login_ui
        gc.collect()
        self.Q1 = Queue()  # open_capture
        self.Q2 = Queue()
        self.share = multiprocessing.Value("f",0.4)
        self.open_capture = OpenCapture(self.Q1, self.Q2)
        self.p = Process(target=process_student_rg, args=(self.Q1, self.Q2,self.share))
        self.p.daemon = True
        self.open_capture.emit_img.connect(self.set_normal_img)
        self.open_capture.emit_result.connect(self.show_result)
        self.open_capture.emit_text.connect(self.change_text)
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_qlabel2)  
        self.show()
     

    #显示识别结果        
    @pyqtSlot(str)          
    def show_result(self,str_result):
        self.qlabel2.clear()
        self.qlabel2.setText(str_result)
        if not self.timer.isActive():
            self.timer.start(3000)

    #清除识别结果        
    def clear_qlabel2(self):
        self.timer.stop()
        self.qlabel2.clear()

    #刻度值槽函数    
    def valueChange(self):
        distance = round(self.slider.value()*0.05,2)
        self.share.value = distance
        self.qlabel3.setText(str(distance))

    #清理活体识别提示信息，设置提示信息
    @pyqtSlot(str)    
    def change_text(self,str):
        self.qlabel1.clear()
        self.qlabel1.setText(str)

    #帧显示视频流
    @pyqtSlot(QImage)
    def set_normal_img(self, image):
        self.qlabel4.setPixmap(QPixmap.fromImage(image))
        self.qlabel4.setScaledContents(True) 

    #创建用户
    def creat_student_user(self):
        path ,_= QFileDialog.getOpenFileName(
               self.parent, "选择文件", "c:\\", "files(*.xlsx )")
        if path == '':
            return        
        list_error = CreatStudentUser().creat_user(path)
        if len(list_error) == 0:
            QMessageBox.information(self.parent, 'Information', 'Register Successfully')
            return 
        else:
            error_string = ""
            for i in list_error:
                error_string = error_string + i + "\n"
            
            QMessageBox.information(self.parent, 'Information', error_string)
    #帮助页面        
    def help(self):
        self.help_qlabe = Help()
        self.help_qlabe.exec_()

    #正常识别
    def open_normal(self):
        if self.btn2.isChecked():  # 两个按钮互斥判断另一个按钮
            self.btn3.setChecked(False)
            self.btn2.setEnabled(False)
            self.btn3.setEnabled(True)
           
            while self.open_capture.timer1.isActive():
                self.open_capture.timer1.stop()
            while self.open_capture.timer2.isActive():
                self.open_capture.timer2.stop()
            while self.open_capture.timer1.isActive():
                self.open_capture.timer1.stop()
            while self.Q1.qsize() != 0:  # 清空队列 
                pass
            while self.Q2.qsize() != 0:
                self.Q2.get()          
            self.qlabel1.clear()   
            if self.open_capture.isRunning():
                if not self.open_capture.timer3.isActive():
                    self.open_capture.timer3.start(1000)
    #活体识别
    def open_eye(self):
    
        if self.btn3.isChecked(): 
            self.btn2.setChecked(False)
            self.btn3.setEnabled(False)
            self.btn2.setEnabled(True)    
            if self.open_capture.isRunning():
                if self.open_capture.timer3.isActive():
                    self.open_capture.timer3.stop()
                    while self.Q1.qsize() != 0:  # 清空队列 
                        pass
                    while self.Q2.qsize() != 0:
                        self.Q2.get()
            if self.open_capture.isRunning():
                if not self.open_capture.timer1.isActive():
                    self.open_capture.timer1.start(200)
                    self.qlabel1.setText("提示：请张嘴")
 
    def open(self):
        #self.open_capture.emit_img.connect(self.set_normal_img)
        self.btn1.clicked.disconnect(self.open)
        self.btn1.clicked.connect(self.close)
        self.btn1.setText("关闭摄像头")
        self.btn1.setIcon(QIcon("./resources/摄像头.png"))
        self.open_capture.start()
        if not self.p.is_alive():
            self.p.start()

        if psutil.Process(self.p.pid).status() == "stopped":
                psutil.Process(self.p.pid).resume()    
          
            
        if self.btn2.isChecked():
        
            if not self.open_capture.timer3.isActive():
                self.open_capture.timer3.start(1000)
                
        elif self.btn3.isChecked():
            if not self.open_capture.timer1.isActive():
                self.open_capture.timer1.start(200)
                self.qlabel1.setText("提示：请张嘴")

    def close(self):

        self.btn1.clicked.connect(self.open)
        self.btn1.clicked.disconnect(self.close)
        self.btn1.setText("打开摄像头")
        self.btn1.setIcon(QIcon("./resources/摄像头_关闭.png"))
        self.open_capture.close()  # 关闭摄像头
        
        while self.open_capture.timer3.isActive():
            self.open_capture.timer3.stop()

        while self.open_capture.timer1.isActive():
            self.open_capture.timer1.stop()
        while self.open_capture.timer2.isActive():
            self.open_capture.timer2.stop()
        while self.open_capture.timer1.isActive():
            self.open_capture.timer1.stop()

        while self.open_capture.timer3.isActive():
            self.open_capture.timer3.stop()
        while self.Q1.qsize() != 0:  # 清空队列 
                    pass
        while self.Q2.qsize() != 0:
                self.Q2.get()
        self.qlabel1.clear()
        self.qlabel4.clear()
        if psutil.Process(self.p.pid).status() == "running":
            psutil.Process(self.p.pid).suspend()  # 挂起进程
        time.sleep(0.5)
     

    def closeEvent(self,Event):
        if hasattr(self,"open_capture"):
            self.open_capture.close()

        # p = psutil.Process(os.getpid())
        # print(p.children())
        # for i in p.children():
        #     i.kill()
        # p.kill()
