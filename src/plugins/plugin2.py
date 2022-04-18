from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class Plugin2(QWidget):
    label="第二个插件"
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setWindowModality(Qt.ApplicationModal)
       
def get_plugin_class():
    return Plugin2
