from PyQt5.QtWidgets import QWidget, QLabel,QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import pyqtSignal,Qt
from src.Capture import Capture
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
from PyQt5.QtGui import QImage,QPixmap
from .Face import AdminRgFace
import cv2,copy
from .GlobalVariable import GlobalFlag,models
from PyQt5.QtWidgets import QGroupBox
from .LivenessDetection import LivenessDetection

class FaceLoginPage(QWidget):
    emit_show_parent = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
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
        self.setWindowModality(Qt.ApplicationModal)
        self.face_rg = AdminRgFace()
        self.capture = Capture()
        self.capture.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.capture.emit_img.connect(self.set_normal_img)
        self.capture.start()
        self.timer1 = QTimer()
        self.timer2 =QTimer()
        self.timer2.timeout.connect(self.collect_frame)
        self.timer1.timeout.connect(self.get_result)
        self.timer1.start(500)
        self.cout = 0
        self.list_img = []
        self.show()

    def get_result(self):
        self.timer1.stop()
        rgbImage = cv2.cvtColor(self.capture.frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(rgbImage, cv2.COLOR_RGB2GRAY)
        location_faces = models.detector(gray)
        if len(location_faces) == 1:
            raw_face = models.predictor(gray, location_faces[0])
            result = self.face_rg.rg_face(self.capture.frame, rgbImage,
                                          raw_face)
            if result:
                self.capture.close()
                self.emit_show_parent.emit()
                self.close
            else:
                self.groupbox.show()
                if self.cout> 2:
                    self.timer2.start(200)
                    self.livecheck  = LivenessDetection()
                    self.label1.setText("提示：请张嘴")
                    return
                self.cout = self.cout +1
                self.label1.setText("验证失败{0}".format(self.cout))
        self.timer1.start(500)
        
    def collect_frame(self):
        self.timer2.stop()
        if not GlobalFlag.gflag2:
            img = copy.deepcopy(self.capture.frame)
            flag = self.livecheck.comput_mouth(img)
            if flag:
                GlobalFlag.gflag2 = True
                self.label1.setText("提示：请看镜头眨眼睛")
        else:
            if len(self.list_img) <= 1:
                self.list_img.append(self.capture.frame)
            elif len(self.list_img) == 2:
                
                list_img = copy.deepcopy(self.list_img)
                flag = self.livecheck.compare2faces(list_img)
                print(flag)
                if flag:
                    print('检测到眨眼')  
                    GlobalFlag.gflag2 = False
                    rgbImage = cv2.cvtColor(self.capture.frame, cv2.COLOR_BGR2RGB)
                    gray = cv2.cvtColor(rgbImage, cv2.COLOR_RGB2GRAY)
                    location_faces = models.detector(gray)
                    if len(location_faces) == 1:
                        raw_face = models.predictor(gray, location_faces[0])
                        result = self.face_rg.rg_face(self.capture.frame, rgbImage,
                                            raw_face)
                                     
                    if result:                      
                        self.capture.close()
                        self.emit_show_parent.emit()
                        self.close
                        return
                    else:
                        self.label1.setText("提示：请张嘴")
                self.list_img.clear()

        self.timer2.start(200)

    def closeEvent(self, event):
        if self.timer1.isActive():
            print("tingzhi")
            self.timer1.stop()
        if self.timer2.isActive():
            print("tingzhi")
            self.timer2.stop()    
        self.capture.close()
        super().closeEvent(event)

    @pyqtSlot(list,QImage)
    def set_normal_img(self, list_,img):
        self.capture.frame = list_[0]
        self.label2.setPixmap(QPixmap.fromImage(img))
        self.label2.setScaledContents(True)



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
