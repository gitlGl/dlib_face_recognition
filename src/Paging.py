import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from .Database import Database
class Paging(QWidget):
    control_signal = pyqtSignal(str)
    page_number = pyqtSignal(int)
    

    def __init__(self,total_page=20):
        super(Paging, self).__init__()
        self.total_page = total_page
        self.control_signal.connect(self.page_controller)
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.setPageController()
    
    def setPageController(self):
        """自定义页码控制器"""
        control_layout = QHBoxLayout()
        homePage = QPushButton("首页",objectName="GreenButton")
        prePage = QPushButton("<上一页",objectName="GreenButton")
        self.curPage = QLabel("1")
        nextPage = QPushButton("下一页>",objectName="GreenButton")
        finalPage = QPushButton("尾页",objectName="GreenButton")
        self.totalPage = QLabel("共" + str(self.total_page) + "页")
        skipLable_0 = QLabel("跳到")
        self.skipPage = QLineEdit(objectName="QLineEdit2")
        skipLabel_1 = QLabel("页")
        confirmSkip = QPushButton("确定",objectName="GreenButton")
        homePage.clicked.connect(self.__home_total_page)
        prePage.clicked.connect(self.__pre_total_page)
        nextPage.clicked.connect(self.__next_total_page)
        finalPage.clicked.connect(self.__final_total_page)
        confirmSkip.clicked.connect(self.__confirm_skip)
        control_layout.addStretch(1)
        control_layout.addWidget(homePage)
        control_layout.addWidget(prePage)
        control_layout.addWidget(self.curPage)
        control_layout.addWidget(nextPage)
        control_layout.addWidget(finalPage)
        control_layout.addWidget(self.totalPage)
        control_layout.addWidget(skipLable_0)
        control_layout.addWidget(self.skipPage)
        control_layout.addWidget(skipLabel_1)
        control_layout.addWidget(confirmSkip)
        control_layout.addStretch(1)
        self.__layout.addLayout(control_layout)

    def __home_total_page(self):
        """点击首页信号"""
        self.control_signal.emit("home")

    def __pre_total_page(self):
        """点击上一页信号"""
        self.control_signal.emit("pre")

    def __next_total_page(self):
        """点击下一页信号"""
        self.control_signal.emit("next")

    def __final_total_page(self):
        """尾页点击信号"""
        self.control_signal.emit("final")

    def __confirm_skip(self):
        """跳转页码确定"""
        if not self.skipPage.text() :
            QMessageBox.information(self, "提示", "请输入页码", QMessageBox.Yes)
            return
        if not self.skipPage.text().isdigit():
            QMessageBox.information(self, "提示", "页码为数字", QMessageBox.Yes)
            return
        self.control_signal.emit("confirm")



    def page_controller(self, signal):
        if "home" == signal:
            self.curPage.setText("1")

            self.page_number.emit(1)
            return

        if "pre" == signal:
            if 1 == int(self.curPage.text()):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.page_number.emit(int(self.curPage.text())-1)
            self.curPage.setText(str(int(self.curPage.text())-1))
            return

        if "next" == signal:
            if self.total_page == int(self.curPage.text()):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.page_number.emit(int(self.curPage.text())+1)
            self.curPage.setText(str(int(self.curPage.text())+1))
            return
        if "final" == signal:
            self.page_number.emit(int(self.total_page))
            self.curPage.setText(str(self.total_page))
            return
        
        if "confirm" == signal:
            if self.total_page < int(self.skipPage.text()) or int(self.skipPage.text()) < 0:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                return
            self.curPage.setText(self.skipPage.text())
            self.page_number.emit(int(self.skipPage.text()))
            return
        


       
          


class Page(Paging):
    information_signal = pyqtSignal()
    def __init__(self,table,column,page_count=15,id_number=None,):
        super().__init__(Page.total_count(table,page_count,id_number))
        self.page_count = page_count
        self.id_number = id_number
        self.table = table
        self.column = column
        
        #super().__init__(page_count,self.total_page)
        self.page_number.connect(self.set_information)
        self.init_information()
  
    def init_information(self):
        self.total_page = Page.total_count(self.table,self.page_count,self.id_number)
        self.string = ""
        for i in self.column:
            self.string = self.string+i+","
        self.string = self.string[:-1]
        if self.id_number:
            
            self.sql =  "select {0} from {1} where id_number ={2}   limit {3} offset {4}"
            sql = self.sql.format(self.string,self.table,self.id_number,self.page_count,0)
            print(sql)
                
            self.information = Database().c.execute(sql).fetchall()

        else:
            self.sql =  "select {0} from {1}   limit {2} offset {3}"
            sql = self.sql.format(self.string,self.table,self.page_count,0)
            self.information = Database().c.execute(sql).fetchall()
        if not self.information:
                QMessageBox.critical(self, 'Wrong', '不存在用户记录')
                return
            
            

    def set_information(self, signal=0):
        total_page = Page.total_count(self.table,self.page_count,self.id_number)
        self.totalPage.setText("共" + str(total_page) + "页")#更新总页数
        self.total_page = total_page
        if self.id_number:
            sql = self.sql.format(self.string,self.table,self.id_number,self.page_count,(signal-1)*self.page_count)
            print(sql)
            self.information = Database().c.execute(sql).fetchall()
            self.information_signal.emit()
        
        else:
            sql = self.sql.format(self.string,self.table,self.page_count,(signal-1)*self.page_count)
            print(sql)
            self.information = Database().c.execute(sql).fetchall()
            self.information_signal.emit()
        return

        
    #计算页数,静态函数
    def total_count(table,page_count,id_number=None):
        print(id_number)


        if id_number:
            Page.count = Database().c.execute(
                "select count(id_number)  from {0} where id_number ={1} "
                .format(table,id_number)).fetchall()
            print(Page.count)
            print("select count(id_number)  from {0} where id_number ={1} "
                .format(table,id_number))
          
        else:
            
            Page.count = Database().c.execute(
            "select count(id_number)  from {0} "
            .format(table)).fetchall()
            print("select count(id_number)  from {0} "
            .format(table))
            print(Page.count)
            
        if not Page.count[0]["count(id_number)"]:
            return 0
       
       
        print(Page.count)
        count  = Page.count[0]["count(id_number)"]
        i = count/page_count
        q = count%page_count
    
        if count < page_count:
            total_page = 1
            return total_page
        else:
            if q > 0:
                total_page = i+1
                return int(total_page)
            else:
                total_page = i
                return int(total_page)
    

# app = QApplication(sys.argv)
# window = PageSudentLog()
# window.show()
# sys.exit(app.exec_())

