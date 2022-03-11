from PyQt5.QtWidgets import QApplication
from src import Ui
import sys
from test import StyleSheet

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    ui = Ui()
    app.exec_()
