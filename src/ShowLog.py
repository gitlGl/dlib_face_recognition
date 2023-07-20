from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QPoint,pyqtSlot,QSize
from  PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QVBoxLayout,QMenu,QHeaderView,QMessageBox, QDialog,QCheckBox
from PyQt5 import QtWidgets
from .ImageView import ShowImage
from .GlobalVariable import database
from .Paging import Page
import os
from PyQt5.QtGui import QIcon
class ShowLog(QDialog):
    def __init__(self,id_number, QTableWidget_column_name,table_name, table_cloumn_name):
        super().__init__()
        self.id_number = id_number
        self.page_count = 30
        self.table_name = table_name
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("学生日志")
        self.setWindowIcon(QIcon("resources/日志.svg"))
        self.resize(300,400)
        self.tableWidget = QTableWidget(self)
        self.table_cloumn_name = table_cloumn_name
        self.page = Page(self.table_name+"_log_time",table_cloumn_name,
        page_count=self.page_count,id_number = id_number)
        if  not self.page.information:
            QMessageBox.critical(self, '警告', '不存在用户或记录')
            self.close()
            return
        self.page.information_signal.connect(self.setInformation)
        
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
        
        self.tableWidget.customContextMenuRequested[QPoint].connect(self.contextMenu)#菜单右键槽函数
        self.tableWidget.cellDoubleClicked.connect(self.onTableWidgetCellDoubleClicked)
        self.VBoxLayout = QVBoxLayout()
        self.VBoxLayout.addWidget(self.tableWidget)
        self.VBoxLayout.addWidget(self.page)
        self.setLayout(self.VBoxLayout)
        self.resize(480, 600)
        columncout = len( QTableWidget_column_name)
        self.tableWidget.setColumnCount(columncout)#根据数据量确定列数
        self.tableWidget.setHorizontalHeaderLabels( QTableWidget_column_name)
        self.setInformation()

    
        
    def setInformation(self):
        self.information = self.page.information
        self.tableWidget.setRowCount(0)
        for row,i in enumerate(self.information):
            i["log_time"] = i["log_time"].strftime("%Y-%m-%d-%H-%M")#时间格式化
           
            self.tableWidget.insertRow(row)
            for row2,cloumn in enumerate(self.table_cloumn_name[1:]):#第一列为id，列表中不显示，所以从第二列开始，且id删除时需要使用
                item  = QTableWidgetItem(i[cloumn])
                self.tableWidget.setItem(row, row2, item)
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                
            
            imag_path = "img_information/{0}/{1}/log/{2}.jpg".format(self.table_name,i["id_number"],i["log_time"])
            img_item =  QTableWidgetItem()
            img_item.setIcon(QIcon(imag_path))
            self.tableWidget.setItem(row, row2+1,img_item)
            self.tableWidget.setIconSize(QSize(60, 100))
            
      
           
    def onTableWidgetCellDoubleClicked(self, row, column):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        imag_path = "img_information/{0}/{1}/log/{2}.jpg".format(
            self.table_name,str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
        show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
        show_imag.exec_()

    @pyqtSlot(QPoint)
    def contextMenu(self,pos):
        item = self.tableWidget.itemAt(pos)
        if item == None:
            return
        selected_rows = set()
        for r in self.tableWidget.selectedRanges():
            selected_rows.update(range(r.topRow(), r.bottomRow() + 1))
        selected_rows = list(selected_rows)
        selected_rows.sort(reverse=True)
        pop_menu = QMenu()
        #菜单事件信号
        delete_event = pop_menu.addAction("删除")
        imageView_event = pop_menu.addAction("查看图片")
        if len(selected_rows) > 1:
            imageView_event.setEnabled(False)
       
        row = item.row()
        action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))#显示菜单列表，pos为菜单栏坐标位置
        if action == delete_event:
            r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No)
            if r == QMessageBox.No:
                return
            for row in selected_rows:
                self.delete(row)

        if action == imageView_event:
            imag_path = "img_information/{0}/{1}/log/{2}.jpg".format(
                self.table_name,str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
            show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
            show_imag.exec_()

    def delete(self,row):
        
        log_table = self.table_name + "_log_time"
        database.c.execute("delete from {0} where id  = {1}".format(
            log_table,self.information[row]["id"]))
        if self.table_name == "student":
            database.c.execute(
            "SELECT count,id_number from {0} where id_number = '{1}'".format(
                self.table_name,str(self.information[row]["id_number"])))
            item = database.c.fetchall()[0] # 取出返回所有数据，fetchall返回类型是[()]
            if item["count"] is not None:
                database.c.execute(
        "UPDATE {0} SET count = {1} WHERE id_number = {2}".format(
                self.table_name,item["count"]-1,item["id_number"]))
        database.conn.commit()
                
        imag_path = "img_information/{0}/{1}/log/{2}.jpg".format(
            self.table_name,str(self.information[row]["id_number"]),str(self.information[row]["log_time"]))
        if os.path.isfile(imag_path):
            os.remove(imag_path)
        
        self.tableWidget.removeRow(row) 
        self.information.pop(row)#删除信息列表
        return

