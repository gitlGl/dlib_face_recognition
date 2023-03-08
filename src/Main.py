import gc,multiprocessing,psutil
from PyQt5.QtWidgets import QWidget, QMessageBox,QMenu
from src.Process import processStudentRg
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QIcon,QPixmap
from src.Help import Help
from src.AdminInformation  import AdminInformation
from multiprocessing import Process, Queue
from .PutImg import PutImg
from src.Login import LoginUi
from src.ShowData import ShowData
from .Login import LoginUi,configAotuLogin,aes
from  .Ui import Ui
from src.GlobalVariable import database

class Main(QWidget,Ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Q1 = Queue()  # put_img
        self.Q2 = Queue()
        self.share = multiprocessing.Value("f", 0.4)
        self.put_img = PutImg(self.Q1, self.Q2)
        self.put_img.emit_result.connect(self.show_result)
        self.put_img.emit_text.connect(self.change_text)
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_qlabel2)#清除识别结果
        self.login_ui = LoginUi()
        if self.login_ui.config_auto_login.check():
            id_ = self.login_ui.config_auto_login.result[-36:]
            id_ = id_[:-16]
            id_ = id_.strip(' ')
            self.id_number = id_
            self.p = Process(target=processStudentRg,
                            args=(self.Q1, self.Q2, self.share))
            self.p.daemon = True
            self.show()
            del self.login_ui
            return
        self.login_ui.emitsingal.connect(self.show_parent)
        self.login_ui.show()
    #退出登录
    def pos_menu(self,pos):
        if(self.show_error()):
             return
        pop_menu = QMenu(self)
        pop_menu.addAction("用户信息")
        pop_menu.addAction("退出登录")
        action = pop_menu.exec_(self.mapToGlobal(pos))
        if action == pop_menu.actions()[0]:
            self.admin_information = AdminInformation(self.id_number)
            self.admin_information.show()
            return
        if action == pop_menu.actions()[1]:
            if self.put_img.work.cap is not None:#判断摄像头状态
                if self.put_img.work_thread.isRunning():
                    QMessageBox.information(self, 'Information', '请先关闭摄像头')
                    return  
            if self.p.is_alive():
                self.p.terminate()
            self.hide()
            self.login_ui = LoginUi()
            self.login_ui.emitsingal.connect(self.show_parent)
            self.login_ui.show()
            self.login_ui.config_auto_login.setId('')
            self.login_ui.config_auto_login.setStates('')
            self.login_ui.config_auto_login.setFlag('0')
        
    def show_error(self):
        if(self.put_img.work_thread.isRunning()):
             QMessageBox.critical(self, 'Wrong', '请先关闭摄像头')
             return True
             
    def show_data(self):
        if(self.show_error()):
             return
        self.view =ShowData()
        self.view.show()
        pass

 
        
    
    #登录成功后显示主界面
   # @pyqtSlot(str)
    def show_parent(self,id_number):
        self.id_number = id_number
        del self.login_ui
        gc.collect()
        self.p = Process(target=processStudentRg,
                         args=(self.Q1, self.Q2, self.share))
        self.p.daemon = True
        self.show()
     
       

    #显示识别结果
    @pyqtSlot(str)
    def show_result(self, str_result):
        self.rg_label.clear()
        self.rg_label.setText(str_result)
        self.tips_label.clear()#清除提示
        if not self.timer.isActive():#开启清除识别结果
            self.timer.start(1500)

    #清除识别结果
    def clear_qlabel2(self):
        self.timer.stop()
        self.rg_label.clear()
        if self.Liveness_rgface_btn.isChecked() and self.put_img.work_thread.isRunning(): #and self.put_img.isRunning()
            self.tips_label.setText("提示：请张嘴")


    #刻度值槽函数
    def valueChange(self):
        distance = round(self.slider.value() * 0.05, 2)
        self.share.value = distance
        self.scale_value_label.setText(str(distance))

    #清理活体识别提示信息，设置提示信息
    @pyqtSlot(str)
    def change_text(self, str):
        self.tips_label.clear()
        self.tips_label.setText(str)

    #帧显示视频流
    #@pyqtSlot(list,QImage)
    def set_normal_img(self, list):   
        self.picture_qlabel.setPixmap(QPixmap.fromImage(list[0])) #设置图片，图片跟随ui.qlabel大小缩放
        self.put_img.frame = list[1]#待识别帧
        
        
        #QPixmap.fromImage(img).scaled(self.qlabel4.size(),Qt.KeepAspectRatio)图片跟随ui.qlabel大小缩放
        self.picture_qlabel.setScaledContents(True)#ui.qlabel4自适应图片大小

    #帮助页面
    def help(self):
        if(self.show_error()):
             return
        self.help_qlabe = Help()
        self.help_qlabe.exec_()

    #正常识别
    def open_normal(self):
        if self.normal_rgface_btn.isChecked():  # 两个按钮互斥判断另一个按钮
            self.Liveness_rgface_btn.setChecked(False)
            self.normal_rgface_btn.setEnabled(False)
            self.Liveness_rgface_btn.setEnabled(True)

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
            self.tips_label.clear()
            if self.put_img.work_thread.isRunning():
                if not self.put_img.timer3.isActive():
                    self.put_img.timer3.start(1000)

    #活体识别
    def open_eye(self):

        if self.Liveness_rgface_btn.isChecked():
            self.normal_rgface_btn.setChecked(False)
            self.Liveness_rgface_btn.setEnabled(False)
            self.normal_rgface_btn.setEnabled(True)
            self.put_img.flag = False
            if self.put_img.work_thread.isRunning():
                if self.put_img.timer3.isActive():
                    self.put_img.timer3.stop()
                    while self.Q1.qsize() != 0:  # 清空队列
                        pass
                    while self.Q2.qsize() != 0:
                        self.Q2.get()
            if self.put_img.work_thread.isRunning():
                if not self.put_img.timer1.isActive():
                    self.put_img.timer1.start(200)
                    self.tips_label.setText("提示：请张嘴")
                  

    def open(self):
        self.picture_qlabel.show()
        self.qlabel5.hide()##用于修复无法清理（qlable.claer()）图片
        self.put_img.work.emit_img.connect(self.set_normal_img)
        self.open_capture_btn.clicked.disconnect(self.open)
        self.open_capture_btn.clicked.connect(self.close)
        self.open_capture_btn.setText("关闭摄像头")
        self.open_capture_btn.setIcon(QIcon("resources/摄像头.png"))
        self.put_img.SetCap()
        self.put_img.work_thread.start()
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

        if self.normal_rgface_btn.isChecked():
            if not self.put_img.timer3.isActive():
                self.put_img.timer3.start(1000)
            return

        if self.Liveness_rgface_btn.isChecked():
            if not self.put_img.timer1.isActive():
                self.put_img.timer1.start(200)
                self.tips_label.setText("提示：请张嘴")
            return
               

    def close(self):
        self.put_img.work.emit_img.disconnect(self.set_normal_img)
       
        self.put_img.flag = False

        self.open_capture_btn.clicked.connect(self.open)
        self.open_capture_btn.clicked.disconnect(self.close)
        self.open_capture_btn.setText("打开摄像头")
        self.open_capture_btn.setIcon(QIcon("resources/摄像头_关闭.png"))
        self.put_img.close()  # 关闭摄像头
        #self.qlabel4.setPixmap(QPixmap("./resources/摄像头.png"))

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
        self.tips_label.clear()#清除提示信息
        if self.flag == True:
            psutil.Process(self.p.pid).suspend()  # 挂起进程
            self.flag = False#子进程状态标志，False表示子进程已经暂停
        self.picture_qlabel.clear()
        self.picture_qlabel.hide()#用于修复无法清理（qlable.claer()）图片
        self.qlabel5.show()

    def closeEvent(self, Event):
        if hasattr(self, "put_img"):
            self.put_img.close()
        super().closeEvent(Event)
        database.c.close()

        # p = psutil.Process(os.getpid())
        # print(p.children())
        # for i in p.children():
        #     i.kill()
        # p.kill()
