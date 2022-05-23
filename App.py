from PyQt5.QtWidgets import QApplication
from src import Ui
import sys
from test import StyleSheet

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)    
    ui = Ui()
    app.exec_()

#     """

#     可视化数据格式
    
#     """




    #   dataTable = [
    #         ["test", [10, 132, 778, 134, 500, 280, 212]],
    #         ["邮件销", [10, 132, 778, 134, 90, 250, 212]],
    #         ["邮件营销", [120, 132, 101, 134, 90, 230

    #         ["联盟广告", [220, 182, 191, 234, 290, 330, 310]],
    #         ["视频广告", [150, 232, 201, 154, 190, 330, 410]],
    #         ["直接访问", [320, 332, 301, 334, 390, 330, 320]],
    #         ["搜索引擎", [820, 932, 901, 934, 1290, 1330, 1320]]
    #     ]