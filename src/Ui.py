
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
class Ui(QWidget):
    def __init__(self,open_capture):
        super().__init__()
        #self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setStyleSheet('QWidget{background:transparent}') 
        self.open_capture  = open_capture
        self.open_capture.emit_img.connect(self.set_normal_img)
        self.share = multiprocessing.Value("f",0.4)
       
        self.open_capture.emit_result.connect(self.show_result)
        self.open_capture.emit_text.connect(self.change_text)
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_qlabel2)
        
        #self.setFixedSize(480, 600)
        self.resize(480, 600)
        #self.setStyleSheet ("border:2px groove gray;border-radius:10px;padding:2px 2px;")
        self.groupbox_1 = QGroupBox( self)                       # 1
        self.groupbox_2 = QGroupBox( self)
        self.groupbox_1.setFixedSize(460,35)
        self.groupbox_2.setFixedSize(460,35)
        Vlayout = QVBoxLayout()
        Hlayout = QHBoxLayout()
        Hlayout2 = QHBoxLayout()
        allvlaout = QVBoxLayout()

        self.btn1 = QPushButton()
        self.btn2 = QCheckBox(self)
        self.btn3 = QCheckBox(self)
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
      
       
       
        Hlayout.addWidget(self.btn1)
        Hlayout.addWidget(self.btn2)
        Hlayout.addWidget(self.btn3)
        Hlayout.addWidget(self.btn4)
        Hlayout.addWidget(self.btn5)
        self.groupbox_1.setLayout(Hlayout)

        Hlayout2.addWidget(self.qlabel1)
        Hlayout2.addWidget(self.qlabel2)
        Hlayout2.addWidget(self.slider)
        Hlayout2.addWidget(self.qlabel3)
        self.groupbox_2.setLayout(Hlayout2)
        
       
        Vlayout.addWidget(self.groupbox_1)
        Vlayout.addWidget(self.groupbox_2)
        Vlayout.addWidget(self.qlabel4)

        allvlaout.addLayout(Vlayout)
        self.setLayout(allvlaout)
  
        self.setWindowTitle("测试")
    
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
    @pyqtSlot(str)    
    def change_text(self,str):
        self.qlabel1.clear()
        self.qlabel1.setText(str)

    @pyqtSlot(QImage)
    def set_normal_img(self, image):
        self.qlabel4.setPixmap(QPixmap.fromImage(image))
        self.qlabel4.setScaledContents(True)  

    def creat_student_user(self):
        path ,_= QFileDialog.getOpenFileName(
                self, "选择文件", "c:\\", "files(*.xlsx )")
        if path == '':
            return        
        list_error = CreatStudentUser().creat_user(path)
        if len(list_error) == 0:
            QMessageBox.information(self, 'Information', 'Register Successfully')
            return 
        else:
            error_string = ""
            for i in list_error:
                error_string = error_string + i + "\n"
            
            QMessageBox.information(self, 'Information', error_string)
    def help(self):
        self.help_qlabe = Help()
        self.help_qlabe.exec_()   
    def closeEvent(self, event): #关闭线程
        self.open_capture.terminate()
        self.open_capture.wait()
        if hasattr(self.open_capture,"cap"):
            
            self.open_capture.close()
    