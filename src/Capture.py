import cv2
from PyQt5.QtCore import QThread
import numpy as np
from PyQt5.QtGui import QImage
from src.Process import *
from PyQt5.QtCore import pyqtSignal
#from PIL import Image, ImageDraw, ImageFont
class Capture(QThread):
  
    emit_img = pyqtSignal(list,QImage)
    def __init__(self):
        super().__init__()
        self.frame = np.random.randint(255, size=(900, 800, 3),
                                       dtype=np.uint8)  #初始化
        self.cap = None
    def run(self): 
        while True:
            ret, frame = self.cap.read()
            if ret:
                
                p = convertToQtFormat(frame)
                self.emit_img.emit([frame],p)
    

    def close(self): #关闭线程
        if self.isRunning():
            self.terminate()
            self.wait()
        if self.cap is not None:
            self.cap.release()
            cv2.destroyAllWindows()

#转换位qt图像格式
def convertToQtFormat(frame_show):
    rgbImage = cv2.cvtColor(frame_show, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(rgbImage,cv2.COLOR_RGB2GRAY)
    faces = models.detector(gray)
    if len(faces) == 1:
        face = faces[0]
        cv2.rectangle(rgbImage, (face.left(), face.top()), (face.right(), face.bottom()), (255,0,0), 4)

    h, w, ch = rgbImage.shape
    bytesPerLine = ch * w
    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine,
                               QImage.Format.Format_RGB888)
    p = convertToQtFormat.scaled(480, 530)
    return p


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