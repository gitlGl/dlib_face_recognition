import sys
sys.path.append(r'./')

from  Crypto.PublicKey import RSA
from PyQt5.QtWidgets import QApplication
from src import Main
import sys
from qss import StyleSheet
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
#import qdarkstyle
if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    f = QFont("宋体",10)
    app.setFont(f)
    app.setStyleSheet(StyleSheet)   
    ui = Main()
    app.exec_()

