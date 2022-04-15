from PyQt5.QtWidgets import  QDialog,QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
class Help(QDialog):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle("帮助")
        self.setWindowIcon(QIcon("resources/帮助.png"))
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.help  = QDialog()
        self.qlabel = QLabel(self.help)