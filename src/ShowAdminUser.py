from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize, QPoint,pyqtSlot
from .ImageView import ShowImage
from  PyQt5.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QVBoxLayout,QMenu,QHeaderView,QMessageBox,QAbstractItemView
from .UpdateAdminData import UpdateAdminData
from .Database import Database
from .ShowAdminLog import ShowAdminLog
class ShowAdminUser(QWidget):
    def __init__(self,information,str_list_column ):
        super().__init__()
        self.information = information
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
        # self.qlineedit = QLineEdit()
        # self.qlineedit.setPlaceholderText('Please enter your usernumber')
        # self
        self.tableWidget.customContextMenuRequested[QPoint].connect(self.context_menu)#菜单右键槽函数
        self.tableWidget.cellDoubleClicked.connect(self.on_tableWidget_cellDoubleClicked)
        self.VBoxLayout = QVBoxLayout()
        self.VBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.VBoxLayout)
        columncout = len(str_list_column)
        self.tableWidget.setColumnCount(columncout)#根据数据量确定列数
        self.tableWidget.setHorizontalHeaderLabels(str_list_column)
        self.set_information()
    def set_information(self):
        row = 0
        for i in self.information:
            if i["id_number"] == "12345678910":
                self.information.remove(self.information[row])
                continue
            self.tableWidget.setRowCount(row)
            self.tableWidget.insertRow(row)
            sid_item = QTableWidgetItem(str(i["id_number"]))
            pwd_item = QTableWidgetItem(i["password"])
            img_item =  QTableWidgetItem()
            self.tableWidget.setIconSize(QSize(60, 100))
            imag_path = "img_information/admin/{0}/{1}.jpg".format(i["id_number"],i["id_number"])#获取图片路径
            img_item.setIcon(QIcon(imag_path))
            sid_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            pwd_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            self.tableWidget.setItem(row, 0, sid_item)
            self.tableWidget.setItem(row, 1, pwd_item)
            self.tableWidget.setItem(row, 2,img_item)
            row = row + 1
           
      
           
    def on_tableWidget_cellDoubleClicked(self, row):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        update_data =UpdateAdminData(self.information[row])
        ok = update_data.exec_()
        if not ok:
            return
        
        id_number = update_data.id_number_line.text()
        password = update_data.password_line.text()

        #变更信息后修改信息
        self.information[row]["id_number"] = id_number
        self.information[row]["password"] = password
       
         #变更表格信息
        self.tableWidget.item(row, 0).setText(id_number)
        self.tableWidget.item(row, 1).setText(password)
        self.tableWidget.item(row,2).setIcon(QIcon("img_information/admin/{0}/{1}.jpg"
        .format(self.information[row]["id_number"],self.information[row]["id_number"])))#获取图片路径)
    @pyqtSlot(QPoint)
    def context_menu(self,pos):
        pop_menu = QMenu()
        #菜单事件信号
        change_new_event = pop_menu.addAction("修改")
        delete_event = pop_menu.addAction("删除")
        imageView_event = pop_menu.addAction("查看图片")
        log_event = pop_menu.addAction("查看日志")
        item = self.tableWidget.itemAt(pos)
        if item == None:
            return
        
        row = item.row()
        print(row)
        update_data =UpdateAdminData(self.information[row])
        action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))#显示菜单列表，pos为菜单栏坐标位置
        if action == change_new_event:
            id_number = update_data.id_number_line.text()
            password = update_data.password_line.text()
            ok = update_data.exec_()
            if not ok:
                return
            password = update_data.password_line.text()
            id_number = update_data.id_number_line.text()
        
        #变更信息后修改信息
            self.information[row]["id_number"] = id_number
            self.information[row]["password"] = password

        #变更表格信息
            self.tableWidget.item(item.row(), 0).setText(id_number)
            self.tableWidget.item(item.row(), 1).setText(password)
            self.tableWidget.item(row,2).setIcon(QIcon("img_information/admin/{0}/{1}.jpg"
    .format(self.information[row]["id_number"],self.information[row]["id_number"])))#获取图片路径)

        if action == delete_event:
            r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if r == QMessageBox.No:
                return
            update_data.delete(self.information[row]["id_number"])
            self.tableWidget.removeRow(row) 
            self.information.remove(self.information[row])#删除信息列表
        if action == imageView_event:
            imag_path = "img_information/admin/{0}/{1}.jpg".format(str(self.information[row]["id_number"]),str(self.information[row]["id_number"]))
            show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
            show_imag.exec_()
            return
        if action == log_event:
            result = Database().c.execute("select rowid,id_number,log_time from admin_log_time where id_number ={0} order by log_time desc".format(self.information[row]["id_number"])).fetchall()
            self.result = ShowAdminLog(result,['用户ID','时间',"图片" ])
            self.result.exec_()
            return

