import cv2
from PySide6.QtCore import QThread,Signal,QObject
import numpy as np
from PySide6.QtGui import QImage
from .GlobalVariable import models
#from PIL import Image, ImageDraw, ImageFont
from .conver import convertToQtFormat
class Work(QObject):
  
    emit_img = Signal(list)
    def __init__(self):
        super().__init__()
        self.Priority = QThread.HighestPriority
        self.cap = None
        self.flag = 1
    
    def do(self): 
        while self.flag:
            ret, frame = self.cap.read()
            frame2 = frame
            if ret:
                p = convertToQtFormat(frame)
                self.emit_img.emit([p,frame2])
    

class Capture(QObject):
    def __init__(self):
        super().__init__()
        #self.Priority = QThread.HighestPriority
        self.frame = np.random.randint(255, size=(900, 800, 3),#颜色为0-255的随机数，size为图片大小，3为RGB， dtype=np.uint8数据类型，8个bit
                                       dtype=np.uint8)  #待识别帧初始化
        self.work = Work()
        self.work_thread =  QThread()
        self.work.moveToThread(self.work_thread)
        self.work_thread.started.connect(self.work.do)

    def SetCap(self):
        #print("主线程",QThread.currentThreadId())
        self.work.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    

    def close(self): #关闭线程
        if self.work_thread.isRunning():
            # self.work_thread.terminate()
            # self.work_thread.wait()
            self.work.flag = 0
            self.work_thread.exit(0)
            self.work_thread.wait()
            self.work.flag = 1
        if self.work.cap is not None:
            self.work.cap.release()
            cv2.destroyAllWindows()

#转换位qt图像格式
# def convertToQtFormat(frame_show):
#     #print("子线程",QThread.currentThreadId())
#     rgbImage = cv2.cvtColor(frame_show, cv2.COLOR_BGR2RGB)
#     faces = models.detector(rgbImage)
#     if len(faces) == 1:
#         face = faces[0]
#         cv2.rectangle(rgbImage, (face.left(), face.top()), (face.right(), face.bottom()), (255,0,0), 4)

#     h, w, ch = rgbImage.shape
#     bytesPerLine = ch * w
#     convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine,
#                                QImage.Format.Format_RGB888)
#     p = convertToQtFormat.scaled(460, 530)
#     return p

#为图片渲染中文
# def put_chines_test(frame, chinnes_text):
#     rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     location = models.detector(rgbImage)
#     if len(location) == 1:
#         location = location[0]
#         font = ImageFont.truetype("./resources/simsun.ttc",
#                                   50,
#                                   encoding="utf-8")
#         rgbImage = Image.fromarray(rgbImage)
#         draw = ImageDraw.Draw(rgbImage)
#         draw.text(((location.right() + 6, location.top() - 6)), chinnes_text,
#                   (0, 0, 255), font)
#         rgbImage = np.asarray(rgbImage)
#     return rgbImage