from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog
from src.Database import database
from PyQt5.QtGui import QIcon 
from PyQt5.QtCore import Qt
from .Creatuser import CreatUser
import os,shutil
from .ImgPath import get_img_path
from .MyMd5 import MyMd5
class UpdateUserData(QDialog):
    def __init__(self,information= None):
        super(UpdateUserData, self).__init__()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("修改用户信息")
        self.setWindowIcon(QIcon("resources/修改.png"))
        self.path = None
        self.information =information
      
        self.id_label = QLabel('学号:', self)
        self.user_label = QLabel('姓名:', self)
        self.gender_label = QLabel('性别:', self)
        self.password_label = QLabel('密码:', self)

        self.id_number_line = QLineEdit(self)
        self.user_name_line = QLineEdit(self)
        self.gender_line = QLineEdit(self)
        self.password_line = QLineEdit(self)
        self.vector_button = QPushButton(":", self,objectName="GreenButton2")
        self.vector_button.setFlat(True)

        self.vector_button.setIcon(QIcon("./resources/文件.png"))

        self.vector_line = QLineEdit(self)
        #self.ensure_button = QPushButton('确定修改', self,objectName="GreenButton")

        self.user_h_layout = QHBoxLayout()
        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.vector_h_layout = QHBoxLayout()
        self.password_h_layout = QHBoxLayout()
        self.buttonBox_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()
        self.resize(300, 200)
        if information is not None:
            self.id_number_line.setText((str(information["id_number"])))
            self.user_name_line.setText(information["user_name"])
            self.gender_line.setText(information["gender"])
            self.password_line.setText(information["password"])
        
        self.buttonBox1 = QPushButton()
        self.buttonBox2 = QPushButton()
        self.buttonBox1 = QPushButton(objectName="GreenButton")
        self.buttonBox2 = QPushButton(objectName="GreenButton")
        self.buttonBox1.setText("确定")
        self.buttonBox2.setText("取消")
        #self.buttonBox.setGeometry(QRect(-20, 340, 341, 32))
        self.buttonBox1.clicked.connect(self.accept_)
        self.buttonBox2.clicked.connect(self.reject_)
        self.layout_init()
    #
    def accept_(self):#接受弹出窗口状态
       result = self.update(self.information["id_number"])
       if result:
            
            QMessageBox.information(self, "sucess", "修改成功",
                                QMessageBox.Yes) #最后的Yes表示弹框的按钮显示为Yes，默认按钮显示为OK,不填QMessageBox.Yes即为默认
           
            self.accept()#返回1
    def reject_(self):
        self.reject()#返回0
    def layout_init(self):
        self.user_h_layout.addWidget(self.id_label)
        self.user_h_layout.addWidget(self.id_number_line)
        self.pwd_h_layout.addWidget(self.user_label)
        self.pwd_h_layout.addWidget(self.user_name_line)
        self.pwd2_h_layout.addWidget(self.gender_label)
        self.pwd2_h_layout.addWidget(self.gender_line)
        self.password_h_layout.addWidget(self.password_label)
        self.password_h_layout.addWidget(self.password_line)
        self.vector_h_layout.addWidget(self.vector_button)
        self.vector_h_layout.addWidget(self.vector_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addLayout(self.password_h_layout)
        self.all_v_layout.addLayout(self.vector_h_layout)
        self.buttonBox_layout.addWidget(self.buttonBox1)
        self.buttonBox_layout.addWidget(self.buttonBox2)
        self.all_v_layout.addLayout(self.buttonBox_layout)
        self.setLayout(self.all_v_layout)
        self.vector_button.clicked.connect(self.get_path)
    
    def delete(self,id):
        path = "img_information/student/{0}".format(str(id))
       
        database.delete(id)
        database.c.execute("delete from student_log_time where id_number = {0}".format(id))
        
        #删除用户日志信息文件
        if  os.path.exists(path):
            shutil.rmtree(path)
            print("删除用户文件夹")

    def update(self,id):
        user_name = self.user_name_line.text()
        id_number = self.id_number_line.text()
        password = self.password_line.text()
        gender = self.gender_line.text()
        #检查输入信息
        
        if  gender == "男" or gender == "女":
            pass
        else:
            QMessageBox.critical(self, 'Wrong', 'gender is only 男 or 女')
            return False

        if len(id_number)>20 or (not id_number.isdigit()):
            QMessageBox.critical(self, 'Wrong', 'id_number is only digit or is too long!')
            return False

        if  len(database.c.execute("select id_number from student where id_number = {} "
        .format(id_number)).fetchall()) == 1 and id != id_number:
            QMessageBox.critical(self, 'Wrong',
                                     ' 这个学号已经存在')
            return False
        if (len(password) < 6 or len(password) > 13): 
            if(password != self.information["password"]):
                QMessageBox.critical(self, 'Wrong', ' Passwords is too short or too long!')
                return False
            
        r = QMessageBox.warning(self, "注意", "确认修改？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.No:
            return False
               ##更改用户文件信息
        old_path = "img_information/student/{0}/".format(str(id))
        new_path = "img_information/student/{0}/".format(str(id_number))
        #更改后变更用户日志信息文件夹
        if not os.path.exists(old_path):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(new_path)
            os.makedirs("img_information/student/{0}/log".format(str(id_number)))
            #shutil.rmtree("img_information/student/{0}".format(str(id)))
        else :
            os.rename("img_information/student/{0}/{1}.jpg".format(str(id),str(id)),"img_information/student/{0}/{1}.jpg".format(str(id),str(id_number)))
            os.rename(old_path,new_path)
        if self.path == None:#图片可以为不变更
           
            if(password != self.information["password"]):
                salt = MyMd5().create_salt()
                password = MyMd5().create_md5(password,salt)
                database.c.execute("UPDATE student SET id_number = '{0}',user_name = '{1}',gender = '{2}',password = ?,img_path =? ,salt = ? WHERE id_number = {3}"\
            .format(id_number,user_name,gender,id),(password,"img_information/student/{0}/log".format(id_number),salt))
            else:
                database.c.execute("UPDATE student SET id_number = '{0}',user_name = '{1}',gender = '{2}',img_path = ?  WHERE id_number = '{3}'"\
            .format(id_number,user_name,gender,id),("img_information/student/{0}/log".format(id_number),))
            
        else :
           
            creatuser = CreatUser()
            vector = creatuser.get_vector(self.path)
            creatuser.insert_img(id_number,self.path,"student")
            if(password != self.information["password"]):
                salt = MyMd5().create_salt()
                password = MyMd5().create_md5(password,salt)
                database.c.execute("update student set id_number= ?,user_name = ?,gender = ? ,vector = ?,password = ?,img_path = ? ,salt = ? where id_number = {0}"
                .format(id),(id_number,user_name,gender,vector,password,"img_information/student/{0}/log".format(id_number),salt))
            else:
                database.c.execute("update student set id_number= ?,user_name = ?,gender = ? ,vector = ?,img_path = ?  where id_number = {0}"
                .format(id),(id_number,user_name,gender,vector,"img_information/student/{0}/log".format(id_number)))
        database.c.execute("update student_log_time set id_number= {0} where id_number = {1}".format(id_number,id))
        return True
           
        #获取图片路径  
    def get_path(self):
        path = get_img_path(self)
        if path :
            self.path = path
            self.vector_line.setText(path) 
            return 
