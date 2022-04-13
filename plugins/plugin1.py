from PyQt5.QtWidgets import *
class Plugin1(QWidget):
    label="第一个插件"
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

def get_plugin_class():
    return Plugin1
