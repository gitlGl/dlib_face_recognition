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
}
QTableWidget::item
{
    color:rgb(111, 156, 207);
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
    border-right-width:1px; 
    border-top-width:0px;
    border-bottom-width:1px; 
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
QPushButton#RedButton {
    background-color: #f44336; /*背景颜色*/
}
#RedButton:hover {
    background-color: #e57373; /*鼠标悬停时背景颜色*/
}
/*注意pressed一定要放在hover的后面，否则没有效果*/
#RedButton:pressed {
    background-color: #ffcdd2; /*鼠标按下不放时背景颜色*/
}

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

#GreenButton2 {
    /*background-color: #4caf50;*/
    height:15px; 
    width: 30px;
    border-radius: 5px; /*圆角*/
}
#GreenButton2:hover {
    background-color: #81c784;
}
#GreenButton2:pressed {
    background-color: #c8e6c9;
}


/*根据文字内容来区分按钮,同理还可以根据其它属性来区分*/
QPushButton[text="purple button"] {
    color: white; /*文字颜色*/
    background-color: #9c27b0;
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
"""




# sql2 = "SELECT gender where gender = 1 in (select gender as gender FROM student_log_time where log_time between '2022-03-18'  and '2022-03-19') ;"
# test = Database()
# sql = "select count (gender) FROM student_log_time where log_time between '2022-03-18'  and '2022-03-19' and gender =0;"

# print(test.c.execute(sql).fetchall())
# input() 

#递归删除文件夹以及文件




# import numpy as np  
# import faiss  

# # 向量个数  
# num_vec = 5000  
# # 向量维度  
# vec_dim =   128
# # 搜索topk  
# topk = 5

# # 随机生成一批向量数据  
# vectors = np.random.rand(num_vec, vec_dim).astype('float32')


# # 创建索引  
# faiss_index = faiss.IndexFlatL2(vec_dim)  # 使用欧式距离作为度量 
# print(type(vectors))

# # 添加数据  
# faiss_index.add(vectors)  

# # 查询向量 假设有5个  
# query_vectors = np.random.rand(5, vec_dim).astype('float32')
# print(type(query_vectors))
# print(query_vectors)

# # 搜索结果  
# # 分别是 每条记录对应topk的距离和索引  
# # ndarray类型 。shape：len(query_vectors)*topk  
# res_distance, res_index = faiss_index.search(query_vectors, topk)  
# print("索引:",res_index)  
# print("距离:",res_distance)
# print(vectors[res_index[0]])

# # def creat_faiss(self):
# #         student = Database()
# #         self.list_vector = []
# #         for i in student.c.execute("SELECT vector from student"):#查询数据库中所有人脸编码
# #             i = np.loads(i["vector"])
# #             self.list_vector.append(i)
       
# #         if len(self.list_vector) == 0:
# #             return "请先注册用户"
# #         vec_dim = 128
# #         self.faiss_index = faiss.IndexFlatL2(vec_dim)  # 使用欧式距离作为度量  
# #         self.faiss_index.add(np.array(self.list_vector).astype('float32'))

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


