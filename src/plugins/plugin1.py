from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
class Plugin1(QWidget):
    label="第一个插件"
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setWindowModality(Qt.ApplicationModal)

def get_plugin_class():
    return Plugin1
