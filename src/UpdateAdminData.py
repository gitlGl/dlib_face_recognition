from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from src.Database import Database
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from src.GlobalVariable import models
from .Creatuser import CreatUser
import os,shutil
from .MyMd5 import MyMd5
from .ImgPath import get_img_path
class UpdateAdminData(QDialog):
    def __init__(self,information= None):
        super(UpdateAdminData, self).__init__()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("修改管理员信息")
        self.setWindowIcon(QIcon("resources/修改.png"))
        self.path = None
        self.information =information
      
        self.id_label = QLabel('学号:', self)
        self.password_label = QLabel('密码:', self)
       
        self.id_number_line = QLineEdit(self)
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
        self.buttonBox_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()
        self.resize(300, 200)
        if information is not None:
            self.id_number_line.setText((str(information["id_number"])))
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
            QMessageBox.critical(self, 'sucess', '修改成功!')
            self.accept()#返回1
    def reject_(self):
        self.reject()#返回0
    def layout_init(self):
        self.user_h_layout.addWidget(self.id_label)
        self.user_h_layout.addWidget(self.id_number_line)
        self.pwd_h_layout.addWidget(self.password_label)
        self.pwd_h_layout.addWidget(self.password_line)
        
        self.vector_h_layout.addWidget(self.vector_button)
        self.vector_h_layout.addWidget(self.vector_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addLayout(self.vector_h_layout)
        self.buttonBox_layout.addWidget(self.buttonBox1)
        self.buttonBox_layout.addWidget(self.buttonBox2)
        self.all_v_layout.addLayout(self.buttonBox_layout)
        self.setLayout(self.all_v_layout)
        self.vector_button.clicked.connect(self.get_path)
    
    def delete(self,id):
        path = "img_information/admin/{0}".format(str(id))
        data = Database()
        data.c.execute("delete from admin where id_number = {0}".format(id))
        data.c.execute("delete from admin_log_time where id_number = {0}".format(id))
        data.conn.commit()
        data.c.close()

        #删除用户日志信息文件
        if  os.path.exists(path):
            shutil.rmtree(path)

    def update(self,id):
        password = self.password_line.text()
        id_number = self.id_number_line.text()

        #检查输入信息
        if len(id_number)>20 or (not id_number.isdigit()):
            QMessageBox.critical(self, 'Wrong', 'id_number is only digit or is too long!')
            return False

        

        elif  len(Database().c.execute("select id_number from admin where id_number = {} "
        .format(id_number)).fetchall()) == 1 and id != id_number:
            QMessageBox.critical(self, 'Wrong',
                                     ' 这个用户已存在')
            return False
        if (len(password) < 6 or len(password) > 13): 
            if(password != self.information["password"]):
                QMessageBox.critical(self, 'Wrong', ' Passwords is too short or too long!')
                return False
            

        
        r = QMessageBox.warning(self, "注意", "确认修改？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.No:
            return False
        if self.path == None:#图片可以为不变更
            data = Database()
            if(password != self.information["password"]):
                salt = MyMd5().create_salt()
                password = MyMd5().create_md5(password,salt)
                data.c.execute("update admin set id_number = ?,password = ?,salt = ? where id_number = {0}"
                .format(id),(id_number,password,salt))
            else:
                    data.c.execute("update admin set id_number = {0} where id_number = {1}"
                .format(id_number,id))

            data.c.execute("update admin_log_time set id_number= {0} where id_number = {1}".format(id_number,id))
            data.conn.commit()
            data.conn.close()
            ##更改用户文件信息
            old_path = "img_information/admin/{0}/".format(str(id))
            new_path = "img_information/admin/{0}/".format(str(id_number))
            #更改后变更用户日志信息文件夹
            if not os.path.exists(old_path):  #判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(new_path)
                os.makedirs("img_information/admin/{0}/log".format(str(id_number)))
                #shutil.rmtree("img_information/admin/{0}".format(str(id)))
            else :
                os.rename("img_information/admin/{0}/{1}.jpg".format(str(id),str(id)),"img_information/admin/{0}/{1}.jpg".format(str(id),str(id_number)))
                os.rename(old_path,new_path)
            
        else :
            data = Database()
            salt = MyMd5().create_salt()
            password = MyMd5().create_md5(password,salt)
            old_path = "img_information/admin/{0}/".format(str(id))
            new_path = "img_information/admin/{0}/".format(str(id_number))
            if not os.path.exists(old_path):  #判断是否存在文件夹如果不存在则创建为文件夹
                if not os.path.exists("img_information/admin/{0}/log".format(str(id_number))):
                    os.makedirs("img_information/admin/{0}/log".format(str(id_number)))
            else:
                    os.rename("img_information/admin/{0}/{1}.jpg".format(str(id),str(id)),"img_information/admin/{0}/{1}.jpg".format(str(id),str(id_number)))
                    os.rename(old_path,new_path)
            vector = CreatUser().get_vector(id_number,self.path,"admin")
            data.c.execute("update admin set id_number= ?,password = ?,salt = ? ,vector = ? where id_number = {0}"
            .format(id),(id_number,password,salt,vector))
            data.c.execute("update admin_log_time set id_number= {0} where id_number = {1}".format(id_number,id))
            data.conn.commit()
            data.conn.close()
        
        return True
           
        #获取图片路径  
    def get_path(self):
        path = get_img_path(self)
        if path :
            self.path = path
            self.vector_line.setText(path) 
            return 
