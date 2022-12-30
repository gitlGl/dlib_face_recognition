import os,cv2
import numpy as np
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from .GlobalVariable import models
def get_img_path(parent=None):
    path, _ = QFileDialog.getOpenFileName(
        parent, "选择文件", "c:\\", "Image files(*.jpg *.gif *.png)")
    if path == '':
        return False
    elif os.path.getsize(path) > 1024000 :
        QMessageBox.critical(parent, 'Wrong', '文件应小于10mb')
        return False
    data = open(path,"rb").read(32)
    if not (data[6:10] in (b'JFIF',b'Exif')):#检查文件类型是否属于jpg文件
       
        QMessageBox.critical(parent, 'Wrong', '文件非图片文件')
        return False
    raw_data = np.fromfile(path, dtype=np.uint8)  #先用numpy把图片文件存入内存：raw_data，把图片数据看做是纯字节数据
    rgbImage = cv2.imdecode(raw_data, cv2.IMREAD_COLOR)  #从内存数据读入图片
    rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
    
    faces = models.detector(rgbImage)
    if len(faces) == 1:
        return path
    else:
        QMessageBox.critical(parent, 'Wrong', '文件不存在人脸或多个人脸')
        return False
