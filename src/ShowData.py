
from src.Creatuser import CreatStudentUser
from src.Database import Database
from src.ShowStudentUser import ShowStudentUser
from PyQt5.QtCore import QDate,Qt
import copy,os 
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit,\
QGroupBox,QPushButton,QFileDialog,QDateEdit,QMessageBox, QMenu
from src.LineStack import ChartView
from src.Plugins import Plugins
class ShowData(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300,400, 380)
        self.setWindowTitle('数据')
        self.setWindowIcon(QIcon('resources/数据.png'))
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
        self.label.setText("")
        self.btn1 = QPushButton("分析")
        self.btn1 = QPushButton(objectName="GreenButton")
        self.btn1.setIcon(QIcon("./resources/分析.png"))
        self.btn2 = QPushButton()
        self.btn2 = QPushButton(objectName="GreenButton")
        self.btn2.setIcon(QIcon("./resources/搜索.png"))
        
        self.btn1.setText("分析")
        self.btn2.setText("查询")
        self.qlabel.setText("时间范围：")
        self.btn3 = QPushButton()
        self.btn3 = QPushButton(objectName="GreenButton")
        self.btn3.setText("浏览")
        self.btn3.setIcon(QIcon("./resources/浏览.png"))
        self.btn4 = QPushButton()
        self.btn4 = QPushButton(objectName="GreenButton")
        self.btn4.setIcon(QIcon("./resources/文件.png"))
        self.btn4.setText("批量创建用户")
        self.btn5 = QPushButton()
        self.btn5 = QPushButton(objectName="GreenButton")
        self.btn5.setText("插件")
        self.btn5.setIcon(QIcon("./resources/插件.png"))
        
        
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
        self.Hlayout.addWidget(self.btn4)
        self.Hlayout.addWidget(self.btn5)
        self.grou.setLayout(self.Hlayout)
        self.Vhlayout.addWidget(self.grou)
        self.grou.setMaximumSize(1000,40)
        self.setLayout(self.Vhlayout)
        self.btn1.clicked.connect(self.analyze_data)
        self.btn2.clicked.connect(self.show_search_result)
        self.btn3.clicked.connect(self.browse)
        self.btn4.clicked.connect(self.creat_student_user)
        self.btn5.clicked.connect(lambda:self.pos_menu(self.btn5.pos()))
        datatabel,data_title ,number=  self.get_data_()
        self.view = ChartView(datatabel,data_title,number)
        self.Vhlayout.addWidget(self.view)
  
    # def resizeEvent(self, event):
    #     super(ChartView, self).resizeEvent(event)
    #     self.grou.resize(self.width,40)

    #插件菜单
    def pos_menu(self,pos):#pos是按钮坐标
        path = os.path.abspath("./src/plugins")#获取绝对路径
        controls_class = Plugins(path).load_plugins()
        pop_menu = QMenu()
        for label,clazz in controls_class.items():
            pop_menu.addAction(label)
        action = pop_menu.exec_(self.mapToGlobal(pos))
        if action:
            self.Vhlayout.itemAt(1).widget().deleteLater()
            self.Vhlayout.addWidget(controls_class[action.text()](self))
        
       
        
    def creat_student_user(self):#批量创建用户
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
    #显示搜索结果
    def show_search_result(self):
        if not self.linnedit.text(): 
             QMessageBox.critical(self, 'Wrong', '请输入学号')
             self.linnedit.clear()
             return 
        id_number = self.linnedit.text()
        if not id_number.isdigit():
            QMessageBox.critical(self, 'Wrong', '学号为数字')
            self.linnedit.clear()
            return
            
        result = Database().c.execute("select id_number,user_name,gender from student where id_number = {}".format(id_number)).fetchall()
        if len(result)!= 0:
           
            self.result = ShowStudentUser(result,[ '学号', '姓名', '性别',"图片" ])
            self.Vhlayout.itemAt(1).widget().deleteLater()
            self.Vhlayout.addWidget(self.result)
        else: 
            QMessageBox.critical(self, 'Wrong', '用户不存在')
            return
    #浏览所有用户
    def browse(self):
        result = Database().c.execute("select id_number,user_name,gender,password from student").fetchall()
        if len(result)!= 0:
           
            self.result = ShowStudentUser(result,[ '学号', '姓名', '性别',"图片" ])
            self.Vhlayout.itemAt(1).widget().deleteLater()
            self.Vhlayout.addWidget(self.result)
        else: 
            QMessageBox.critical(self, 'Wrong', '不存在用户')
            return

            
    def analyze_data(self):
        #根据输入时间范围决定X轴刻度间隔
        self.Vhlayout.itemAt(1).widget().deleteLater()
        days = abs(self.DateEdit1.date().daysTo(self.DateEdit2.date()) )
        temdays = self.DateEdit1.date().daysTo(self.DateEdit2.date())
        if days < 1:
            datatabel,data_title,number = self.get_data_()
           
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
    def get_data_(self):
    
        self.test = Database()
        timestr = ["-07","-08","-09","-10","-11","-12","-13","-14","-15","-16","-17","-18","-19","-20","-21","-22","-23"]
        total_data = []
        female_data = []
        male_data = []
        # sql_female = "SELECT count(id_number)  FROM student_log_time where log_time between  '{0}'   and '{1}' and gender =0;"
        # sql_male = "SELECT count(id_number)  FROM student_log_time where log_time between  '{0}'   and '{1}' and gender =1;"
        # sql = "SELECT count(id_number)  FROM student_log_time where log_time \
        #  between '{0}'  and '{1}';"
        sql_female = "SELECT count(id_number)  FROM student_log_time where log_time like  '{0}%'    and gender =0;"
        sql_male = "SELECT count(id_number)  FROM student_log_time where log_time like  '{0}%'    and gender =1;"
        sql = "SELECT count(id_number)  FROM student_log_time where log_time \
         like '{0}%';"

        for i in timestr:
            reuslt = self.test.c.execute(sql.format(self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i,self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i)).fetchall()
            #print(type(result))
            total_data.append(reuslt[0]['count(id_number)'])
            reuslt = self.test.c.execute(sql_female.format(self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i,self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i)).fetchall()
            female_data.append(reuslt[0]['count(id_number)'])
            reuslt = self.test.c.execute(sql_male.format(self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i,self.DateEdit1.date().toPyDate().strftime("%Y-%m-%d")+i)).fetchall()
            male_data.append(reuslt[0]['count(id_number)'])
    
      
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
       
        
        data_title = [i+"时" for i in timestr]

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
                    total_data .append(result[0]['count(id_number)'])
                    result = self.test.c.execute(sql_female.format(self.DateEdit1.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit1.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    female_data .append(result[0]['count(id_number)'])
                    result = self.test.c.execute(sql_male.format(self.DateEdit1.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit1.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    male_data .append(result[0]['count(id_number)'])
                    step_ = step+step_

        else: 
            step_= 0
            for k in range(abs(days)+1):   
                    result = self.test.c.execute(sql.format(self.DateEdit2.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit2.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    total_data .append(result[0]['count(id_number)'])
                    result = self.test.c.execute(sql_female.format(self.DateEdit2.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit2.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    female_data .append(result[0]['count(id_number)'])
                    result = self.test.c.execute(sql_male.format(self.DateEdit2.date().addDays(step_).toPyDate().strftime("%Y-%m-%d"),self.DateEdit2.date().addDays(step_+step).toPyDate().strftime("%Y-%m-%d"))).fetchall()
                    male_data .append(result[0]['count(id_number)'])
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
        
        temdata = copy.deepcopy(total_data)
        temdata.sort(reverse=True)    
        return datatabel,data_title ,temdata[0]
