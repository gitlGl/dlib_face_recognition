#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

class ToolTipItem(QWidget):

    def __init__(self, color, text, parent=None):
        super(ToolTipItem, self).__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        clabel = QLabel(self)
        clabel.setMinimumSize(12, 12)
        clabel.setMaximumSize(12, 12)
        clabel.setStyleSheet("border-radius:6px;background: rgba(%s,%s,%s,%s);" % (
            color.red(), color.green(), color.blue(), color.alpha()))
        layout.addWidget(clabel)
        self.textLabel = QLabel(text, self, styleSheet="color:white;")
        layout.addWidget(self.textLabel)

    def setText(self, text):
        self.textLabel.setText(text)


class ToolTipWidget(QWidget):
    Cache = {}

    def __init__(self, *args, **kwargs):
        super(ToolTipWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            "ToolTipWidget{background: rgba(50, 50, 50, 100);}")
        layout = QVBoxLayout(self)
        self.titleLabel = QLabel(self, styleSheet="color:white;")
        layout.addWidget(self.titleLabel)

    def updateUi(self, title, points):
        self.titleLabel.setText(title)
        for serie, point in points:
            if serie not in self.Cache:
                item = ToolTipItem(
                    serie.color(),
                    (serie.name() or "-") + ":" + str(point.y()), self)
                self.layout().addWidget(item)
                self.Cache[serie] = item
            else:
                self.Cache[serie].setText(
                    (serie.name() or "-") + ":" + str(point.y()))
            self.Cache[serie].setVisible(serie.isVisible())  # 隐藏那些不可用的项
        self.adjustSize()  # 调整大小


class GraphicsProxyWidget(QGraphicsProxyWidget):

    def __init__(self, *args, **kwargs):
        super(GraphicsProxyWidget, self).__init__(*args, **kwargs)
        self.setZValue(999)
        self.tipWidget = ToolTipWidget()
        self.setWidget(self.tipWidget)
        self.hide()

    def width(self):
        return self.size().width()

    def height(self):
        return self.size().height()

    def show(self, title, points, pos):
        self.setGeometry(QRectF(pos, self.size()))
        self.tipWidget.updateUi(title, points)
        super(GraphicsProxyWidget, self).show()


class ChartView(QChartView):

    def __init__(self, datatabel,category, number):
        super(ChartView, self).__init__()
        self.number = number
        self.datatabel = datatabel
        self.category = category
        self.resize(800, 600)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        # 自定义x轴label
        #self.category = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]#使用参数变更
        
        self.initChart()

        # 提示widget
        self.toolTipWidget = GraphicsProxyWidget(self._chart)

        # line
        self.lineItem = QGraphicsLineItem(self._chart)
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        self.lineItem.setPen(pen)
        self.lineItem.setZValue(998)
        self.lineItem.hide()

        # 一些固定计算，减少mouseMoveEvent中的计算量
        # 获取x和y轴的最小最大值
        axisX, axisY = self._chart.axisX(), self._chart.axisY()
        self.min_x, self.max_x = axisX.min(), axisX.max()
        self.min_y, self.max_y = axisY.min(), axisY.max()

    def resizeEvent(self, event):
        super(ChartView, self).resizeEvent(event)
        
        # 当窗口大小改变时需要重新计算
        # 坐标系中左上角顶点
        self.point_top = self._chart.mapToPosition(
            QPointF(self.min_x, self.max_y))
        # 坐标原点坐标
        self.point_bottom = self._chart.mapToPosition(
            QPointF(self.min_x, self.min_y))
        self.step_x = (self.max_x - self.min_x) / \
                      (self._chart.axisX().tickCount() - 1)

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        pos = event.pos()
        # 把鼠标位置所在点转换为对应的xy值
        x = self._chart.mapToValue(pos).x()
        y = self._chart.mapToValue(pos).y()
        index = round((x - self.min_x) / self.step_x)#通过步长与x坐标获得索引
        # 得到在坐标系中的所有正常显示的series的类型和点
        points = [(serie, serie.at(index))
                  for serie in self._chart.series()
                  if self.min_x <= x <= self.max_x and
                  self.min_y <= y <= self.max_y]
        if points:
            pos_x = self._chart.mapToPosition(
                QPointF(index * self.step_x + self.min_x, self.min_y))
            self.lineItem.setLine(pos_x.x(), self.point_top.y(),
                                  pos_x.x(), self.point_bottom.y())
            self.lineItem.show()
            try:
                title = self.category[index]
            except:
                title = ""
            t_width = self.toolTipWidget.width()
            t_height = self.toolTipWidget.height()
            # 如果鼠标位置离右侧的距离小于tip宽度
            x = pos.x() - t_width if self.width() - \
                                     pos.x() - 20 < t_width else pos.x()
            # 如果鼠标位置离底部的高度小于tip高度
            y = pos.y() - t_height if self.height() - \
                                      pos.y() - 20 < t_height else pos.y()
            self.toolTipWidget.show(
                title, points, QPoint(x, y))
        else:
            self.toolTipWidget.hide()
            self.lineItem.hide()

    def handleMarkerClicked(self):#重写鼠标事件，显示信息
        marker = self.sender()  # 信号发送者
        if not marker:
            return
        visible = not marker.series().isVisible()
        #         # 隐藏或显示series
        marker.series().setVisible(visible)
        marker.setVisible(True)  # 要保证marker一直显示
        # 透明度
        alpha = 1.0 if visible else 0.4
        # 设置label的透明度
        brush = marker.labelBrush()
        color = brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setLabelBrush(brush)
        # 设置marker的透明度
        brush = marker.brush()
        color = brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setBrush(brush)
        # 设置画笔透明度
        pen = marker.pen()
        color = pen.color()
        color.setAlphaF(alpha)
        pen.setColor(color)
        marker.setPen(pen)

    def handleMarkerHovered(self, status):
        # 设置series的画笔宽度
        marker = self.sender()  # 信号发送者
        if not marker:
            return
        series = marker.series()
        if not series:
            return
        pen = series.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        series.setPen(pen)

    def handleSeriesHoverd(self, point, state):
        # 设置series的画笔宽度
        series = self.sender()  # 信号发送者
        pen = series.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if state else -1))
        series.setPen(pen)

    def initChart(self):
        self._chart = QChart(title="折线图分析")
        self._chart.setAcceptHoverEvents(True)
     
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
      
        for series_name, data_list in self.datatabel:
            series = QLineSeries(self._chart)
            for j, v in enumerate(data_list):
                series.append(j, v)
            series.setName(series_name)
            series.setPointsVisible(True)  # 显示圆点
            series.hovered.connect(self.handleSeriesHoverd)  # 鼠标悬停
            self._chart.addSeries(series)
        self._chart.createDefaultAxes()  # 创建默认的轴
        axisX = self._chart.axisX()  # x轴
        axisX.setTickCount(len(self.category))  # x轴设置7个刻度,使用参数变更
        axisX.setGridLineVisible(False)  # 隐藏从x轴往上的线条
        axisY = self._chart.axisY()
        #Y轴刻度间隔与刻度范围随着输入数据量动态变化
        tick = [5,10,20,30,40,50,60,70,80,100,110,120,130,140,150]#刻度间隔
        #刻度范围不能太低
        if self.number<=10:
                axisY.setTickCount(11)#刻度个数
                axisY.setRange(0,10)#刻度范围
        else:
            for i in tick:
                if int(self.number/i) <= 20:#刻度个数不大于20
                    k = i-self.number%i
                    axisY.setTickCount((self.number+k)/i+1)#刻度个数
                    axisY.setRange(0,self.number+k)#刻度范围
                    #print(self.number+k)
                    break
              
                    
        # 自定义x轴
        axis_x = QCategoryAxis(
            self._chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)#设置文字标示位置
        axis_x.setTickCount(len(self.category))
        axis_x.setGridLineVisible(False)
        min_x = axisX.min()
        max_x = axisX.max()
        step = (max_x - min_x) / (len(self.category) -1)  # 7个tick
        for h in range(0,len(self.category)):
            #print("测试",i)
            axis_x.append(self.category[h], min_x + h * step)#刻度位置
        self._chart.setAxisX(axis_x, self._chart.series()[-1])
        # chart的图例
        legend = self._chart.legend()
        # 设置图例由Series来决定样式
        legend.setMarkerShape(QLegend.MarkerShapeFromSeries)
        # 遍历图例上的标记并绑定信号
        for marker in legend.markers():
            # 点击事件
            marker.clicked.connect(self.handleMarkerClicked)#鼠标点击隐藏对应折线
            # 鼠标悬停事件
            marker.hovered.connect(self.handleMarkerHovered)#对应折线显示高亮
        self.setChart(self._chart)
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
