from .Creatuser import CreatStudentUser
from .GlobalVariable import database
from .ShowUser import ShowStudentUser
from PyQt5.QtCore import QDate, Qt
import copy
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit,\
    QGroupBox, QPushButton, QFileDialog, QDateEdit, QMessageBox, QMenu, QProgressBar, QProgressDialog
from .LineStack import ChartView
from .Plugins import Plugins


class ShowData(QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(300, 300,480, 600)
        self.setWindowTitle('数据')
        self.setWindowIcon(QIcon('resources/数据.svg'))
        self.setWindowModality(Qt.ApplicationModal)
        self.Hlayout = QHBoxLayout()
        self.Vhlayout = QVBoxLayout()
        self.linnedit = QLineEdit()
        # self.linnedit.setFixedSize(400,15)
        self.linnedit.setMaximumSize(200, 20)
        self.linnedit.setPlaceholderText('输入学号或姓名')
        self.grou = QGroupBox(self)
        self.label_tip = QLabel()
        self.btn_analyzeData = QPushButton("分析")
        self.btn_analyzeData = QPushButton(objectName="GreenButton")
        self.btn_analyzeData.setIcon(QIcon("resources/分析.svg"))
        self.btn_Search = QPushButton()
        self.btn_Search = QPushButton(objectName="GreenButton")
        self.btn_Search.setIcon(QIcon("resources/搜索.svg"))

        self.btn_analyzeData.setText("分析")
        self.btn_Search.setText("查询")
        self.label_tip.setText("时间范围：")
        self.btn_brow = QPushButton()
        self.btn_brow = QPushButton(objectName="GreenButton")
        self.btn_brow.setText("浏览")
        self.btn_brow.setIcon(QIcon("resources/浏览.svg"))
        self.btn_create_user = QPushButton()
        self.btn_create_user = QPushButton(objectName="GreenButton")
        self.btn_create_user.setIcon(QIcon("resources/文件.svg"))
        self.btn_create_user.setText("批量创建用户")
        self.btn_plugin = QPushButton()
        self.btn_plugin = QPushButton(objectName="GreenButton")
        self.btn_plugin.setText("插件")
        self.btn_plugin.setIcon(QIcon("resources/插件.svg"))

        # self.grou.setFixedSize(self.width(), 40)
        # self.grou.move(0,0)
        self.DateEdit1 = QDateEdit(QDate.currentDate(), self)
        self.DateEdit2 = QDateEdit(QDate.currentDate())
        self.DateEdit1.setDisplayFormat("yyyy-MM-dd")  # 设置格式
        self.DateEdit2.setDisplayFormat("HH")  # 设置格式
        self.DateEdit1.setMinimumDate(
            QDate.currentDate().addDays(-365))  # 设置最小日期
        self.DateEdit1.setMaximumDate(
            QDate.currentDate().addDays(365))  # 设置最大日期
        self.DateEdit1.setCalendarPopup(True)  # 弹出日历
        self.DateEdit2.setCalendarPopup(True)
        self.Hlayout.addWidget(self.label_tip)
        self.Hlayout.addWidget(self.DateEdit1)
        self.Hlayout.addWidget(self.DateEdit2)
        self.Hlayout.addWidget(self.btn_analyzeData)
        self.Hlayout.addSpacing(10)
        # self.Hlayout.addWidget(self.label)
        self.Hlayout.addWidget(self.linnedit)
        self.Hlayout.addWidget(self.btn_Search)
        self.Hlayout.addWidget(self.btn_brow)
        self.Hlayout.addWidget(self.btn_create_user)
        self.Hlayout.addWidget(self.btn_plugin)
        self.grou.setLayout(self.Hlayout)
        self.Vhlayout.addWidget(self.grou)

        self.grou.setMaximumSize(1000, 40)

        self.setLayout(self.Vhlayout)
        self.btn_analyzeData.clicked.connect(self.analyzeData)
        self.btn_Search.clicked.connect(self.showSearchResult)
        self.btn_brow.clicked.connect(self.browse)
        self.btn_create_user.clicked.connect(self.creatStudentUser)
        self.btn_plugin.clicked.connect(
            lambda: self.posMenu(self.btn_plugin.pos()))
        self.qlabel_ = QLabel(self)
        # self.Vhlayout.addWidget(self.view)
        self.resize(720, 600)
        self.Vhlayout.addWidget(self.qlabel_)

    # def resizeEvent(self, event):
    #     super(ChartView, self).resizeEvent(event)
    #     self.grou.resize(self.width,40)

    # 插件菜单
    def posMenu(self, pos):  # pos是按钮坐标
        path = os.path.abspath("./src/plugins")  # 获取绝对路径
        controls_class = Plugins(path).load_plugins()
        pop_menu = QMenu()
        for label, clazz in controls_class.items():
            pop_menu.addAction(label)
        action = pop_menu.exec_(self.mapToGlobal(pos))
        if action:
            item = self.Vhlayout.itemAt(1)
            self.Vhlayout.removeItem(item)
            item.widget().deleteLater()
            self.Vhlayout.addWidget(controls_class[action.text()](self))

    def creatStudentUser(self):  # 批量创建用户
        path, _ = QFileDialog.getOpenFileName(self, "选择文件", "c:\\",
                                              "files(*.xlsx )")
        if path == '':
            return

        self.ProgressBar = QtBoxStyleProgressBar()

        item = self.Vhlayout.itemAt(1)
        self.Vhlayout.removeItem(item)
        item.widget().deleteLater()
        QApplication.processEvents()

        self.Vhlayout.addWidget(self.ProgressBar)
        qlabel_ = QLabel()
        self.Vhlayout.addWidget(qlabel_)
        QApplication.processEvents()

        creat_student_user = CreatStudentUser()
        creat_student_user.sig_end.connect(self.showEerror)
        creat_student_user.sig_progress.connect(self.ProgressBar.setValue)
        QApplication.processEvents()
        self.setEnabled(False)
        list_error = creat_student_user.creatUser(path)
        self.setEnabled(True)

    def showEerror(self, list_error):
        item = self.Vhlayout.itemAt(1)
        self.Vhlayout.removeItem(item)
        item.widget().deleteLater()
        if len(list_error) == 0:
            QMessageBox.information(self, 'Information',
                                    'Register Successfully')
            return

        error_string = ""
        for i in list_error:
            error_string = error_string + i + "\n"

        QMessageBox.information(self, 'Information', error_string)

    # 显示搜索结果

    def showSearchResult(self):
        if not self.linnedit.text():
            QMessageBox.critical(self, '警告', '请输入内容')
            self.linnedit.clear()
            return
        search_content = self.linnedit.text()
        result = None
        if search_content.isdigit():
            database.c.execute(
                "select id_number,user_name,gender,password from student where id_number = {}".format(search_content))
            result = database.c.fetchall()
            if len(result) == 0:
                QMessageBox.critical(self, '警告', '用户不存在')
                self.linnedit.clear()
                return
        else:
            database.c.execute(
                "select id_number,user_name,gender,password from student where user_name like '%{}%'".format(search_content))
            result = database.c.fetchall()
            if len(result) == 0:
                QMessageBox.critical(self, '警告', '用户不存在')
                self.linnedit.clear()
                return

        result = ShowStudentUser(['学号', '姓名', '性别', '密码', "图片"],
                                 "student", ["id_number", "user_name", "gender", "password"], result)
        item = self.Vhlayout.itemAt(1)
        self.Vhlayout.removeItem(item)
        item.widget().deleteLater()
        self.Vhlayout.addWidget(result)
        self.linnedit.clear()
        return

    # 浏览所有用户
    def browse(self):

        result = ShowStudentUser(['学号', '姓名', '性别', '密码', "图片"],
                                 "student", ["id_number", "user_name", "gender", "password"])
        item = self.Vhlayout.itemAt(1)
        self.Vhlayout.removeItem(item)
        item.widget().deleteLater()

        self.Vhlayout.addWidget(result)
        QApplication.processEvents()
        return

    def analyzeData(self):
        # 根据输入时间范围决定X轴刻度间隔
        item = self.Vhlayout.itemAt(1)
        self.Vhlayout.removeItem(item)
        item.widget().deleteLater()
        if self.DateEdit1.date().daysTo(self.DateEdit2.date()) < 0:
            self.time1 = self.DateEdit2
            self.time2 = self.DateEdit1
        else:
            self.time1 = self.DateEdit1
            self.time2 = self.DateEdit2

        days = abs(self.DateEdit1.date().daysTo(self.DateEdit2.date()))
        temdays = abs(self.DateEdit1.date().daysTo(self.DateEdit2.date()))
        if days < 1:
            datatabel, data_title, number = self.getData_()

            self.view = ChartView(datatabel, data_title, number)
            self.Vhlayout.addWidget(self.view)
        elif days < 14 and days >= 1:
            datatabel, data_title, number = self.getData(temdays, 1)
            # print(datatabel,data_title,number)
            self.view = ChartView(datatabel, data_title, number)
            self.Vhlayout.addWidget(self.view)

        elif days >= 14 and days < 60:
            datatabel, data_title, number = self.getData(
                int(temdays/7), 7)  # 计算x轴步长
            self.view = ChartView(datatabel, data_title, number)
            self.Vhlayout.addWidget(self.view)
        elif days >= 60 and days < 365:
            datatabel, data_title, number = self.getData(int(temdays/30), 30)
            self.view = ChartView(datatabel, data_title, number)
            self.Vhlayout.addWidget(self.view)
        elif days >= 365:
            datatabel, data_title, number = self.getData(int(temdays/365), 365)
            self.view = ChartView(datatabel, data_title, number)
            self.Vhlayout.addWidget(self.view)

    def getData_(self):

        timestr = ["-07", "-08", "-09", "-10", "-11", "-12", "-13", "-14",
                   "-15", "-16", "-17", "-18", "-19", "-20", "-21", "-22", "-23"]
        total_data = []
        female_data = []
        male_data = []
        # sql_female = "SELECT count(id_number)  FROM student_log_time where log_time between  '{0}'   and '{1}' and gender =0;"
        # sql_male = "SELECT count(id_number)  FROM student_log_time where log_time between  '{0}'   and '{1}' and gender =1;"
        # sql = "SELECT count(id_number)  FROM student_log_time where log_time \
        #  between '{0}'  and '{1}';"
        sql = "SELECT log_time ,gender FROM student_log_time   where log_time between  '{0}'   and '{1}' ;"

        "" .format(self.DateEdit1.date().toPyDate().strftime(
            "%Y-%m-%d"), (self.DateEdit1.date().addDays(1).toPyDate()).strftime("%Y-%m-%d"))

        database.c.execute(sql.format(self.DateEdit1.date().toPyDate().strftime(
            "%Y-%m-%d"), (self.DateEdit1.date().addDays(1).toPyDate()).strftime("%Y-%m-%d")))
        reuslt = database.c.fetchall()

        for time in timestr:
            total_data.append(
                len([i for i in reuslt if i['log_time'].strftime("%Y-%m-%d-%H")[-3:] == time]))
            female_data.append(len([i for i in reuslt if i['log_time'].strftime(
                "%Y-%m-%d-%H")[-3:] == time and i["gender"] == '女']))
            male_data.append(len([i for i in reuslt if i['log_time'].strftime(
                "%Y-%m-%d-%H")[-3:] == time and i["gender"] == '男']))

        category1 = ["总数"]
        category2 = ["女性"]
        category3 = ["男性"]
        datatabel = []
        category1.append(total_data)
        category2.append(female_data)
        category3.append(male_data)
        datatabel.append(category1)
        datatabel.append(category2)
        datatabel.append(category3)

        data_title = [i+"时" for i in timestr]

        temdata = copy.deepcopy(total_data)
        temdata.sort(reverse=True)
        return datatabel, data_title, temdata[0]

    def getData(self, days, step):
        self.DateEdit1.date()

        total_data = []
        female_data = []
        male_data = []
        sql = "SELECT log_time ,gender FROM student_log_time   where log_time between  '{0}'   and '{1}' ;"

        result = database.c.execute(sql.format(self.time1.date().toPyDate().strftime(
            "%Y-%m-%d"), self.time2.date().addDays(1).toPyDate().strftime("%Y-%m-%d")))
        result = database.c.fetchall()

        result1 = [i for i in result if abs(
            (i["log_time"].date() - self.time1.date().toPyDate()).days) < step]
        count1 = len(result1)
        total_data .append(count1)
        count2 = len([i for i in result1 if i['gender'] == '女'])
        female_data .append(count2)
        count3 = len([i for i in result1 if i['gender'] == '男'])
        male_data .append(count3)

        result = [i for i in result if i not in result1]

        step_ = 0
        for i in range(days):
            result1 = [i for i in result if abs((i["log_time"].date(
            ) - self.time1.date().addDays(step_ + step).toPyDate()).days) < step]
            count1 = len(result1)
            total_data .append(count1)
            count2 = len([i for i in result1 if  i['gender'] == '女'])

            female_data .append(count2)
            count3 = len([i for i in result1 if  i['gender'] == '男'])
            male_data .append(count3)

            step_ = step + step_
            result = [i for i in result if i not in result1]

        category1 = ["总数"]
        category2 = ["女性"]
        category3 = ["男性"]
        datatabel = []
        category1.append(total_data)
        category2.append(female_data)
        category3.append(male_data)
        datatabel.append(category1)
        datatabel.append(category2)
        datatabel.append(category3)
        data_title = []

        step_ = step
        data_title.append(self.time1.date().toPyDate().strftime("%Y-%m-%d"))
        for i in range(abs(days)):
            data_title.append(self.time1.date().addDays(
                step_).toPyDate().strftime("%Y-%m-%d"))
            step_ = step_+step

        temdata = copy.deepcopy(total_data)
        temdata.sort(reverse=True)

        return datatabel, data_title, temdata[0]


class QtBoxStyleProgressBar(QProgressBar):
    def __init__(self):
        super(QtBoxStyleProgressBar, self).__init__()
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowModality(Qt.WindowModal)
        self.setRange(0, 100)
        self.setValue(0)
        self.setStyleSheet("""
        QProgressBar::chunk
            {
                border-radius:5px;
                background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 #01FAFF,stop:1  #26B4FF);
            }
            QProgressBar
            {
                height:22px;
                text-align:center;/*文本位置*/
                font-size:14px;
                color:white;
                border-radius:5px;
                background: #1D5573 ;
            }
       

        """)

    def setValue(self, value: int) -> None:
        self.setFormat("加载中请勿关闭窗口，loading {}%.....".format(value))
        super().setValue(value)
        return
