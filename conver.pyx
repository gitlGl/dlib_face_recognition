import cv2
from PySide6.QtGui import QImage
from src.Setting import models
#转换位qt图像格式
def convertToQtFormat(frame_show):
    #print("子线程",QThread.currentThreadId())
    rgbImage = cv2.cvtColor(frame_show, cv2.COLOR_BGR2RGB)
    faces = models.detector(rgbImage)
    if len(faces) == 1:
        face = faces[0]
        cv2.rectangle(rgbImage, (face.left(), face.top()), (face.right(), face.bottom()), (255,0,0), 4)
    cdef int h, w, ch,bytesPerLine
    h, w, ch = rgbImage.shape
    bytesPerLine = ch * w
    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine,
                               QImage.Format.Format_RGB888)
    p = convertToQtFormat.scaled(460, 530)
    return p