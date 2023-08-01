from PySide6.QtWidgets import QWidget, QLabel,QVBoxLayout,QHBoxLayout
from PySide6.QtCore import Signal,Qt,QTimer, Qt
from .Capture import Capture
from PySide6.QtGui import QPixmap,QIcon
from .Face import AdminRgFace
import cv2,copy
from .Setting import models
from PySide6.QtWidgets import QGroupBox
from .LivenessDetection import LivenessDetection
class FaceLoginPage(QWidget):
    emit_show_parent = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("人脸识别登录")
        self.setWindowIcon(QIcon("resources/人脸识别.svg"))

        self.Hlayout = QHBoxLayout()
        self.Vlayout = QVBoxLayout(self)
        self.groupbox = QGroupBox(self)
        self.groupbox.setLayout(self.Hlayout)
        self.tips_label = QLabel()
        self.tips_label.setAlignment(Qt.AlignHCenter)
        self.picture_label = QLabel(self)
        self.Hlayout.addWidget(self.tips_label)
        self.Vlayout.addWidget(self.groupbox)
        self.Vlayout.addWidget(self.picture_label)
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
        self.get_result_timer = QTimer()
        self.get_frame_timer =QTimer()
        self.get_frame_timer.timeout.connect(self.collectFrame)
        self.get_result_timer.timeout.connect(self.getResult)
        self.get_result_timer.start(500)
        self.count = 0
        self.list_img = []
        self.flag = False
        self.show()

    def getResult(self):
        self.get_result_timer.stop()
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
            if self.count> 2:
                self.get_frame_timer.start(200)
                self.tips_label.setText("提示：请张嘴")
                return
            self.count = self.count +1
            self.tips_label.setText("验证失败{0}".format(self.count))
        self.get_result_timer.start(500)
        
    def collectFrame(self):
        self.get_frame_timer.stop()
        if not self.flag:
            img = copy.deepcopy(self.capture.frame)
            flag =  LivenessDetection.computMouth(img)
            if flag:
                self.flag = True
                self.tips_label.setText("提示：请看镜头眨眼睛")
            self.get_frame_timer.start(200)
            return
        if len(self.list_img) < 2:
            self.list_img.append(self.capture.frame)
            self.get_frame_timer.start(200)
            return
    
        list_img = copy.deepcopy(self.list_img)
        flag = LivenessDetection.compare2faces(list_img)
        if flag: 
            self.flag = False
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
                
            self.tips_label.setText("验证失败，提示：请张嘴")
        self.list_img.clear()
        self.get_frame_timer.start(200)

    def closeEvent(self, event):
        if self.get_result_timer.isActive():
            self.get_result_timer.stop()
        if self.get_frame_timer.isActive():
            self.get_frame_timer.stop()    
        self.capture.close()
        super().closeEvent(event)

    #@Slot(list,QImage)
    def setNormalImg(self, list):
        self.picture_label.setPixmap(QPixmap.fromImage(list[0]))#设置图片
        self.capture.frame = list[1]#待识别帧
        #QPixmap.fromImage(img).scaled(self.label2.size(), Qt.KeepAspectRatio))#图片跟随qlabel大小缩放
        self.picture_label.setScaledContents(True)#qlabel2自适应图片大小



# class FaceLoginPage(QWidget):
#     emit_show_parent = Signal()
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

#     @Slot(QImage)
#     def set_normal_img(self, image):
#         self.label.setPixmap(QPixmap.fromImage(image))
#         self.label.setScaledContents(True)
