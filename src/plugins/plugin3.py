from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class Plugin3(QWidget):
    label="第三个插件"
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.tab_widget=QTabWidget()
        # self.tab_widget.addTab("控件里的标签1",QLabel("heheheheheeh1"))
        # self.tab_widget.addTab("控件里的标签1",QLabel("heheheheheeh2"))

def get_plugin_class():
    return Plugin3

