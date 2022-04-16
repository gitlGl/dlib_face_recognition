import os,PIL
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
    rgbImage = PIL.Image.open(path)
    rgbImage  =  rgbImage .convert("RGB")
    rgbImage =  np.array(rgbImage )
    faces = models.detector(rgbImage)
    if len(faces) == 1:
        return path
    else:
        QMessageBox.critical(parent, 'Wrong', '文件不存在人脸或多个人脸')
        return False
