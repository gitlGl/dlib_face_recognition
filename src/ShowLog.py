from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QPoint,pyqtSlot,QSize
from  PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QVBoxLayout,QMenu,QHeaderView,QMessageBox, QDialog
from PyQt5 import QtWidgets
from .ImageView import ShowImage
from .Database import database
from .Paging import Page
import os
from PyQt5.QtGui import QIcon
class ShowLog(QDialog):
    def __init__(self,id_number,str_list_column,table, list_cloumn):
        super().__init__()
        self.id_number = id_number
        self.page_count = 30
        self.table = table
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("学生日志")
        self.setWindowIcon(QIcon("resources/日志.png"))
        self.resize(300,400)
        self.tableWidget = QTableWidget(self)
        self.list_cloumn = list_cloumn
        self.page = Page(self.table+"_log_time",self.list_cloumn,
        page_count=self.page_count,id_number = self.id_number)
        if  not self.page.information:
            self.close()
            return
        self.page.information_signal.connect(self.setInformation)
        
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
        # self.qlineedit = QLineEdit()
        # self.qlineedit.setPlaceholderText('Please enter your usernumber')
        # self
        self.tableWidget.customContextMenuRequested[QPoint].connect(self.contextMenu)#菜单右键槽函数
        self.tableWidget.cellDoubleClicked.connect(self.onTableWidgetCellDoubleClicked)
        self.VBoxLayout = QVBoxLayout()
        self.VBoxLayout.addWidget(self.tableWidget)
        self.VBoxLayout.addWidget(self.page)
        self.setLayout(self.VBoxLayout)
        self.resize(480, 600)
        columncout = len(str_list_column)
        self.tableWidget.setColumnCount(columncout)#根据数据量确定列数
        self.tableWidget.setHorizontalHeaderLabels(str_list_column)
        self.setInformation()

    
        
    def setInformation(self):
        self.information = self.page.information
        self.row = 0
        self.tableWidget.setRowCount(0)
        for i in self.information:
            self.tableWidget.insertRow(self.row)
            self.row2 = 0
            for cloumn in self.list_cloumn:
                if cloumn == 'rowid':
                    continue
                item  = QTableWidgetItem((i[cloumn]))
                self.tableWidget.setItem(self.row, self.row2, item)
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.row2 = self.row2 +1
            
            imag_path = "img_information/{0}/{1}/log/{2}.jpg".format(self.table,i["id_number"],i["log_time"])
            img_item =  QTableWidgetItem()
            img_item.setIcon(QIcon(imag_path))
            self.tableWidget.setItem(self.row, self.row2,img_item)
            self.tableWidget.setIconSize(QSize(60, 100))
            self.row = self.row + 1
            self.tableWidget.setRowCount(self.row)
      
           
    def onTableWidgetCellDoubleClicked(self, row, column):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        imag_path = "img_information/{0}/{1}/log/{2}.jpg".format(
            self.table,str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
        show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
        show_imag.exec_()

    @pyqtSlot(QPoint)
    def contextMenu(self,pos):
        pop_menu = QMenu()
        #菜单事件信号
        delete_event = pop_menu.addAction("删除")
        imageView_event = pop_menu.addAction("查看图片")
        item = self.tableWidget.itemAt(pos)
        if item == None:
            return
        row = item.row()
        action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))#显示菜单列表，pos为菜单栏坐标位置
        if action == delete_event:
            r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if r == QMessageBox.No:
                return
           
            log_table = self.table + "_log_time"
            database.c.execute("delete from {0} where rowid  = {1}".format(
                log_table,self.information[row]["rowid"])).fetchall()
            if self.table == "student":
                item = database.c.execute(
                "SELECT  cout,id_number from {0} where id_number = '{1}'".format(
                    self.table,str(self.information[row]["id_number"]))).fetchall()[0] # 取出返回所有数据，fetchall返回类型是[()]
                if item["cout"] is not None:
                    database.c.execute(
            "UPDATE {0} SET cout = {1} WHERE id_number = {2}".format(
                self.table,item["cout"]-1,item["id_number"]))
                    
            imag_path = "img_information/{0}/{1}/log/{2}.jpg".format(
                self.table,str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
            if os.path.isfile(imag_path):
                os.remove(imag_path)
           
            self.tableWidget.removeRow(row) 
            self.information.pop(row)#删除信息列表
            
            return

        if action == imageView_event:
            imag_path = "img_information/{0}/{1}/log/{2}.jpg".format(
                self.table,str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
            show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
            show_imag.exec_()


