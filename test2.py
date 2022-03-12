import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):
	def __init__(self):
		# 主界面初始化
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		# 一级菜单栏初始化
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menu = QtWidgets.QMenu(self.menubar)
		self.menu_2 = QtWidgets.QMenu(self.menubar)
		self.menu_3 = QtWidgets.QMenu(self.menubar)
		self.menu_4 = QtWidgets.QMenu(self.menubar)
		# 二级菜单栏初始化
		self.actionRGB_histogram = QtWidgets.QAction(MainWindow)
		self.action = QtWidgets.QAction(MainWindow)
		self.actionDAISY = QtWidgets.QAction(MainWindow)
		self.actionEHD = QtWidgets.QAction(MainWindow)
		self.action_2 = QtWidgets.QAction(MainWindow)
		self.actionVGG = QtWidgets.QAction(MainWindow)
		self.actionResNet = QtWidgets.QAction(MainWindow)
		# 界面布局
		self.Layout = QVBoxLayout(self.centralwidget)  # 垂直布局
		# stackedWidget初始化
		self.stackedWidget = QStackedWidget()

	def setupUi(self, MainWindow):
		# 创建界面
	
		MainWindow.resize(1440, 773)
		MainWindow.setCentralWidget(self.centralwidget)
		# 一级菜单栏布置
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 24))
		MainWindow.setMenuBar(self.menubar)
		# # 二级菜单栏布置
		self.menu.addAction(self.actionRGB_histogram)

		self.menu_2.addAction(self.action)

		self.menu_3.addAction(self.actionDAISY)
		self.menu_3.addAction(self.actionEHD)
		self.menu_3.addAction(self.action_2)
        
		self.menu_4.addAction(self.actionVGG)
		self.menu_4.addAction(self.actionResNet)

		self.menubar.addAction(self.menu.menuAction())
		self.menubar.addAction(self.menu_2.menuAction())
		self.menubar.addAction(self.menu_3.menuAction())
		self.menubar.addAction(self.menu_4.menuAction())

		# 布局添加stackedWidget控件
		self.Layout.addWidget(self.stackedWidget)

		# 设置主界面面板：
		self.form = QWidget()
		self.formLayout = QHBoxLayout(self.form)  # 水平布局
		self.label0 = QLabel()
		self.label0.setText("主界面！")
		self.label0.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
		self.label0.setAlignment(Qt.AlignCenter)
		self.label0.setFont(QFont("Roman times", 50, QFont.Bold))
		self.formLayout.addWidget(self.label0)  # 添加控件

		# 设置第1个面板：
		self.form1 = QWidget()
		self.formLayout1 = QHBoxLayout(self.form1)  # 水平布局
		self.label1 = QLabel()
		self.label1.setText("Color")
		self.label1.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
		self.label1.setAlignment(Qt.AlignCenter)
		self.label1.setFont(QFont("Roman times", 50, QFont.Bold))
		self.formLayout1.addWidget(self.label1)  # 添加控件
		# 设置第2个面板：
		self.form2 = QWidget()
		self.formLayout2 = QHBoxLayout(self.form2)
		self.label2 = QLabel()
		self.label2.setText("Gabor")
		self.label2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
		self.label2.setAlignment(Qt.AlignCenter)
		self.label2.setFont(QFont("Roman times", 50, QFont.Bold))
		self.formLayout2.addWidget(self.label2)
		# 设置第3个面板：
		self.form3 = QWidget()
		self.formLayout3 = QHBoxLayout(self.form3)
		self.label3 = QLabel()
		self.label3.setText("DAISY")
		self.label3.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
		self.label3.setAlignment(Qt.AlignCenter)
		self.label3.setFont(QFont("Roman times", 50, QFont.Bold))
		self.formLayout3.addWidget(self.label3)
		# 设置第4个面板：
		self.form4 = QWidget()
		self.formLayout4 = QHBoxLayout(self.form4)
		self.label4 = QLabel()
		self.label4.setText("EHD")
		self.label4.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
		self.label4.setAlignment(Qt.AlignCenter)
		self.label4.setFont(QFont("Roman times", 50, QFont.Bold))
		self.formLayout4.addWidget(self.label4)
		# 设置第5个面板：
		self.form5 = QWidget()
		self.formLayout5 = QHBoxLayout(self.form5)
		self.label5 = QLabel()
		self.label5.setText("HOG")
		self.label5.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
		self.label5.setAlignment(Qt.AlignCenter)
		self.label5.setFont(QFont("Roman times", 50, QFont.Bold))
		self.formLayout5.addWidget(self.label5)
		# 设置第6个面板：
		self.form6 = QWidget()
		self.formLayout6 = QHBoxLayout(self.form6)
		self.label6 = QLabel()
		self.label6.setText("VGG")
		self.label6.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
		self.label6.setAlignment(Qt.AlignCenter)
		self.label6.setFont(QFont("Roman times", 50, QFont.Bold))
		self.formLayout6.addWidget(self.label6)
		# 设置第7个面板：
		self.form7 = QWidget()
		self.formLayout7 = QHBoxLayout(self.form7)
		self.label7 = QLabel()
		self.label7.setText("ResNet")
		self.label7.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
		self.label7.setAlignment(Qt.AlignCenter)
		self.label7.setFont(QFont("Roman times", 50, QFont.Bold))
		self.formLayout7.addWidget(self.label7)

		# stackedWidget添加各种界面用于菜单切换
		self.stackedWidget.addWidget(self.form)
		self.stackedWidget.addWidget(self.form1)
		self.stackedWidget.addWidget(self.form2)
		self.stackedWidget.addWidget(self.form3)
		self.stackedWidget.addWidget(self.form4)
		self.stackedWidget.addWidget(self.form5)
		self.stackedWidget.addWidget(self.form6)
		self.stackedWidget.addWidget(self.form7)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)


	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		# 窗口名称
		MainWindow.setWindowTitle(_translate("MainWindow", "HZAU实训CBIR系统 @ by ZilanYu"))
		# 一级目录
		self.menu.setTitle(_translate("MainWindow", "基于颜色查找"))
		self.menu_2.setTitle(_translate("MainWindow", "基于纹理查找"))
		self.menu_3.setTitle(_translate("MainWindow", "基于形状查找"))
		self.menu_4.setTitle(_translate("MainWindow", "基于深度学习查找"))
		# 二级目录
		# Color方法1：RGB直方图
		self.actionRGB_histogram.setText(_translate("MainWindow", "RGB 直方图"))
		self.actionRGB_histogram.triggered.connect(self.gotoColorWin)
		# Texture方法1：Gabor滤波
		self.action.setText(_translate("MainWindow", "Gabor 滤波"))
		self.action.triggered.connect(self.gotoTexWin)
		# shape方法1：DAISY算子
		self.actionDAISY.setText(_translate("MainWindow", "DAISY 算子"))
		self.actionDAISY.triggered.connect(self.gotoDaisyWin)
		# shape方法2：EHD
		self.actionEHD.setText(_translate("MainWindow", "边缘直方图描述符（EHD）"))
		self.actionEHD.triggered.connect(self.gotoEHDWin)
		# shape方法3：HOG
		self.action_2.setText(_translate("MainWindow", "方向梯度直方图（HOG）"))
		self.action_2.triggered.connect(self.gotoHOGWin)
		# deep-learning方法1：VGG
		self.actionVGG.setText(_translate("MainWindow", "VGG"))
		self.actionVGG.triggered.connect(self.gotoVGGWin)
		# deep-learning方法2：ResNet
		self.actionResNet.setText(_translate("MainWindow", "ResNet"))
		self.actionResNet.triggered.connect(self.gotoResWin)

	# 菜单栏触发每个界面调用函数
	def gotoColorWin(self):
		self.stackedWidget.setCurrentIndex(1)
	def gotoTexWin(self):
		self.stackedWidget.setCurrentIndex(2)
	def gotoDaisyWin(self):
		self.stackedWidget.setCurrentIndex(3)
	def gotoEHDWin(self):
		self.stackedWidget.setCurrentIndex(4)
	def gotoHOGWin(self):
		self.stackedWidget.setCurrentIndex(5)
	def gotoVGGWin(self):
		self.stackedWidget.setCurrentIndex(6)
	def gotoResWin(self):
		self.stackedWidget.setCurrentIndex(7)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
