import cv2,gc,multiprocessing,psutil,os
from PyQt5.QtWidgets import QWidget, QMessageBox,QMenu
from src.Process import process_student_rg 
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QIcon,QPixmap
from src.Help import Help
from src.AdminInformation  import AdminInformation
from multiprocessing import Process, Queue
from .PutImg import PutImg
from src.Login import LoginUi
from .GlobalVariable import  GlobalFlag
from src.ShowData import ShowData
from .Plugins import Plugins
from .Login import LoginUi
from .Ui import Ui
class main(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui()
        self.ui.setupUi(self)
        self.Q1 = Queue()  # put_img
        self.Q2 = Queue()
        self.share = multiprocessing.Value("f", 0.4)
        self.put_img = PutImg(self.Q1, self.Q2)
        self.put_img.emit_result.connect(self.show_result)
        self.put_img.emit_text.connect(self.change_text)
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_qlabel2)#清除识别结果

        self.login_ui = LoginUi()
        self.login_ui.emitsingal.connect(self.show_parent)
        self.login_ui.show()
    #退出登录
    def pos_menu(self,pos):
        if(self.show_error()):
             return
        pop_menu = QMenu(self.ui)
        pop_menu.addAction("用户信息")
        pop_menu.addAction("退出登录")
        action = pop_menu.exec_(self.ui.mapToGlobal(pos))
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
            self.ui.hide()
            self.login_ui = LoginUi()
            self.login_ui.emitsingal.connect(self.show_parent)
            self.login_ui.show()
    def show_error(self):
        if(self.put_img.isRunning()):
             QMessageBox.critical(self, 'Wrong', '请先关闭摄像头')
             return True
             
    def show_data(self):
        if(self.show_error()):
             return
        self.view =ShowData()
        self.view.show()
        pass

       #插件菜单
    def pos_menu_plugins(self,pos):#pos是按钮坐标
        path = os.path.abspath("./src/plugins")#获取绝对路径
        controls_class = Plugins(path).load_plugins()
        pop_menu = QMenu()
        for label,clazz in controls_class.items():
            pop_menu.addAction(label)
        action = pop_menu.exec_(self.mapToGlobal(pos))
        if action:

            self.win = (controls_class[action.text()]())
            self.win.show()
        
    
    #登录成功后显示主界面
   # @pyqtSlot(str)
    def show_parent(self,id_number):
        self.id_number = id_number
        del self.login_ui
        gc.collect()
        self.p = Process(target=process_student_rg,
                         args=(self.Q1, self.Q2, self.share))
        self.p.daemon = True
        self.ui.show()
     
       

    #显示识别结果
    @pyqtSlot(str)
    def show_result(self, str_result):
        self.ui.qlabel2.clear()
        self.ui.qlabel2.setText(str_result)
        self.ui.qlabel1.clear()#清除提示
        if not self.timer.isActive():#开启清除识别结果
            self.timer.start(1500)

    #清除识别结果
    def clear_qlabel2(self):
        self.timer.stop()
        self.ui.qlabel2.clear()
        if self.ui.btn3.isChecked() and self.put_img.isRunning(): #and self.put_img.isRunning()
            self.ui.qlabel1.setText("提示：请张嘴")


    #刻度值槽函数
    def valueChange(self):
        distance = round(self.slider.value() * 0.05, 2)
        self.share.value = distance
        self.ui.qlabel3.setText(str(distance))

    #清理活体识别提示信息，设置提示信息
    @pyqtSlot(str)
    def change_text(self, str):
        self.ui.qlabel1.clear()
        self.ui.qlabel1.setText(str)

    #帧显示视频流
    #@pyqtSlot(list,QImage)
    def set_normal_img(self, img):    
        #self.put_img.frame = list_[0]#待识别帧
        #设置图片，图片跟随ui.qlabel大小缩放
        self.ui.qlabel4.setPixmap(QPixmap.fromImage(img))
        #QPixmap.fromImage(img).scaled(self.ui.qlabel4.size(),Qt.KeepAspectRatio)图片跟随ui.qlabel大小缩放
        self.ui.qlabel4.setScaledContents(True)#ui.qlabel4自适应图片大小

    #帮助页面
    def help(self):
        if(self.show_error()):
             return
        self.help_qlabe = Help()
        self.help_qlabe.exec_()

    #正常识别
    def open_normal(self):
        if self.ui.btn2.isChecked():  # 两个按钮互斥判断另一个按钮
            self.ui.btn3.setChecked(False)
            self.ui.btn2.setEnabled(False)
            self.ui.btn3.setEnabled(True)

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
            self.ui.qlabel1.clear()
            if self.put_img.isRunning():
                if not self.put_img.timer3.isActive():
                    self.put_img.timer3.start(1000)

    #活体识别
    def open_eye(self):

        if self.ui.btn3.isChecked():
            self.ui.btn2.setChecked(False)
            self.ui.btn3.setEnabled(False)
            self.ui.btn2.setEnabled(True)
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
                    self.ui.qlabel1.setText("提示：请张嘴")
                  

    def open(self):
        self.ui.qlabel4.show()
        self.ui.qlabel5.hide()##用于修复无法清理（qlable.claer()）图片
        self.put_img.emit_img.connect(self.set_normal_img)
        self.ui.btn1.clicked.disconnect(self.open)
        self.ui.btn1.clicked.connect(self.close)
        self.ui.btn1.setText("关闭摄像头")
        self.ui.btn1.setIcon(QIcon("./resources/摄像头.png"))
        self.put_img.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.put_img.start()
        self.put_img.priority
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

        if self.ui.btn2.isChecked():

            if not self.put_img.timer3.isActive():
                self.put_img.timer3.start(1000)

        elif self.ui.btn3.isChecked():
            if not self.put_img.timer1.isActive():
                self.put_img.timer1.start(200)
                self.ui.qlabel1.setText("提示：请张嘴")
               

    def close(self):
        self.put_img.emit_img.disconnect(self.set_normal_img)
       
        GlobalFlag.gflag2 = False

        self.ui.btn1.clicked.connect(self.open)
        self.ui.btn1.clicked.disconnect(self.close)
        self.ui.btn1.setText("打开摄像头")
        self.ui.btn1.setIcon(QIcon("./resources/摄像头_关闭.png"))
        self.put_img.close()  # 关闭摄像头
        self.ui.qlabel4.setPixmap(QPixmap("./resources/摄像头.png"))

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
        while self.Q1.qsize() != 0:  # 清空队列
            pass
        while self.Q2.qsize() != 0:
            self.Q2.get()
        self.ui.qlabel1.clear()#清除提示信息
        if self.flag == True:
            psutil.Process(self.p.pid).suspend()  # 挂起进程
            self.flag = False#子进程状态标志，False表示子进程已经暂停
        self.ui.qlabel4.clear()
        self.ui.qlabel4.hide()#用于修复无法清理（qlable.claer()）图片
        self.ui.qlabel5.show()

    def closeEvent(self, Event):
        if hasattr(self, "put_img"):
            self.put_img.close()
        super().closeEvent(Event)

        # p = psutil.Process(os.getpid())
        # print(p.children())
        # for i in p.children():
        #     i.kill()
        # p.kill()