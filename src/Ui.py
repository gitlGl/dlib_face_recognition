from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout,QGroupBox,QCheckBox,QLabel,QSlider
from PySide6.QtCore import Qt,QObject
from PySide6.QtGui import QIcon,QFont,QPixmap
from . import Setting

class Ui(QWidget):
     def __init__(self):
        super().__init__()
     def setupUi(self,mainwin):
        self.setWindowTitle("图书馆人脸识别系统")
        self.setWindowIcon(QIcon("resources/图书馆.svg"))
        #self.setStyleSheet ("border:2px groove gray;border-radius:10px;padding:2px 2px;")
        self.groupbox_1 = QGroupBox()  # 1
        self.groupbox_2 = QGroupBox()
        self.groupbox_1.setFixedSize(460, 40)
        self.groupbox_2.setFixedSize(460, 35)
        self.Vlayout = QVBoxLayout()
        self.Hlayout = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.allvlaout = QVBoxLayout()

        self.open_capture_btn = QPushButton()
        self.normal_rgface_btn = QCheckBox()
        self.Liveness_rgface_btn = QCheckBox()
        self.data_btn = QPushButton(objectName="GreenButton")
        self.help_btn = QPushButton(objectName="GreenButton")
        self.user_btn = QPushButton(objectName="GreenButton")

        self.open_capture_btn.setText("打开摄像头")
        self.open_capture_btn.setObjectName("GreenButton")
        self.open_capture_btn.setIcon(QIcon("resources/摄像头_关闭.svg"))
        self.normal_rgface_btn.setText("普通识别")
        self.Liveness_rgface_btn.setText("活体识别")
      
        self.data_btn.setText("数据")
        self.help_btn.setText("帮助")
        self.help_btn.clicked.connect(mainwin.help)
        self.data_btn.setIcon(QIcon("resources/数据.svg"))
        self.help_btn.setIcon(QIcon("resources/帮助.svg"))
        self.open_capture_btn.setFlat(True)
        self.help_btn.setFlat(True)
        self.data_btn.clicked.connect(mainwin.showData)
        self.open_capture_btn.clicked.connect(mainwin.open)
        self.normal_rgface_btn.clicked.connect(mainwin.openNormal)
        self.Liveness_rgface_btn.clicked.connect(mainwin.openEye)
        self.user_btn.clicked.connect(lambda:mainwin.posMenu(self.user_btn.pos()))

        self.user_btn.setIcon(QIcon("resources/用户.svg"))
        self.user_btn.setText("用户")
        self.tips_label = QLabel()
        self.rg_label = QLabel()
        self.scale_value_label = QLabel()
        self.picture_qlabel = QLabel()
        self.qlabel5 = QLabel()#用于修复无法清理（qlable.claer()）图片
        self.qlabel5.hide()
        self.scale_value_label.setFixedSize(30, 20)
        self.scale_value_label.setFont(QFont("Arial", 10))
        self.scale_value_label.setAlignment(Qt.AlignCenter)
        self.scale_value_label.setText(str(Setting.user_threshold))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMaximum(12)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        self.slider.setValue(8)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(mainwin.valueChange)
        self.slider.setFixedSize(100, 20)
        self.slider.height()

        self.Hlayout.addWidget(self.open_capture_btn)
        self.Hlayout.addWidget(self.normal_rgface_btn)
        self.Hlayout.addWidget(self.Liveness_rgface_btn)
        self.Hlayout.addWidget(self.data_btn)
        self.Hlayout.addWidget(self.help_btn)
        self.Hlayout.addWidget(self.user_btn)
       
        self.groupbox_1.setLayout(self.Hlayout)

        self.Hlayout2.addWidget(self.tips_label)
        self.Hlayout2.addWidget(self.rg_label)
        self.Hlayout2.addWidget(self.slider)
        self.Hlayout2.addWidget(self.scale_value_label)
        self.groupbox_2.setLayout(self.Hlayout2)

        self.Vlayout.addWidget(self.groupbox_1)
        self.Vlayout.addWidget(self.groupbox_2)
        self.Vlayout.addWidget(self.picture_qlabel)
        self.Vlayout.addWidget(self.qlabel5)
        self.allvlaout.addLayout(self.Vlayout)
        self.resize(480, 600)
        self.setLayout(self.allvlaout)