from PyQt5.QtWidgets import QWidget, QLabel,QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import pyqtSignal,Qt,pyqtSlot,QTimer, Qt
from src.Capture import Capture
from PyQt5.QtGui import QImage,QPixmap,QIcon
from .Face import AdminRgFace
import cv2,copy
from .GlobalVariable import GlobalFlag,models
from PyQt5.QtWidgets import QGroupBox
from .LivenessDetection import LivenessDetection

class FaceLoginPage(QWidget):
    emit_show_parent = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("人脸识别登录")
        self.setWindowIcon(QIcon("resources/人脸识别.png"))

        self.Hlayout = QHBoxLayout()
        self.Vlayout = QVBoxLayout(self)
        self.groupbox = QGroupBox(self)
        self.groupbox.setLayout(self.Hlayout)
        self.label1 = QLabel()
        self.label1.setAlignment(Qt.AlignHCenter)
        self.label2 = QLabel(self)
        self.Hlayout.addWidget(self.label1)
        self.Vlayout.addWidget(self.groupbox)
        self.Vlayout.addWidget(self.label2)
        self.setLayout(self.Vlayout)
        self.groupbox.setFixedSize(480, 35)
        self.groupbox.hide()
        self.resize(480, 600)
        self.setWindowModality(Qt.ApplicationModal)#
        self.face_rg = AdminRgFace()
        self.capture = Capture()
        self.capture.SetCap()
        self.capture.work.emit_img.connect(self.setNormalImg)
        self.capture.work_thread.start()
        self.timer1 = QTimer()
        self.timer2 =QTimer()
        self.timer2.timeout.connect(self.collectFrame)
        self.timer1.timeout.connect(self.getResult)
        self.timer1.start(500)
        self.cout = 0
        self.list_img = []
        self.show()

    def getResult(self):
        self.timer1.stop()
        rgbImage = cv2.cvtColor(self.capture.frame, cv2.COLOR_BGR2RGB)
        location_faces = models.detector(rgbImage)
        if len(location_faces) == 1:
            raw_face = models.predictor(rgbImage, location_faces[0])
            result = self.face_rg.rgFace(self.capture.frame, rgbImage,
                                          raw_face)
            if result:
                self.capture.close()
                self.emit_show_parent.emit(result)
                self.close
                return
        
            self.groupbox.show()
            if self.cout> 2:
                self.timer2.start(200)
                self.livecheck  = LivenessDetection()
                self.label1.setText("提示：请张嘴")
                return
            self.cout = self.cout +1
            self.label1.setText("验证失败{0}".format(self.cout))
        self.timer1.start(500)
        
    def collectFrame(self):
        self.timer2.stop()
        if not GlobalFlag.gflag2:
            img = copy.deepcopy(self.capture.frame)
            flag = self.livecheck.computMouth(img)
            if flag:
                GlobalFlag.gflag2 = True
                self.label1.setText("提示：请看镜头眨眼睛")
        else:
            if len(self.list_img) <= 1:
                self.list_img.append(self.capture.frame)
            elif len(self.list_img) == 2:
                
                list_img = copy.deepcopy(self.list_img)
                flag = self.livecheck.compare2faces(list_img)
                if flag: 
                    GlobalFlag.gflag2 = False
                    rgbImage = cv2.cvtColor(self.capture.frame, cv2.COLOR_BGR2RGB)
                    
                    location_faces = models.detector(rgbImage)
                    if len(location_faces) == 1:
                        raw_face = models.predictor(rgbImage, location_faces[0])
                        result = self.face_rg.rgFace(self.capture.frame, rgbImage,
                                            raw_face)
                                     
                        if result:                      
                            self.capture.close()
                            self.emit_show_parent.emit(result)
                            self.close
                            return
                    else:
                        self.label1.setText("提示：请张嘴")
                self.list_img.clear()

        self.timer2.start(200)

    def closeEvent(self, event):
        if self.timer1.isActive():
            self.timer1.stop()
        if self.timer2.isActive():
            self.timer2.stop()    
        self.capture.close()
        super().closeEvent(event)

    #@pyqtSlot(list,QImage)
    def setNormalImg(self, list):
        self.label2.setPixmap(QPixmap.fromImage(list[0]))#设置图片
        self.capture.frame = list[1]#待识别帧
        #QPixmap.fromImage(img).scaled(self.label2.size(), Qt.KeepAspectRatio))#图片跟随qlabel大小缩放
        self.label2.setScaledContents(True)#qlabel2自适应图片大小



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
