import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from .GlobalVariable import models
from .Creatuser import CreatUser


def get_img_path(parent=None):
    path, _ = QFileDialog.getOpenFileName(parent, "选择文件", "c:\\",
                                          "Image files(*.jpg *.gif *.png)")
    if path == '':
        return False

    if os.path.getsize(path) > 1024000:
        QMessageBox.critical(parent, 'Wrong', '文件应小于10mb')
        return False

    data = open(path, "rb").read(32)
    if not (data[6:10] in (b'JFIF', b'Exif')):  #检查文件类型是否属于jpg文件
        QMessageBox.critical(parent, 'Wrong', '文件非图片文件')
        return False

    rgbImage = CreatUser().get_img(path)

    faces = models.detector(rgbImage)
    if len(faces) != 1:
        QMessageBox.critical(parent, 'Wrong', '文件不存在人脸或多个人脸')
        return False
    return path
