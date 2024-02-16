
import os,sys
current_file_path = os.path.abspath(__file__)
current_work_path = os.path.dirname(current_file_path)
os.chdir(current_work_path)
from PySide6.QtWidgets import QApplication
from src import Main
import sys
from qss import StyleSheet
from PySide6.QtGui import QFont
from PySide6 import QtCore
from src import resources_dir,base_dir,isVerifyeRemote
from src import logger
#方便启动远程验证时进行测试



if __name__ == '__main__':
    # QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    logger.basicConfig()#初始化全局默认日志配置
    if isVerifyeRemote:
        os.system(f'start python {base_dir}\\Server.py')  
    app = QApplication(sys.argv)
    translator = QtCore.QTranslator()
    translator.load(resources_dir + "widgets_zh_CN_all.qm")#加载中文文件
    app.installTranslator(translator)
    f = QFont("宋体",10)
    app.setFont(f)
    app.setStyleSheet(StyleSheet)   
    ui = Main()
    app.exec()



