from PySide6.QtWidgets import QWidget, QLabel,QVBoxLayout,QHBoxLayout, QGroupBox
from PySide6.QtCore import Signal,Qt,QTimer, Qt
from .Capture import Capture
from PySide6.QtGui import QPixmap,QIcon
from .Face import AdminRgFace
import cv2,copy
from .Setting import predictor,detector,isVerifyeRemote
from . import LivenessDetection
from .Setting import resources_dir
from PySide6.QtCore import QUrl, Slot
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import pickle
import uuid
from .logger import logger
if isVerifyeRemote:
    from .Setting import ip,port
class FaceLoginPage(QWidget):
    emit_show_parent = Signal(str)

    def __init__(self,id_number) -> None:
        super().__init__()
        self.manager = QNetworkAccessManager()

        url = f"http://{ip}:{port}"  # 请求的URL
        self.request = QNetworkRequest(QUrl(url))
        self.request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")

        # 发送POST请求
        data = pickle.dumps({'flag':'login',"mac_address":uuid.uuid1().hex[-12:],"id_number":id_number})
        self.reply = self.manager.post(self.request, data)

        self.reply.finished.connect(lambda: self.handle_response(self.reply))
       
       
    
        self.setWindowTitle("人脸识别登录")
        self.setWindowIcon(QIcon(resources_dir + "人脸识别.svg"))

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
       
        self.count = 0
        self.list_img = []
        self.flag = False
        self.show()
    def handle_response(self,reply): 
        if reply.error().value:
            self.emit_show_parent.emit(False)#接收到的是空字符串
            return
           
        data = reply.readAll()
        flag = pickle.loads(data) 
        print("Response:",flag)
        if not flag:
            logger.error(reply.error())
            self.emit_show_parent.emit(False)
            self.close()
            return
        self.get_result_timer.start(500)
      
        
        #reply.deleteLater()

   
       
        
    def getResult(self):

        self.get_result_timer.stop()
        rgbImage = cv2.cvtColor(self.capture.frame, cv2.COLOR_BGR2RGB)
        location_faces = detector(rgbImage)
        if len(location_faces) == 1:
            raw_face = predictor(rgbImage, location_faces[0])
            result = self.face_rg.rgFace(self.capture.frame, rgbImage,
                                          raw_face)
            if result:
                self.capture.close()
                self.emit_show_parent.emit(result)
                self.close()
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
            
            location_faces = detector(rgbImage)
            if len(location_faces) == 1:
                raw_face = predictor(rgbImage, location_faces[0])
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



