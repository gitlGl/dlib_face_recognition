from PySide6.QtWidgets import QWidget,QPushButton,\
QHBoxLayout,QVBoxLayout,QLabel,QLineEdit,QMessageBox
from PySide6.QtCore import Signal
from .Database import database
from PySide6.QtGui import QIntValidator
class Paging(QWidget):
    page_number = Signal(int)
    def __init__(self,total_page=20):
        super(Paging, self).__init__()
        self.total_page = total_page
        
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.setPageController()
    
    def setPageController(self):
        """自定义页码控制器"""
        control_layout = QHBoxLayout()
        home_page = QPushButton("首页",objectName="GreenButton")
        pre_page = QPushButton("<上一页",objectName="GreenButton")
        self.cur_page = QLabel("1")
        next_page = QPushButton("下一页>",objectName="GreenButton")
        final_page = QPushButton("尾页",objectName="GreenButton")
        self.totalPage = QLabel("共" + str(self.total_page) + "页")
        skipLable_0 = QLabel("跳到")
        self.skip_page = QLineEdit(objectName="QLineEdit2")
        self.skip_page.setMaxLength(4)
        self.skip_page.setValidator(QIntValidator())
        skip_label_1 = QLabel("页")
        confirm_skip = QPushButton("确定",objectName="GreenButton")
        home_page.clicked.connect(self.homeTotalPage)
        pre_page.clicked.connect(self.preTotalPage)
        next_page.clicked.connect(self.nextTotalPage)
        final_page.clicked.connect(self.finalTotalPage)
        confirm_skip.clicked.connect(self.confirmSkip)
        control_layout.addStretch(1)
        control_layout.addWidget(home_page)
        control_layout.addWidget(pre_page)
        control_layout.addWidget(self.cur_page)
        control_layout.addWidget(next_page)
        control_layout.addWidget(final_page)
        control_layout.addWidget(self.totalPage)
        control_layout.addWidget(skipLable_0)
        control_layout.addWidget(self.skip_page)
        control_layout.addWidget(skip_label_1)
        control_layout.addWidget(confirm_skip)
        control_layout.addStretch(1)
        self.__layout.addLayout(control_layout)

    def homeTotalPage(self):
        """跳转首页"""
        self.cur_page.setText("1")
        self.page_number.emit(1)
       

    def preTotalPage(self):
        """跳转上一页"""
        if 1 == int(self.cur_page.text()):
            QMessageBox.information(self, "提示", "已经是第一页了")
            return
        self.page_number.emit(int(self.cur_page.text())-1)
        self.cur_page.setText(str(int(self.cur_page.text())-1))
      
       

    def nextTotalPage(self):
        """跳转下一页"""
        if int(self.cur_page.text()) >= self.total_page:
            QMessageBox.information(self, "提示", "已经是最后一页了")
            return
        self.page_number.emit(int(self.cur_page.text())+1)
        self.cur_page.setText(str(int(self.cur_page.text())+1))
        return
       

    def finalTotalPage(self):
        """跳转尾页"""
        self.page_number.emit(int(self.total_page))
        self.cur_page.setText(str(self.total_page))
        return
       

    def confirmSkip(self):
        """跳转指定页"""
        if not self.skip_page.text() :
            QMessageBox.information(self, "提示", "请输入页码")
            return
        if not self.skip_page.text().isdigit():
            QMessageBox.information(self, "提示", "页码为数字")
            self.skip_page.clear()
            return

        if self.total_page < int(self.skip_page.text()) or int(self.skip_page.text()) < 0:
            QMessageBox.information(self, "提示", "跳转页码超出范围")
            self.skip_page.clear()
            return
        self.cur_page.setText(self.skip_page.text())
        self.page_number.emit(int(self.skip_page.text()))
        self.skip_page.clear()
        return
        


class Page(Paging):
    information_signal = Signal()
    def __init__(self,table,column,page_count=15,id_number=None,):
        super().__init__(Page.totalCount(table,page_count,id_number))
        self.page_count = page_count
        self.id_number = id_number
        self.table = table
        self.column = column
        
        #super().__init__(page_count,self.total_page)
        self.page_number.connect(self.setInformation)
        self.initInformation()
  
    def initInformation(self):
        """数据初始化"""
        self.total_page = Page.totalCount(self.table,self.page_count,self.id_number)
        self.string = ""#拼接sql语句
        for i in self.column:
            self.string = self.string+i+","
        self.string = self.string[:-1]
        if self.id_number:#显示用户log数据
            self.sql =  "select {0} from {1} where id_number ={2}   limit {3} offset {4}"
            sql = self.sql.format(self.string,self.table,self.id_number,self.page_count,0)
            self.information = database.execute(sql)
            return
        #显示用户
        self.sql =  "select {0} from {1}   limit {2} offset {3}"
        sql = self.sql.format(self.string,self.table,self.page_count,0)
        self.information = database.execute(sql)
       

        
            
            

    def setInformation(self, signal=0):
        """获取数据库数据"""
        total_page = Page.totalCount(self.table,self.page_count,self.id_number)
        self.totalPage.setText("共" + str(total_page) + "页")#更新总页数
        self.total_page = total_page
        if self.id_number:#显示用户log数据
            sql = self.sql.format(self.string,self.table,self.id_number,self.page_count,(signal-1)*self.page_count)
            self.information =  database.execute(sql)
            self.information_signal.emit()
            return
        #显示用户
        sql = self.sql.format(self.string,self.table,self.page_count,(signal-1)*self.page_count)
        self.information =   database.execute(sql)
        
        self.information_signal.emit()
        

        
    #计算页数,静态函数
    @staticmethod
    def totalCount(table,page_count,id_number=None):
        if id_number:
            count =  database.execute(
                "select count(*)  from {0} where id_number ={1} "
                .format(table,id_number))
           
        else:
            count = database.execute(
            "select count(*)  from {0} "
            .format(table))
           
            
        if not count[0]["count(*)"]:
            return 0
    
        count  = count[0]["count(*)"]
        i = count/page_count
        q = count%page_count
    
        if count < page_count:
            total_page = 1
            return total_page
    
        if q > 0:
            total_page = i+1
            return int(total_page)
        else:
            total_page = i
            return int(total_page)
    



