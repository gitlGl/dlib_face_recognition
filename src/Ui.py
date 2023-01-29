from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QLabel, QSlider
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QIcon, QFont


class Ui(QObject):
    def __init__(self):
        super().__init__()

    def setupUi(self, mainwin):
        self.setWindowTitle("图书馆人脸识别系统")
        self.setWindowIcon(QIcon("./resources/图书馆.png"))
        #self.setStyleSheet ("border:2px groove gray;border-radius:10px;padding:2px 2px;")
        self.groupbox_1 = QGroupBox()  # 1
        self.groupbox_2 = QGroupBox()
        self.groupbox_1.setFixedSize(460, 40)
        self.groupbox_2.setFixedSize(460, 35)
        self.Vlayout = QVBoxLayout()
        self.Hlayout = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.allvlaout = QVBoxLayout()

        self.btn1 = QPushButton()
        self.btn2 = QCheckBox()
        self.btn3 = QCheckBox()
        self.btn4 = QPushButton(objectName="GreenButton")
        self.btn5 = QPushButton(objectName="GreenButton")
        self.btn6 = QPushButton(objectName="GreenButton")
        self.btn7 = QPushButton()
        self.btn7 = QPushButton(objectName="GreenButton")
        self.btn7.setText("插件")
        self.btn7.setIcon(QIcon("./resources/插件.png"))
        self.btn7.clicked.connect(
            lambda: mainwin.pos_menu_plugins(self.btn7.pos()))

        self.btn1.setText("打开摄像头")
        self.btn1.setIcon(QIcon("./resources/摄像头_关闭.png"))
        self.btn2.setText("普通识别")
        self.btn3.setText("活体识别")

        self.btn4.setText("数据")
        self.btn5.setText("帮助")
        self.btn5.clicked.connect(mainwin.help)
        self.btn4.setIcon(QIcon("./resources/数据.png"))
        self.btn5.setIcon(QIcon("./resources/帮助.png"))
        self.btn1.setFlat(True)
        self.btn5.setFlat(True)
        self.btn4.clicked.connect(mainwin.show_data)
        self.btn1.clicked.connect(mainwin.open)
        self.btn2.clicked.connect(mainwin.open_normal)
        self.btn3.clicked.connect(mainwin.open_eye)
        self.btn6.clicked.connect(lambda: mainwin.pos_menu(self.btn6.pos()))

        self.btn6.setIcon(QIcon("./resources/用户.png"))
        self.btn6.setText("用户")
        self.qlabel1 = QLabel()
        self.qlabel2 = QLabel()
        self.qlabel3 = QLabel()
        self.qlabel4 = QLabel()
        self.qlabel5 = QLabel()  #用于修复无法清理（qlable.claer()）图片
        self.qlabel5.hide()
        self.qlabel3.setFixedSize(30, 20)
        self.qlabel3.setFont(QFont("Arial", 10))
        self.qlabel3.setAlignment(Qt.AlignCenter)
        self.qlabel3.setText("0.4")
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

        self.Hlayout.addWidget(self.btn1)
        self.Hlayout.addWidget(self.btn2)
        self.Hlayout.addWidget(self.btn3)
        self.Hlayout.addWidget(self.btn4)
        #self.Hlayout.addWidget(self.btn7)
        self.Hlayout.addWidget(self.btn5)
        self.Hlayout.addWidget(self.btn6)

        self.groupbox_1.setLayout(self.Hlayout)

        self.Hlayout2.addWidget(self.qlabel1)
        self.Hlayout2.addWidget(self.qlabel2)
        self.Hlayout2.addWidget(self.slider)
        self.Hlayout2.addWidget(self.qlabel3)
        self.groupbox_2.setLayout(self.Hlayout2)

        self.Vlayout.addWidget(self.groupbox_1)
        self.Vlayout.addWidget(self.groupbox_2)
        self.Vlayout.addWidget(self.qlabel4)
        self.Vlayout.addWidget(self.qlabel5)
        self.allvlaout.addLayout(self.Vlayout)
        self.resize(480, 600)
        self.setLayout(self.allvlaout)