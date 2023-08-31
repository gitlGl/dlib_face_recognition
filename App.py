from PySide6.QtWidgets import QApplication
from src import Main
import sys
from qss import StyleSheet
from PySide6.QtGui import QFont
from PySide6 import QtCore
from src import database
import lancedb
from src import getVector
# face_data = getVector('C:/Users/Administrator/Pictures/Camera Roll/8.jpg')
# print(face_data)
# result = database.vector_tbl.search(face_data).limit(1)

# print(result)

if __name__ == '__main__':
    # QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    translator = QtCore.QTranslator()
    translator.load("resources/widgets_zh_CN_all.qm")#加载中文文件
    app.installTranslator(translator)
    f = QFont("宋体",10)
    app.setFont(f)
    app.setStyleSheet(StyleSheet)   
    ui = Main()
    app.exec()



