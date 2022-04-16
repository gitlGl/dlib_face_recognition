import os
import psutil
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout,QMessageBox,QMenu
from src.Process import process_student_rg
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
from PyQt5.QtGui import QIcon,QFont,QImage,QPixmap
from PyQt5.QtWidgets import QGroupBox,QCheckBox,QLabel
import multiprocessing
from src.Help import Help
from src.AdminInformation  import AdminInformation
from multiprocessing import Process, Queue
from .PutImg import PutImg
from src.Login import LoginUi
from .GlobalVariable import  GlobalFlag
import gc
from PyQt5.QtCore import QPoint
from src.Win import Win
import cv2,time
class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图书馆人脸识别系统")
        self.setWindowIcon(QIcon("resources/图书馆.png"))
        #self.setStyleSheet ("border:2px groove gray;border-radius:10px;padding:2px 2px;")
        self.groupbox_1 = QGroupBox()  # 1
        self.groupbox_2 = QGroupBox()
        self.groupbox_1.setFixedSize(460, 40)
        self.groupbox_2.setFixedSize(460, 35)
        self.Vlayout = QVBoxLayout()
        self.Hlayout = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.allvlaout = QVBoxLayout()

        self.btn1 = QPushButton(objectName="GreenButton")
        self.btn2 = QCheckBox()
        self.btn3 = QCheckBox()
        self.btn6 = QPushButton(objectName="GreenButton")
        self.btn4 = QPushButton(objectName="GreenButton")
        self.btn5 = QPushButton(objectName="GreenButton")

        self.btn1.setText("打开摄像头")
        self.btn1.setIcon(QIcon("./resources/摄像头_关闭.png"))
        self.btn2.setText("普通识别")
        self.btn3.setText("活体识别")
      
        self.btn4.setText("数据")
        self.btn5.setText("帮助")
        self.btn5.clicked.connect(self.help)
        self.btn4.setIcon(QIcon("./resources/数据.png"))
        self.btn5.setIcon(QIcon("./resources/帮助.png"))
        self.btn1.setFlat(True)
        self.btn5.setFlat(True)
        self.btn4.clicked.connect(self.analyze_data)
        self.btn1.clicked.connect(self.open)
        self.btn2.clicked.connect(self.open_normal)
        self.btn3.clicked.connect(self.open_eye)
        self.btn6.clicked.connect(lambda:self.pos_menu(self.btn6.pos()))

        self.btn6.setIcon(QIcon("./resources/用户.png"))
        self.btn6.setText("用户")
        self.qlabel1 = QLabel()
        self.qlabel2 = QLabel()
        self.qlabel3 = QLabel()
        self.qlabel4 = QLabel()
        self.qlabel5 = QLabel()#用于修复无法清理（qlable.claer()）图片
        self.qlabel5.hide()
        self.qlabel3.setFixedSize(30, 20)
        self.qlabel3.setFont(QFont("Arial", 10))
        self.qlabel3.setAlignment(Qt.AlignCenter)
        self.qlabel3.setText("0.4")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMaximum(12)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        self.slider.setValue(8)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.valueChange)
        self.slider.setFixedSize(100, 20)
        self.slider.height()

        self.Hlayout.addWidget(self.btn1)
        self.Hlayout.addWidget(self.btn2)
        self.Hlayout.addWidget(self.btn3)
        self.Hlayout.addWidget(self.btn4)
        self.Hlayout.addWidget(self.btn5)
        self.Hlayout.addWidget(self.btn6)
        self.groupbox_1.setLayout(self.Hlayout)

        self.Hlayout2.addWidget(self.qlabel1)
        self.Hlayout2.addWidget(self.qlabel2)
        self.Hlayout2.addWidget(self.slider)
        self.Hlayout2.addWidget(self.qlabel3)
        self.groupbox_2.setLayout(self.Hlayout2)

        self.Vlayout.addWidget(self.groupbox_1)
        self.Vlayout.addWidget(self.groupbox_2)
        self.Vlayout.addWidget(self.qlabel4)
        self.Vlayout.addWidget(self.qlabel5)
        self.allvlaout.addLayout(self.Vlayout)
        self.resize(480, 600)
        self.setLayout(self.allvlaout)
        self.login_ui = LoginUi()
        self.login_ui.emitsingal.connect(self.show_parent)
        self.login_ui.show()
    #退出登录
    def pos_menu(self,pos):
        pop_menu = QMenu()
        pop_menu.addAction("用户信息")
        pop_menu.addAction("退出登录")
        action = pop_menu.exec_(self.mapToGlobal(pos))
        if action == pop_menu.actions()[0]:
            self.admin_information = AdminInformation(self.id_number)
            self.admin_information.show()
        elif action == pop_menu.actions()[1]:
            if self.put_img.cap is not None:#判断摄像头状态
                if self.put_img.isRunning():
                    QMessageBox.information(self, 'Information', '请先关闭摄像头')
                    return  
            if self.p.is_alive():
                self.p.terminate()
            self.hide()
            self.login_ui = LoginUi()
            self.login_ui.emitsingal.connect(self.show_parent)
            self.login_ui.show()
       
    def analyze_data(self):
        self.view =Win()
        self.view.show()
        pass
    
    #登录成功后显示主界面
    @pyqtSlot(int)
    def show_parent(self,id_number):
        self.id_number = id_number
        print(self.id_number)
        print("test")
        del self.login_ui
        gc.collect()
        self.Q1 = Queue()  # put_img
        self.Q2 = Queue()
        self.share = multiprocessing.Value("f", 0.4)
        self.put_img = PutImg(self.Q1, self.Q2)
        self.p = Process(target=process_student_rg,
                         args=(self.Q1, self.Q2, self.share))
        self.p.daemon = True
        #self.put_img.emit_img.connect(self.set_normal_img)
        self.put_img.emit_result.connect(self.show_result)
        self.put_img.emit_text.connect(self.change_text)
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_qlabel2)#清除识别结果
        self.show()
        #self.login_ui.emitsingal.disconnect(self.show_parent)
       

    #显示识别结果
    @pyqtSlot(str)
    def show_result(self, str_result):
        self.qlabel2.clear()
        self.qlabel2.setText(str_result)
        self.qlabel1.clear()#清除提示
        if not self.timer.isActive():#开启清除识别结果
            self.timer.start(1500)

    #清除识别结果
    def clear_qlabel2(self):
        self.timer.stop()
        self.qlabel2.clear()
        if self.btn3.isChecked():
            self.qlabel1.setText("提示：请张嘴")


    #刻度值槽函数
    def valueChange(self):
        distance = round(self.slider.value() * 0.05, 2)
        self.share.value = distance
        self.qlabel3.setText(str(distance))

    #清理活体识别提示信息，设置提示信息
    @pyqtSlot(str)
    def change_text(self, str):
        self.qlabel1.clear()
        self.qlabel1.setText(str)

    #帧显示视频流
    @pyqtSlot(list,QImage)
    def set_normal_img(self, list_,img):
        self.put_img.frame = list_[0]#待识别帧
        self.qlabel4.setPixmap(QPixmap.fromImage(img))
        self.qlabel4.setScaledContents(True)

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

            while self.put_img.timer1.isActive():
                self.put_img.timer1.stop()
            while self.put_img.timer2.isActive():
                self.put_img.timer2.stop()
            while self.put_img.timer1.isActive():
                self.put_img.timer1.stop()
            while self.Q1.qsize() != 0:  # 清空队列
                pass
            while self.Q2.qsize() != 0:
                self.Q2.get()
            self.qlabel1.clear()
            if self.put_img.isRunning():
                if not self.put_img.timer3.isActive():
                    self.put_img.timer3.start(1000)

    #活体识别
    def open_eye(self):

        if self.btn3.isChecked():
            self.btn2.setChecked(False)
            self.btn3.setEnabled(False)
            self.btn2.setEnabled(True)
            GlobalFlag.gflag2 = False
            if self.put_img.isRunning():
                if self.put_img.timer3.isActive():
                    self.put_img.timer3.stop()
                    while self.Q1.qsize() != 0:  # 清空队列
                        pass
                    while self.Q2.qsize() != 0:
                        self.Q2.get()
            if self.put_img.isRunning():
                if not self.put_img.timer1.isActive():
                    self.put_img.timer1.start(200)
                    self.qlabel1.setText("提示：请张嘴")
                  

    def open(self):
        self.qlabel4.show()
        self.qlabel5.hide()##用于修复无法清理（qlable.claer()）图片
        self.put_img.emit_img.connect(self.set_normal_img)
        self.btn1.clicked.disconnect(self.open)
        self.btn1.clicked.connect(self.close)
        self.btn1.setText("关闭摄像头")
        self.btn1.setIcon(QIcon("./resources/摄像头.png"))
        self.put_img.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.put_img.start()
        if not self.p.is_alive():
            self.p.start()
            self.flag = True#子进程状态标志，True表示子进程已经启动
            
        # print(psutil.Process(self.p.pid).status())子进程状态不准确，不能用做恢复子进程的标志，
        # 因为子进程挂一段时间后状态会从“stopped”变为“running”，实质子进程状态仍然是“stopped”
        # print(self.p.is_alive())
        # print(psutil.Process(self.p.pid).is_running())
       

        if  self.flag == False:
            
            psutil.Process(self.p.pid).resume()
            self.flag = True##子进程状态标志，True表示子进程启动

        if self.btn2.isChecked():

            if not self.put_img.timer3.isActive():
                self.put_img.timer3.start(1000)

        elif self.btn3.isChecked():
            if not self.put_img.timer1.isActive():
                self.put_img.timer1.start(200)
                self.qlabel1.setText("提示：请张嘴")
               

    def close(self):
        print("open")
        
       
        self.put_img.emit_img.disconnect(self.set_normal_img)
       
        GlobalFlag.gflag2 = False

        self.btn1.clicked.connect(self.open)
        self.btn1.clicked.disconnect(self.close)
        self.btn1.setText("打开摄像头")
        self.btn1.setIcon(QIcon("./resources/摄像头_关闭.png"))
        self.put_img.close()  # 关闭摄像头
        self.qlabel4.setPixmap(QPixmap("./resources/摄像头.png"))

        while self.put_img.timer3.isActive():
            self.put_img.timer3.stop()

        while self.put_img.timer1.isActive():
            self.put_img.timer1.stop()
        while self.put_img.timer2.isActive():
            self.put_img.timer2.stop()
        while self.put_img.timer1.isActive():
            self.put_img.timer1.stop()

        while self.put_img.timer3.isActive():
            self.put_img.timer3.stop()
        print("测试队列")
        while self.Q1.qsize() != 0:  # 清空队列
            pass
        while self.Q2.qsize() != 0:
            print("get")
            self.Q2.get()
        self.qlabel1.clear()#清除提示信息
        if self.flag == True:
            psutil.Process(self.p.pid).suspend()  # 挂起进程
            self.flag = False#子进程状态标志，False表示子进程已经暂停
        self.qlabel4.clear()
        self.qlabel4.hide()#用于修复无法清理（qlable.claer()）图片
        self.qlabel5.show()

    def closeEvent(self, Event):
        if hasattr(self, "put_img"):
            self.put_img.close()
        super().closeEvent(Event)

        # p = psutil.Process(os.getpid())
        # print(p.children())
        # for i in p.children():
        #     i.kill()
        # p.kill()
