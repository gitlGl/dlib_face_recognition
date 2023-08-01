StyleSheet = """
QWidget {
        background: rgb(232, 241, 252);
       
}
 QMenu::item:selected { 
                     background-color:rgb(111, 156, 207);/*选中的样式*/
}

QCalendarWidget QToolButton {
    color: rgb(111, 156, 207);
    
}
/*表格样式*/

QTableWidget
{
    background: rgb(224, 238, 255);
   border:none
}
QTableWidget::item
{
   /* color:rgb(111, 156, 207);*/
    background: rgb(224, 238, 255);
    text-align:center;
}
QTableWidget::item:hover
{
    color:#FFFFFF;
    background: rgb(111, 156, 207);
}
QTableWidget::item:selected
{
    color:#FFFFFF;
    background: rgb(111, 156, 207);
}
QHeaderView::section,QTableCornerButton:section
{ 
    text-align:center;
    padding:3px; 
    margin:0px; 
    color:rgb(51, 51, 51);
    border:1px solid rgb(51, 51, 51);
    border-left-width:0px; 
    border-bottom-width:1px; 
    border-right-width:1px; 
    border-top-width:0px;
  
    background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 rgb(222, 231, 242),stop:1 rgb(222, 231, 242));
 }
QHeaderView::section:selected
{ 
    color:#FFFFFF; 
    border:1px solid rgb(111, 156, 207);
 }
QScrollBar:vertical{ 
    width:8px;  
    border-style:flat;
    border-radius: 4px;
    border:0px;
     background: rgb(232, 241, 252);
} 
QScrollBar::handle:vertical{ 
    background: rgb(232, 241, 252);
    border-radius: 4px;
    width:8px; 
    min-height:91px; 
    border-style:flat;
}
QScrollBar::handle:vertical::hover{ 
    background: rgb(111, 156, 207);
    border-radius: 4px;
    width:8px; 
}
QScrollBar::handle:vertical::pressed{ 
    background: rgb(111, 156, 207);
    border-radius:4px;
    width:8px; 
}

QScrollBar:horizontal{ 
    height:8px;  
    border-style:flat;
    border-radius: 4px;
    border:0px;
background: rgb(232, 241, 252);
} 
QScrollBar::handle:horizontal{ 
    background: rgb(232, 241, 252);
    border-radius: 4px;
    height:8px; 
    min-width:91px; 
    border-style:flat;
}
QScrollBar::handle:horizontal::hover{ 
    background: rgb(111, 156, 207);
    border-radius: 4px;
    height:8px; 
}
QScrollBar::handle:horizontal::pressed{ 
    background: rgb(111, 156, 207);
    border-radius:4px;
    height:8px; 
}



/*这里是通用设置，所有按钮都有效，不过后面的可以覆盖这个*/
QPushButton {
    border: none; /*去掉边框*/
}

/*
QPushButton#xxx
或者
#xx
都表示通过设置的objectName来指定
*/

#GreenButton {
    /*background-color: #4caf50;*/
    border-radius: 5px; /*圆角*/
}
#GreenButton:hover {
    background-color: #81c784;
}
#GreenButton:pressed {
    background-color: #c8e6c9;
}


#GreenButton2:hover {
    background-color: #81c784;
}
#GreenButton2:pressed {
    background-color: #c8e6c9;
}



    #QProgressBar1::chunk
        {
            border-radius:5px;
            background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 #01FAFF,stop:1  #26B4FF);
        }

        #QProgressBar1
        {
            height:22px;
            text-align:center;/*文本位置*/
            font-size:14px;
            color:white;
            border-radius:5px;
            background: #1D5573 ;
        }
       

     

/**********输入框**********/
QLineEdit {
        border-radius: 4px;
        height: 25px;
        border: 1px solid rgb(111, 156, 207);
        background: white;
}
QLineEdit:enabled {
        color: rgb(84, 84, 84);
}
QLineEdit:enabled:hover, QLineEdit:enabled:focus {
        color: rgb(51, 51, 51);
}
QLineEdit:!enabled {
        color: rgb(80, 80, 80);
}

/**********分页样式**********/

           Page {
                border: none;
                 background: rgb(232, 241, 252);
            }

            
            #QLineEdit2{
                width: 15px
               
               

               
            }

QCheckBox{
    spacing: 5px;
}
QCheckBox::indicator {
	width: 15px;
	height: 15px;
}
QCheckBox::indicator:unchecked {
    image: url(resources/checkbox-uncheck.svg);
}
QCheckBox::indicator:unchecked:hover {
    image: url(resources/checkbox-uncheck.svg);
}
QCheckBox::indicator:checked {
    image: url(resources/checkbox.svg);
}

"""

 


# sql2 = "SELECT gender where gender = 1 in (select gender as gender FROM student_log_time where log_time between '2022-03-18'  and '2022-03-19') ;"
# test = Database()
# sql = "select count (gender) FROM student_log_time where log_time between '2022-03-18'  and '2022-03-19' and gender =0;"

# print(test.c.execute(sql).fetchall())
# input() 

#递归删除文件夹以及文件






# import csv
# car = ['car 11',1]
# finish = ['Landhaus , Nord']
# time = ["['05:36']", "['06:06']", "['06:36']", "['07:06']", "['07:36']"]
# try:
#     with open('Informationen.csv', 'w') as myfile:
#         writer = csv.writer(myfile, dialect='excel')
#         bla = [car, finish]
#         for each_time in time:
#             bla.append(each_time)
#         #print(bla)
#         writer.writerow(bla)
# except IOError as ioe:
#     print('Error: ' + str(ioe))


# import csv
 
# filename='Informationen.csv'
# data = []
# with open(filename) as csvfile:
#     csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
#     #header = next(csv_reader)        # 读取第一行每一列的标题
#     for row in csv_reader:            # 将csv 文件中的数据保存到data中
#         data.append(row)
#         print(row,"\n")           # 选择某一列加入到data数组中
#     print(data)
# import dlib,cv2,numpy as np
# from src import models
# raw_data = np.fromfile("./3.jpg", dtype=np.uint8)  #先用numpy把图片文件存入内存：raw_data，把图片数据看做是纯字节数据
# img = cv2.imdecode(raw_data, cv2.IMREAD_COLOR)  #从内存数据读入图片
# cv2.imwrite( "5.jpg",img)
                               
# raw_data = np.fromfile("./6.jpg", dtype=np.uint8)  #先用numpy把图片文件存入内存：raw_data，把图片数据看做是纯字节数据
# rgbImage = cv2.imdecode(raw_data, cv2.IMREAD_COLOR)  #从内存数据读入图片

# dets = models.detector(rgbImage, 0)
# faces = dlib.full_object_detections()
# for detection in dets:
#     faces.append(models.predictor(rgbImage, detection))
# window = dlib.image_window()
# image = dlib.get_face_chip(rgbImage, faces[0])
# cv2.imwrite("./2.jpg" ,image)
  
# window.set_image(image)
# dlib.hit_enter_to_continue()
#   img = rgbImage
#                 location_faces = models.predictor(rgbImage, location_faces[0])
#                 rgbImage = dlib.get_face_chip(rgbImage, location_faces)
#                 rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
#                 result = face_rg.rg(img, rgbImage,  location_faces,share)
# class test():
#     def __init__(self) -> None:
#         self.test = 0
#     pass
# t = test()
# if hasattr(t, "test"):
#     print("ces")