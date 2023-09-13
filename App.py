from PySide6.QtWidgets import QApplication
from src import Main
import sys
from qss import StyleSheet
from PySide6.QtGui import QFont
from PySide6 import QtCore
from src import resources_dir
#方便启动远程验证时进行测试
import os
from src import isVerifyeRemote


if __name__ == '__main__':
    # QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    if isVerifyeRemote:
        os.system('start python Server.py')  
    app = QApplication(sys.argv)
    translator = QtCore.QTranslator()
    translator.load(resources_dir + "widgets_zh_CN_all.qm")#加载中文文件
    app.installTranslator(translator)
    f = QFont("宋体",10)
    app.setFont(f)
    app.setStyleSheet(StyleSheet)   
    ui = Main()
    app.exec()



