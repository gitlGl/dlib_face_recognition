from . import CreatUser
from .Database import database,PH
from .ShowUser import ShowUser
from PySide6.QtCore import QDate, Qt,QTimer
import copy,multiprocessing
import os,xlrd
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit,\
    QGroupBox, QPushButton, QFileDialog, QDateEdit, QMessageBox, QMenu, QProgressBar,QApplication
from .LineStack import ChartView
from .Plugins import Plugins
from . import Setting
from .Setting import type_database
from . CreatUser import run,insertImg
import gc
from .Setting import resources_dir,base_dir
class ShowData(QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(300, 300,480, 600)
        self.setWindowTitle('数据')
        self.setWindowIcon(QIcon(resources_dir + '数据.svg'))
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
        self.btn_analyzeData.setIcon(QIcon(resources_dir + "分析.svg"))
        self.btn_Search = QPushButton()
        self.btn_Search = QPushButton(objectName="GreenButton") # type: ignore
        self.btn_Search.setIcon(QIcon(resources_dir + "搜索.svg"))

        self.btn_analyzeData.setText("分析")
        self.btn_Search.setText("查询")
        self.label_tip.setText("时间范围：")
        self.btn_brow = QPushButton()
        self.btn_brow = QPushButton(objectName="GreenButton") # type: ignore
        self.btn_brow.setText("浏览")
        self.btn_brow.setIcon(QIcon(resources_dir + "浏览.svg"))
        self.btn_create_user = QPushButton()
        self.btn_create_user = QPushButton(objectName="GreenButton")
        self.btn_create_user.setIcon(QIcon(resources_dir + "文件.svg"))
        self.btn_create_user.setText("批量创建用户")
        self.btn_plugin = QPushButton()
        self.btn_plugin = QPushButton(objectName="GreenButton")
        self.btn_plugin.setText("插件")
        self.btn_plugin.setIcon(QIcon(resources_dir + "插件.svg"))

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
        self.btn_create_user.clicked.connect(self.buttonCreate)
        self.btn_plugin.clicked.connect(
            lambda: self.posMenu(self.btn_plugin.pos()))
        self.qlabel_ = QLabel(self)
        # self.Vhlayout.addWidget(self.view)
        self.resize(720, 600)
        self.Vhlayout.addWidget(self.qlabel_)

   

    # 插件菜单
    def posMenu(self, pos):  # pos是按钮坐标
        controls_class = Plugins().load_plugins()
        pop_menu = QMenu()
        for label, clazz in controls_class.items():
            pop_menu.addAction(label)
        action = pop_menu.exec_(self.mapToGlobal(pos))
        if action:
            item = self.Vhlayout.itemAt(1)
            item.widget().deleteLater()
            self.Vhlayout.removeItem(item)
            self.Vhlayout.addWidget(controls_class[action.text()](self))


    
    
    def refreshProgressBar(self):
        for  index,result in enumerate(self.results[:]):
            if index == Setting.processes:
                return
            if not result.ready():
                continue 
            item = result.get()
            self.results.remove(result)
          
            self.nrow = self.nrow + item[0]
            self.list_problem.extend(item[1])

            self.ProgressBar.setValue(int(self.nrow/self.user_sheet.nrows*100))
            QApplication.processEvents()
            
            if self.nrow == self.user_sheet.nrows-1:
                self.lock = None
                self.timer.stop()
                self.setEnabled(True)
                self.showEerror(self.list_problem)
                self.list_problem = None
                self.results = None
                self.pool = None
                gc.collect()
      
            
    def buttonCreate(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择文件", "c:\\",
                                              "files(*.xlsx )")
        if path == '':
            return
        book = xlrd.open_workbook(path)
        try:
            self.user_sheet = book.sheet_by_name('user')
        except:
            QMessageBox.warning(self, '提示', 'Excel 文件中没有名为 "user" 的 sheet')
            return
        if self.user_sheet.nrows < Setting.count_max:#如果数据量小于30条，就不用多进程了,魔术数字
            self.creatUser(self.user_sheet)
        else:
            self.creatUserMultiprocessing()
            
    def creatUserMultiprocessing(self):
        self.creatProgressBar()
        self.setEnabled(False)

        data = [self.user_sheet.row_values(i) for i in range(1, self.user_sheet.nrows)]
        group_count = Setting.group_count

        lenth = len(data)   
        total_group = lenth // group_count
        self.results = []

        self.pool =  multiprocessing.Pool(Setting.processes)
        self.lock = None 
        if type_database == 'sqlite3':
            self.lock = multiprocessing.Manager().Lock()
            
        for  num in range(total_group):
            result = self.pool.apply_async(run,args =(num,
                                data[num* group_count:(num+1)*group_count],self.lock) )
            self.results.append(result)
        result = self.pool.apply_async(run,args = (total_group,data[total_group*(group_count):],
                                                        self.lock))
        self.results.append(result)
       
        self.pool.close()
    
        self.timer = QTimer()
        self.nrow = 0
        self.list_problem = []
        self.timer.timeout.connect(self.refreshProgressBar)
        self.timer.start(100)
        
    def creatProgressBar(self):  # 创建进度条
        self.ProgressBar = QtBoxStyleProgressBar()
        item = self.Vhlayout.itemAt(1)
        item.widget().deleteLater()
        self.Vhlayout.removeItem(item)
        QApplication.processEvents()

        self.Vhlayout.addWidget(self.ProgressBar)
        qlabel_ = QLabel()
        self.Vhlayout.addWidget(qlabel_)
        QApplication.processEvents()

    def creatUser(self,user_sheet):  # 批量创建用户
        self.creatProgressBar()
        self.setEnabled(False)
        list_problem = []
        rows = user_sheet.nrows
       
        for row in range(1, rows):
            QApplication.processEvents()
            self.ProgressBar.setValue(int(row/rows*100)) 
            row_user_data = user_sheet.row_values(rowx=row)
            dic_data = CreatUser.checkInsert(row+1,row_user_data,list_problem)
            if dic_data is not None:
                img_path = dic_data.pop('img_path')
                
                database.execute(
                    f"INSERT INTO student (id_number,user_name,gender,password ,salt,vector) \
            VALUES ({PH},{PH}, {PH}, {PH} , {PH},{PH})",tuple(dic_data.values()))

                    
                insertImg(dic_data['id_number'],img_path,'student')
           
        self.ProgressBar.setValue(100)
        self.showEerror(list_problem)
        QApplication.processEvents()
        self.setEnabled(True)

    def showEerror(self, list_error):
       
        item = self.Vhlayout.itemAt(1)
        item.widget().deleteLater()
        self.Vhlayout.removeItem(item)
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
            result =  database.execute(
                "select id_number,user_name,gender,password from student where id_number = {0}".format(search_content))
            
            if len(result) == 0:
                QMessageBox.critical(self, '警告', '用户不存在')
                self.linnedit.clear()
                return
        else:
            result = database.execute(
                "select id_number,user_name,gender,password from student where user_name like '%{0}%'".format(search_content))
           
            if len(result) == 0:
                QMessageBox.critical(self, '警告', '用户不存在')
                self.linnedit.clear()
                return

        result = ShowUser("student", result)
        item = self.Vhlayout.itemAt(1)
        item.widget().deleteLater()
        self.Vhlayout.removeItem(item)
        self.Vhlayout.addWidget(result)
        self.linnedit.clear()
        return

    # 浏览所有用户
    def browse(self):

        result = ShowUser("student")
        item = self.Vhlayout.itemAt(1)
        item.widget().deleteLater()
        self.Vhlayout.removeItem(item)
        self.Vhlayout.addWidget(result)
        QApplication.processEvents()
        return

    def analyzeData(self):
        # 根据输入时间范围决定X轴刻度间隔
        item = self.Vhlayout.itemAt(1)
        item.widget().deleteLater()
        self.Vhlayout.removeItem(item)
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
       
        sql = "SELECT log_time ,gender FROM student_log_time   where log_time between  '{0}'   and '{1}' ;"

        reuslt = database.execute(sql.format(self.DateEdit1.date().toPython().strftime(
            "%Y-%m-%d"), (self.DateEdit1.date().addDays(1).toPython()).strftime("%Y-%m-%d")))
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

        result = database.execute(sql.format(self.time1.date().toPython().strftime(
            "%Y-%m-%d"), self.time2.date().addDays(1).toPython().strftime("%Y-%m-%d")))
       
        result1 = [i for i in result if abs(
            (i["log_time"].date() - self.time1.date().toPython()).days) < step]
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
            ) - self.time1.date().addDays(step_ + step).toPython()).days) < step]
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
        data_title.append(self.time1.date().toPython().strftime("%Y-%m-%d"))
        for i in range(abs(days)):
            data_title.append(self.time1.date().addDays(
                step_).toPython().strftime("%Y-%m-%d"))
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
        self.setObjectName("QProgressBar1")
        
    def setValue(self, value: int) -> None:
        self.setFormat("加载中请勿关闭窗口，loading {}%.....".format(value))
        super().setValue(value)
        return
    
#利用管道通信实现进程池例子    
# class Worker:
#     group_conut = 10
#     def __init__(self, task_queue, result_queue):
#         self.task_queue = task_queue
#         self.result_queue = result_queue
    
#     def run(self):
#         while True:
#             # 从任务队列中获取任务
#             data_dict = self.task_queue.get()
                         
#             if data_dict is None:
#                 # 如果获取到的任务为 None，表示任务已经完成，退出循环
#                 break
            
#             list_problem = []
#             for key,item in data_dict.items():
#                 for index,data in enumerate(item):
#                     if key == 0 and index == 0:
#                         CreatUser.checkInsert(1,data,list_problem)
#                     else :
#                         CreatUser.checkInsert(key*group_count+index,data,list_problem)
#                 self.result_queue.put([len(item),list_problem])
# class ProcessPool:
#     def __init__(self, num_processes):
#         self.num_processes = num_processes
#         self.task_queue = multiprocessing.Queue()
#         self.result_queue = multiprocessing.Queue()
#         self.workers = []
    
#     def start(self):
#         # 创建多个进程并启动
#         for i in range(self.num_processes):
#             worker = Worker(self.task_queue, self.result_queue)
#             process = multiprocessing.Process(target=worker.run)
#             process.start()
#             self.workers.append((worker, process))
    
#     def stop(self):
#         # 向任务队列中添加 None，表示任务已经完成
#         for i in range(self.num_processes):
#             self.task_queue.put(None)
    
#     def submit(self, task):
#         # 向任务队列中添加任务
#         self.task_queue.put(task)
    
#     def get_result(self):
#         # 从结果队列中获取结果
#         if self.result_queue.empty():
#             return None
#         return self.result_queue.get()