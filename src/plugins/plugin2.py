from PyQt5.QtWidgets import *
class Plugin2(QWidget):
    label="第二个插件"
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.label=QLabel("test",self)

def get_plugin_class():
    return Plugin2
