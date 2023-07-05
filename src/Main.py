import gc,multiprocessing,psutil
from PyQt5.QtWidgets import QMessageBox,QMenu
from .Process import processStudentRg
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QIcon,QPixmap
from .Help import Help
from .AdminInformation  import AdminInformation
from multiprocessing import Process, Queue
from .PutImg import PutImg
from .Login import LoginUi
from .ShowData import ShowData
from .Login import LoginUi
from  .Ui import Ui
from .GlobalVariable import database
import datetime
from .Database import PH
class Main(Ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Q_put = Queue()  # put_img
        self.Q_get = Queue()
        self.process_exit = 100
        self.share = multiprocessing.Value("f", 0.4)
        self.put_img = PutImg(self.Q_put, self.Q_get)
        self.put_img.emit_result.connect(self.showResult)
        self.put_img.emit_text.connect(self.changeText)
        self.timer_clearQlabel = QTimer()
        self.timer_clearQlabel.timeout.connect(self.clearQlabel)#清除识别结果
        self.login_ui = LoginUi()
        if self.aotuLogin():#检查是否自动登录
            return
        self.login_ui.emitsingal.connect(self.showParent)
        self.login_ui.show()
    #退出登录
    def posMenu(self,pos):
        if(self.showError()):
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
                #if  self.flag == False:
                psutil.Process(self.p.pid).resume()
                self.share.value = self.process_exit
            self.normal_rgface_btn.setChecked(False)
            self.Liveness_rgface_btn.setChecked(False)
            self.normal_rgface_btn.setEnabled(True)
            self.Liveness_rgface_btn.setEnabled(True)
        
                #self.p.terminate()
            self.hide()
            self.login_ui = LoginUi()
            self.login_ui.emitsingal.connect(self.showParent)
            self.login_ui.show()
            self.login_ui.config_auto_login.setStates('')
            self.login_ui.config_auto_login.setFlag('0')
        
    def showError(self):
        if(self.put_img.work_thread.isRunning()):
             QMessageBox.critical(self, '警告', '请先关闭摄像头')
             return True
             
    def showData(self):
        if(self.showError()):
             return
        self.view =ShowData()
        self.view.show()
        pass

 
    def aotuLogin(self):
        if not self.login_ui.config_auto_login.check():
            return False
        self.id_number = self.login_ui.config_auto_login.result['id_number']
        self.p = Process(target=processStudentRg,
                        args=(self.Q_put, self.Q_get, self.share))
        self.p.daemon = True
        self.show()
        del self.login_ui
        database.c.execute(f"INSERT INTO admin_log_time (id_number,log_time ) \
VALUES ({PH},{PH})", (self.id_number, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))
        database.conn.commit()
        return True
        
    
    #登录成功后显示主界面
   # @pyqtSlot(str)
    def showParent(self,id_number):
        self.id_number = id_number
        distance = round(self.slider.value() * 0.05, 2)
        self.share.value = distance
        del self.login_ui
        gc.collect()
        self.p = Process(target=processStudentRg,
                         args=(self.Q_put, self.Q_get, self.share))
        self.p.daemon = True
        self.show()
     
       

    #显示识别结果
    @pyqtSlot(str)
    def showResult(self, str_result):
        self.rg_label.clear()
        self.rg_label.setText(str_result)
        self.tips_label.clear()#清除提示
        if not self.timer_clearQlabel.isActive():#开启清除识别结果
            self.timer_clearQlabel.start(1500)

    #清除识别结果
    def clearQlabel(self):
        self.timer_clearQlabel.stop()
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
    def changeText(self, str):
        self.tips_label.clear()
        self.tips_label.setText(str)

    #帧显示视频流
    #@pyqtSlot(list,QImage)
    def setNormalImg(self, list):   
        self.picture_qlabel.setPixmap(QPixmap.fromImage(list[0])) #设置图片，图片跟随ui.qlabel大小缩放
        self.put_img.frame = list[1]#待识别帧
        
        
        #QPixmap.fromImage(img).scaled(self.qlabel4.size(),Qt.KeepAspectRatio)图片跟随ui.qlabel大小缩放
        self.picture_qlabel.setScaledContents(True)#ui.qlabel4自适应图片大小

    #帮助页面
    def help(self):
        if(self.showError()):
             return
        self.help_qlabe = Help()
        self.help_qlabe.exec_()

    #正常识别
    def openNormal(self):
        if self.normal_rgface_btn.isChecked():  # 两个按钮互斥判断另一个按钮
            self.Liveness_rgface_btn.setChecked(False)
            self.normal_rgface_btn.setEnabled(False)
            self.Liveness_rgface_btn.setEnabled(True)

            while self.put_img.timer_collectFrame.isActive():
                self.put_img.timer_collectFrame.stop()
            while self.put_img.timer_getResult.isActive():
                self.put_img.timer_getResult.stop()
            while self.put_img.timer_collectFrame.isActive():
                self.put_img.timer_collectFrame.stop()
            while self.Q_put.qsize() != 0:  # 清空队列
                pass
            while self.Q_get.qsize() != 0:
                self.Q_get.get()
            self.tips_label.clear()
            if self.put_img.work_thread.isRunning():
                if not self.put_img.timer_toPut.isActive():
                    self.put_img.timer_toPut.start(1000)

    #活体识别
    def openEye(self):

        if self.Liveness_rgface_btn.isChecked():
            self.normal_rgface_btn.setChecked(False)
            self.Liveness_rgface_btn.setEnabled(False)
            self.normal_rgface_btn.setEnabled(True)
            self.put_img.flag = False
            if self.put_img.work_thread.isRunning():
                if self.put_img.timer_toPut.isActive():
                    self.put_img.timer_toPut.stop()
                    while self.Q_put.qsize() != 0:  # 清空队列
                        pass
                    while self.Q_get.qsize() != 0:
                        self.Q_get.get()
            if self.put_img.work_thread.isRunning():
                if not self.put_img.timer_collectFrame.isActive():
                    self.put_img.timer_collectFrame.start(200)
                    self.tips_label.setText("提示：请张嘴")
                  

    def open(self):
        self.picture_qlabel.show()
        self.qlabel5.hide()##用于修复无法清理（qlable.claer()）图片
        self.put_img.work.emit_img.connect(self.setNormalImg)
        self.open_capture_btn.clicked.disconnect(self.open)
        self.open_capture_btn.clicked.connect(self.close)
        self.open_capture_btn.setText("关闭摄像头")
        self.open_capture_btn.setIcon(QIcon("resources/摄像头.svg"))
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
            if not self.put_img.timer_toPut.isActive():
                self.put_img.timer_toPut.start(1000)
            return

        if self.Liveness_rgface_btn.isChecked():
            if not self.put_img.timer_collectFrame.isActive():
                self.put_img.timer_collectFrame.start(200)
                self.tips_label.setText("提示：请张嘴")
            return
               

    def close(self):
        self.put_img.work.emit_img.disconnect(self.setNormalImg)
       
        self.put_img.flag = False

        self.open_capture_btn.clicked.connect(self.open)
        self.open_capture_btn.clicked.disconnect(self.close)
        self.open_capture_btn.setText("打开摄像头")
        self.open_capture_btn.setIcon(QIcon("resources/摄像头_关闭.svg"))
        self.put_img.close()  # 关闭摄像头
        #self.qlabel4.setPixmap(QPixmap("./resources/摄像头.svg"))

        while self.put_img.timer_toPut.isActive():
            self.put_img.timer_toPut.stop()

        while self.put_img.timer_collectFrame.isActive():
            self.put_img.timer_collectFrame.stop()
        while self.put_img.timer_getResult.isActive():
            self.put_img.timer_getResult.stop()
        while self.put_img.timer_collectFrame.isActive():
            self.put_img.timer_collectFrame.stop()

        while self.put_img.timer_toPut.isActive():
            self.put_img.timer_toPut.stop()
        while self.Q_put.qsize() != 0:  # 清空队列
            pass
        while self.Q_get.qsize() != 0:
            self.Q_get.get()
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
