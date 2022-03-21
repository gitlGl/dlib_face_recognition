from src.Creatuser import CreatStudentUser
from src.Database import Database
from src.SearchData import SearchData
import sys,math
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import copy
from PyQt5.QtChart import QChartView, QChart, QLineSeries, QLegend, \
        QCategoryAxis
from PyQt5.QtCore import Qt, QPointF, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsLineItem, QWidget, \
        QHBoxLayout, QLabel, QVBoxLayout, QGraphicsProxyWidget,QLineEdit
from src.LineStack import ChartView
class Win(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300,400, 380)
        self.setWindowTitle('数据分析')
        self.setWindowModality(Qt.ApplicationModal)
        

        self.Hlayout = QHBoxLayout()
        self.Vhlayout = QVBoxLayout()
        self.linnedit = QLineEdit()
        #self.linnedit.setFixedSize(400,15)
        self.linnedit.setMaximumSize(200,20)
        self.linnedit.setPlaceholderText('Please enter your usernumber')
        self.grou = QGroupBox(self)
        self.qlabel = QLabel()
        self.label = QLabel()
        self.label.setText("  ")
        self.btn1 = QPushButton("分析")
        self.btn1 = QPushButton(objectName="GreenButton")
        self.btn1.setIcon(QIcon("./resources/分析.png"))
        self.btn2 = QPushButton()
        self.btn2 = QPushButton(objectName="GreenButton")
        self.btn2.setIcon(QIcon("./resources/搜索.png"))
        self.btn3 = QPushButton()
        self.btn1.setText("分析")
        self.btn2.setText("查询")
        self.qlabel.setText("时间范围：")
        self.btn3 = QPushButton()
        self.btn3 = QPushButton(objectName="GreenButton")
        self.btn3.setIcon(QIcon("./resources/文件.png"))
        self.btn3.setText("批量创建用户")
        
        
        #self.grou.setFixedSize(self.width(), 40)
        self.grou.move(0,0)
        self.DateEdit1 = QDateEdit(QDate.currentDate(),self)
        self.DateEdit2 =QDateEdit(QDate.currentDate())
        self.DateEdit1.setDisplayFormat("yyyy-MM-dd")#设置格式
        self.DateEdit2.setDisplayFormat("HH")#设置格式
        self.DateEdit1.setMinimumDate(QDate.currentDate().addDays(-365))#设置最小日期
        self.DateEdit1.setMaximumDate(QDate.currentDate().addDays(365))#设置最大日期
        self.DateEdit1.setCalendarPopup(True)#弹出日历
        self.DateEdit2.setCalendarPopup(True)
        self.Hlayout.addWidget(self.qlabel)
        self.Hlayout.addWidget(self.DateEdit1)
        self.Hlayout.addWidget(self.DateEdit2)
        self.Hlayout.addWidget(self.btn1)
        self.Hlayout.addWidget(self.label)
        self.Hlayout.addWidget(self.linnedit)
        self.Hlayout.addWidget(self.btn2)
        self.Hlayout.addWidget(self.btn3)
        self.grou.setLayout(self.Hlayout)
        self.Vhlayout.addWidget(self.grou)
        self.grou.setMaximumSize(800,40)
        self.setLayout(self.Vhlayout)
        self.btn1.clicked.connect(self.analyze_data)
        self.btn2.clicked.connect(self.show_search_result)
        self.btn3.clicked.connect(self.creat_student_user)
        datatabel,data_title ,number=  self.get_data_(0)
        self.view = ChartView(datatabel,data_title,number)
        self.Vhlayout.addWidget(self.view)
  
    # def resizeEvent(self, event):
    #     super(ChartView, self).resizeEvent(event)
    #     self.grou.resize(self.width,40)
    def creat_student_user(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择文件", "c:\\",
                                              "files(*.xlsx )")
        if path == '':
            return
        list_error = CreatStudentUser().creat_user(path)
        if len(list_error) == 0:
            QMessageBox.information(self, 'Information',
                                    'Register Successfully')
            return
        else:
            error_string = ""
            for i in list_error:
                error_string = error_string + i + "\n"

            QMessageBox.information(self, 'Information', error_string)

    def show_search_result(self):
        if not self.linnedit.text(): 
             QMessageBox.critical(self, 'Wrong', '请输入学号')
             return 
        id_number = self.linnedit.text()
        if not id_number.isdigit():
            QMessageBox.critical(self, 'Wrong', '学号为数字')
            return
            
        result = Database().c.execute("select id_number,user_name,gender from student where id_number = {}".format(int(id_number))).fetchall()
        if len(result)!= 0:
            information = {"id_number":str(result[0][0])}
            if  result[0][2] == 0:
                information["gender"] = "女"
            else:
                information["gender"] = "男"
            information ["user_name"]= result[0][1]
            print(result[0][0])
            self.result = SearchData()
            self.result.set_information(information)
            self.Vhlayout.itemAt(1).widget().deleteLater()
            self.Vhlayout.addWidget(self.result)
        else: 
            QMessageBox.critical(self, 'Wrong', '用户不存在')
            return
    def analyze_data(self):
        self.Vhlayout.itemAt(1).widget().deleteLater()
        days = abs(self.DateEdit1.date().daysTo(self.DateEdit2.date()) )
        temdays = self.DateEdit1.date().daysTo(self.DateEdit2.date())
        if days < 1:
            datatabel,data_title,number = self.get_data_( temdays)
           
            self.view = ChartView(datatabel,data_title,number)
            self.Vhlayout.addWidget(self.view)
        elif days <14 and days >= 1:
            datatabel,data_title ,number=  self.get_data( temdays,1)
            #print(datatabel,data_title,number)
            self.view = ChartView(datatabel,data_title,number)
            self.Vhlayout.addWidget(self.view)

        elif days >=14 and days< 60:
            datatabel,data_title ,number=  self.get_data(int( temdays/7),7)#计算x轴步长
            self.view = ChartView(datatabel,data_title,number)
            self.Vhlayout.addWidget(self.view)
        elif days >= 60 and days< 365:
            datatabel,data_title,number =  self.get_data(int(temdays/30),30)
            self.view = ChartView(datatabel,data_title,number)
            self.Vhlayout.addWidget(self.view)
        elif days >= 365 :
            datatabel,data_title,number =  self.get_data(int (temdays/365),365)
            self.view = ChartView(datatabel,data_title,number)
            self.Vhlayout.addWidget(self.view)  
            pass
    def get_data_(self,days):
    
        self.DateEdit1.date()
        self.test = Database()
        timestr = ["-07","-08","-09","-10","-11","-12","-13","-14","-15","-16","-17","-18","-19","-20","-21","-22","-23"]
        total_data = []
        female_data = []
        male_data = []
        sql_female = "SELECT count(id_number)  FROM student_log_time where log_time between  '{0}'   and '{1}' and gender =0;"
        sql_male = "SELECT count(id_number)  FROM student_log_time where log_time between  '{0}'   and '{1}' and gender =1;"
        sql = "SELECT count(id_number)  FROM student_log_time where log_time \
         between '{0}'  and '{1}';"
        if days >=0:
            for i in timestr:
                reuslt = self.test.c.execute(sql.format(self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i,self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i)).fetchall()
                total_data.append(reuslt[0][0])
                reuslt = self.test.c.execute(sql_female.format(self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i,self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i)).fetchall()
                female_data.append(reuslt[0][0])
                reuslt = self.test.c.execute(sql_male.format(self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i,self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i)).fetchall()
                male_data.append(reuslt[0][0])
        else: 
             for i in timestr:
                result = self.test.c.execute(sql.format(self.DateEdit2.date().toPyDate().strftime("%Y-%m-%d")+i,self.DateEdit2.date().toPyDate().strftime("%Y-%m-%d")+i)).fetchall()
                total_data.append(result[0][0])
      
        category1 = ["总数"]    
        category2 = ["女性"]  
        category3 = ["男性"]      
        datatabel = []
        category1.append(total_data )
        category2.append(female_data )
        category3.append(male_data )
        datatabel.append(category1)
        datatabel.append(category2)
        datatabel.append(category3)
        print(datatabel)
        data_title = [] 
        if days >=0 :
            for i in timestr:
               data_title.append(i+"时")
        else:
            for i in timestr:
                data_title.append(i+"时")
        temdata = copy.deepcopy(total_data )
        temdata.sort(reverse=True)    
        return datatabel,data_title ,temdata[0]

    def get_data(self,days,step):
        self.DateEdit1.date()
        self.test = Database()
        total_data = []
        female_data = []
        male_data = []
        sql_female = "SELECT count(id_number)  FROM student_log_time where log_time between  '{0}'   and '{1}' and gender =0;"
        sql_male = "SELECT count(id_number)  FROM student_log_time where log_time between  '{0}'   and '{1}' and gender =1;"
        sql = "SELECT count(id_number)  FROM student_log_time where log_time \
         between '{0}'  and '{1}';"
        if days >=0:
            step_= 0
            for k in range(abs(days)+1):   
                    result = self.test.c.execute(sql.format(self.DateEdit1.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit1.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    total_data .append(result[0][0])
                    result = self.test.c.execute(sql_female.format(self.DateEdit1.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit1.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    female_data .append(result[0][0])
                    result = self.test.c.execute(sql_male.format(self.DateEdit1.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit1.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    male_data .append(result[0][0])
                    step_ = step+step_

        else: 
            step_= 0
            for k in range(abs(days)+1):   
                    result = self.test.c.execute(sql.format(self.DateEdit2.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit2.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    total_data .append(result[0][0])
                    result = self.test.c.execute(sql_female.format(self.DateEdit2.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit2.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    female_data .append(result[0][0])
                    result = self.test.c.execute(sql_male.format(self.DateEdit2.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit2.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    male_data .append(result[0][0])
                    step_ = step+step_
  
        category1 = ["总数"]    
        category2 = ["女性"]  
        category3 = ["男性"]      
        datatabel = []
        category1.append(total_data )
        category2.append(female_data )
        category3.append(male_data )
        datatabel.append(category1)
        datatabel.append(category2)
        datatabel.append(category3)
        data_title = [] 
        if days >=0 :
            step_ = step
            data_title.append(self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d"))
            for i in range(days):
               data_title.append(self.DateEdit1.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"))
               step_ = step_+step
        else:
            step_ = step
            data_title.append(self.DateEdit2.date().toPyDate().strftime("%Y-%m-%d"))
            for i in range(abs(days)):
               data_title.append(self.DateEdit2.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"))
               step_ = step_+step
        print(total_data )
        print(data_title)
        temdata = copy.deepcopy(total_data)
        temdata.sort(reverse=True)    
        return datatabel,data_title ,temdata[0]