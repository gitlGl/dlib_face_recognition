from PySide6.QtWidgets import  QDialog,QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
class Help(QDialog):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle("帮助")
        self.setWindowIcon(QIcon("resources/帮助.svg"))
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.qlabel = QLabel(self)
        self.qlabel.setText("""

        <font style = 'font-size:15px; color:#cc163a;'> 使用帮助  </font>
          <font style = 'font-size:30px; color:#621d34;'> 不同颜色 </font>

        """
    
        


        
        
                            
                            
                            
                            )
        self.resize(480, 600)