from PyQt5.QtWidgets import *
class Plugin4(QWidget):
    label="第四个插件"
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        la = QPushButton("test",self)

def get_plugin_class():
    return Plugin4
