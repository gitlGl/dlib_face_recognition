from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog
from src.GlobalVariable import database
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .Creatuser import CreatUser
import os, shutil
from .Check import getImgPath
from .MyMd5 import MyMd5
from .Check import verifyePwd,checkPath


class UpdateUserData(QDialog):
    def __init__(self, information=None):
        super(UpdateUserData, self).__init__()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint
                            | Qt.WindowCloseButtonHint)
        self.setWindowTitle("修改用户信息")
        self.setWindowIcon(QIcon("resources/修改.png"))
        self.path = None
        self.information = information

        self.id_label = QLabel('学号:', self)
        self.user_label = QLabel('姓名:', self)
        self.gender_label = QLabel('性别:', self)
        self.password_label = QLabel('密码:', self)

        self.id_number_line = QLineEdit(self)
        self.user_name_line = QLineEdit(self)
        self.gender_line = QLineEdit(self)
        self.password_line = QLineEdit(self)
        self.vector_button = QPushButton("图片:", self, objectName="GreenButton")
        self.vector_button.setFlat(True)

        self.vector_button.setIcon(QIcon("resources/文件.png"))

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
        self.layoutInit()

    #
    def accept_(self):  #接受弹出窗口状态
        result = self.update(self.information["id_number"])
        if result:

            QMessageBox.information(
                self, "sucess", "修改成功", QMessageBox.Yes
            )  #最后的Yes表示弹框的按钮显示为Yes，默认按钮显示为OK,不填QMessageBox.Yes即为默认

            self.accept()  #返回1

    def reject_(self):
        self.reject()  #返回0

    def layoutInit(self):
        self.user_h_layout.addSpacing(20)
        self.user_h_layout.addWidget(self.id_label)
        self.user_h_layout.addWidget(self.id_number_line)

        self.pwd_h_layout.addSpacing(20)
        self.pwd_h_layout.addWidget(self.user_label)
        self.pwd_h_layout.addWidget(self.user_name_line)

        self.pwd2_h_layout.addSpacing(20)
        self.pwd2_h_layout.addWidget(self.gender_label)
        self.pwd2_h_layout.addWidget(self.gender_line)

        self.password_h_layout.addSpacing(20)
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
        self.vector_button.clicked.connect(self.getPath)

    def delete(self, id):
        path = "img_information/student/{0}".format(str(id))
        try:
            database.c.execute(
                "delete from student where id_number = {0}".format(id))
            database.c.execute(
                "delete from student_log_time where id_number = {0}".format(
                    id))
        except:
            database.conn.rollback()
            QMessageBox.critical(self, 'Wrong', "未知错误")
            return

        #删除用户日志信息文件
        if os.path.exists(path):
            shutil.rmtree(path)
        database.conn.commit()

    def update(self, id):
        user_name = self.user_name_line.text()
        id_number = self.id_number_line.text()
        password = self.password_line.text()
        gender = self.gender_line.text()
        #检查输入信息
        lenth = len(user_name)
        if lenth > 16 or lenth == 0:

             QMessageBox.critical(self, 'Wrong', '用户名为13个有效字符')
             return False

        if gender == "男" or gender == "女":
            pass
        else:
            QMessageBox.critical(self, 'Wrong', 'gender is only 男 or 女')
            return False

        if len(id_number) > 20 or (not id_number.isdigit()):
            QMessageBox.critical(self, 'Wrong',
                                 'id_number is only digit or is too long!')
            return False

        if len(
                database.c.execute(
                    "select id_number from student where id_number = {} ".
                    format(id_number)).fetchall()) == 1 and id != id_number:
            QMessageBox.critical(self, 'Wrong', ' 这个学号已经存在')
            return False
        if (len(password) < 6 or len(password) > 13):
            if (password != self.information["password"]):
                QMessageBox.critical(self, 'Wrong',
                                     ' Passwords is too short or too long!')
                return False

        r = QMessageBox.warning(self, "注意", "确认修改？",
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No)
        if r == QMessageBox.No:
            return False

        try:
            if self.vector_line.text() == '':  #图片可以为不变更
                if (password != self.information["password"]):
                    salt = MyMd5().createSalt()
                    password = MyMd5().createMd5(password, salt, id_number)
                    database.c.execute("UPDATE student SET id_number = '{0}',user_name = '{1}',gender = '{2}',password = ?,salt = ? WHERE id_number = {3}"\
                .format(id_number,user_name,gender,id),(password,salt))
                else:
                    database.c.execute("UPDATE student SET id_number = '{0}',user_name = '{1}',gender = '{2}' WHERE id_number = '{3}'"\
                .format(id_number,user_name,gender,id))
                database.c.execute(
                    "update student_log_time set id_number= {0} where id_number = {1}"
                    .format(id_number, id))
                database.conn.commit()
            else:
                path = self.vector_line.text()
                if not checkPath(path):
                    return
                vector =  CreatUser().getVector(path)
                if (password != self.information["password"]):
                    salt = MyMd5().createSalt()
                    password = MyMd5().createMd5(password, salt, id_number)
                    database.c.execute(
                        "update student set id_number= ?,user_name = ?,gender = ? ,vector = ?,password = ?,salt = ? where id_number = {0}"
                        .format(id),
                        (id_number, user_name, gender, vector, password, salt))
                else:
                    database.c.execute(
                        "update student set id_number= ?,user_name = ?,gender = ? ,vector = ? where id_number = {0}"
                        .format(id), (id_number, user_name, gender, vector))

                database.c.execute(
                    "update student_log_time set id_number= {0} where id_number = {1}"
                    .format(id_number, id))
                database.conn.commit()

        except:
            database.conn.rollback()
            QMessageBox.critical(self, 'Wrong', "未知错误")
            return False

            ##更改用户文件信息
        old_path = "img_information/student/{0}/".format(str(id))
        new_path = "img_information/student/{0}/".format(str(id_number))
        #更改后变更用户日志信息文件夹
        if not os.path.exists(old_path):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(new_path)
            os.makedirs("img_information/student/{0}/log".format(
                str(id_number)))
            QMessageBox.critical(self, 'Wrong', "该用户图片文件可能丢失！")
            #shutil.rmtree("img_information/student/{0}".format(str(id)))
        else:
            img_path = "img_information/student/{0}/{1}.jpg".format(
                str(id), str(id))
            if os.path.isfile(img_path):
                os.rename(
                    img_path, "img_information/student/{0}/{1}.jpg".format(
                        str(id), str(id_number)))
            else:
                QMessageBox.critical(self, 'Wrong', "该用户图片文件可能丢失！")
            os.rename(old_path, new_path)
        if self.path:
            CreatUser().insertImg(id_number, self.path, "student")
        return True

        #获取图片路径
    def getPath(self):
        path = getImgPath(self)
        if path:
            self.vector_line.setText(path)
            return


class UpdateAdminData(QDialog):
    def __init__(self, information=None):
        super(UpdateAdminData, self).__init__()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint
                            | Qt.WindowCloseButtonHint)
        self.setWindowTitle("修改管理员信息")
        self.setWindowIcon(QIcon("resources/修改.png"))
        self.path = None
        self.information = information

        self.id_label = QLabel('学号:', self)
        self.password_label = QLabel('密码:', self)

        self.id_number_line = QLineEdit(self)
        self.password_line = QLineEdit(self)
        self.vector_button = QPushButton("图片:", self, objectName="GreenButton")
        self.vector_button.setFlat(True)

        self.vector_button.setIcon(QIcon("resources/文件.png"))

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
        self.layoutInit()

    #
    def accept_(self):  #接受弹出窗口状态
        result = self.update(self.information["id_number"])
        if result:
            QMessageBox.information(self, 'sucess', '修改成功!')
            self.accept()  #返回1

    def reject_(self):
        self.reject()  #返回0

    def layoutInit(self):
        self.user_h_layout.addSpacing(20)
        self.user_h_layout.addWidget(self.id_label)
        self.user_h_layout.addWidget(self.id_number_line)

        self.pwd_h_layout.addSpacing(20)
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
        self.vector_button.clicked.connect(self.getPath)

    def delete(self, id):
        path = "img_information/admin/{0}".format(str(id))
        try:
            database.c.execute(
                "delete from admin where id_number = {0}".format(id))
            database.c.execute(
                "delete from admin_log_time where id_number = {0}".format(id))
        except:
            QMessageBox.critical(self, 'Wrong', "未知错误")
            database.conn.rollback()
            return

        #删除用户日志信息文件
        if os.path.exists(path):
            shutil.rmtree(path)
        database.conn.commit()

    def update(self, id):
        password = self.password_line.text()
        id_number = self.id_number_line.text()

        #检查输入信息
        if len(id_number) > 20 or (not id_number.isdigit()):
            QMessageBox.critical(self, 'Wrong',
                                 'id_number is only digit or is too long!')
            return False

        if len(
                database.c.execute(
                    "select id_number from admin where id_number = {} ".format(
                        id_number)).fetchall()) == 1 and id != id_number:
            QMessageBox.critical(self, 'Wrong', ' 这个用户已存在')
            return False
        if (len(password) < 6 or len(password) > 13):
            if (password != self.information["password"]):
                QMessageBox.critical(self, 'Wrong',
                                     ' Passwords is too short or too long!')
                return False

        r = QMessageBox.warning(self, "注意", "确认修改？",
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No)
        if r == QMessageBox.No:
            return False
        try:
            if self.vector_line.text() == '':  #图片可以为不变更
                if (password != self.information["password"]):
                    salt = MyMd5().createSalt()
                    password = MyMd5().createMd5(password, salt, id_number)
                    database.c.execute(
                        "update admin set id_number = ?,password = ?,salt = ? where id_number = {0}"
                        .format(id), (id_number, password, salt))
                else:
                    database.c.execute(
                        "update admin set id_number = {0} where id_number = {1}"
                        .format(id_number, id))
                database.c.execute(
                    "update admin_log_time set id_number= {0} where id_number = {1}"
                    .format(id_number, id))
                database.conn.commit()
            else:
                path = self.vector_line.text()
                if not checkPath(path):
                    return
                vector = CreatUser().getVector(path)
                if (password != self.information["password"]):
                    salt = MyMd5().createSalt()
                    password = MyMd5().createMd5(password, salt, id_number)
                    database.c.execute(
                        "update admin set id_number= ?,password = ?,salt = ? ,vector = ? where id_number = {0}"
                        .format(id), (id_number, password, salt, vector))
                else:
                    database.c.execute(
                        "update admin set id_number= ? ,vector = ? where id_number = {0}"
                        .format(id), (id_number, vector))
                database.conn.commit()
        except:
            QMessageBox.critical(self, 'Wrong', "未知错误")
            database.conn.rollback()
            return False

        ##更改用户文件信息


        old_path = "img_information/admin/{0}/".format(str(id))
        new_path = "img_information/admin/{0}/".format(str(id_number))
        #更改后变更用户日志信息文件夹
        if not os.path.exists(old_path):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(new_path)
            os.makedirs("img_information/admin/{0}/log".format(str(id_number)))
            
            QMessageBox.critical(self, 'Wrong', "该用户图片文件可能丢失！")
            #shutil.rmtree("img_information/admin/{0}".format(str(id)))
        else:
            img_path = "img_information/admin/{0}/{1}.jpg".format(
                str(id), str(id))
            if os.path.isfile(img_path):
                os.rename(
                    img_path, "img_information/admin/{0}/{1}.jpg".format(
                        str(id), str(id_number)))
            else:
                QMessageBox.critical(self, 'Wrong', "该用户图片文件可能丢失！")
            os.rename(old_path, new_path)
        if self.path:
            CreatUser().insertImg(id_number, self.path, "admin")
        return True

        #获取图片路径
    def getPath(self):
        path = getImgPath(self)
        if path:
            self.vector_line.setText(path)
            return


class UpdatePwd(QDialog):
    def __init__(self, id_number):
        super().__init__()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint
                            | Qt.WindowCloseButtonHint)
        self.setWindowTitle('修改密码')
        self.setWindowIcon(QIcon('resources/修改密码.png'))
        self.id_number = id_number
        self.old_pwd_label = QLabel('旧密码:', self)
        self.new_pwd2_label = QLabel('新密码:', self)
        self.new_pwd3_label = QLabel('确认密码:', self)
        #self.new_pwd3_label.setStyleSheet("font-size:9pt;font-weight:35;")
        self.old_pwd_line = QLineEdit(self)
        self.new_pwd2_line = QLineEdit(self)
        self.new_pwd3_line = QLineEdit(self)

        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.pwd3_h_layout = QHBoxLayout()
        self.ensure_or = QHBoxLayout()
        self.pwd_h_layout.addSpacing(12)
        self.pwd_h_layout.addWidget(self.old_pwd_label)
        
        self.pwd_h_layout.addWidget(self.old_pwd_line)

        self.pwd2_h_layout.addSpacing(12)
        
        self.pwd2_h_layout.addWidget(self.new_pwd2_label)
        
        self.pwd2_h_layout.addWidget(self.new_pwd2_line)

        self.pwd3_h_layout.addWidget(self.new_pwd3_label)
        self.pwd3_h_layout.addWidget(self.new_pwd3_line)

        self.pwd_v_layout = QVBoxLayout()
        self.pwd_v_layout.addLayout(self.pwd_h_layout)
        self.pwd_v_layout.addLayout(self.pwd2_h_layout)
        self.pwd_v_layout.addLayout(self.pwd3_h_layout)
        self.btn1_event = QPushButton()
        self.btn1 = QPushButton(objectName="GreenButton")
        self.btn1.setText("确认修改")
        self.btn2 = QPushButton()
        self.btn2 = QPushButton(objectName="GreenButton")
        self.btn2.setText("取消修改")
        self.ensure_or.addWidget(self.btn1)
        self.ensure_or.addWidget(self.btn2)
        self.pwd_v_layout.addLayout(self.ensure_or)
        self.btn1.clicked.connect(self.btn1UpdatePwd)
        self.btn2.clicked.connect(self.btn2Event)

        self.setLayout(self.pwd_v_layout)

    def btn1UpdatePwd(self):
        old_pwd = self.old_pwd_line.text()
        new_pwd = self.new_pwd2_line.text()
        new_pwd_2 = self.new_pwd3_line.text()
        if new_pwd != new_pwd_2:
            QMessageBox.critical(self, 'Wrong', '两次密码不一致')
            return

        if len(new_pwd) < 6 and len(new_pwd) > 16:
            QMessageBox.critical(self, 'Wrong', '密码长度不能小于6位或大于16位')
            return

        if old_pwd == new_pwd:
            QMessageBox.critical(self, 'Wrong', '新旧密码不能一致')
            return

        item = database.c.execute(
            "select salt from admin where id_number = {0}".format(
                self.id_number)).fetchone()
        result = verifyePwd(self.id_number, old_pwd, "admin")
        if not result:
            QMessageBox.critical(self, 'Wrong', '旧密码错误')
            return
        new_pass_word = MyMd5().createMd5(new_pwd, item["salt"],
                                          self.id_number)
        database.c.execute(
            "update admin set password = ? where id_number = {0}".format(
                self.id_number), (new_pass_word, ))
        database.conn.commit()
        QMessageBox.information(self, 'Success', '修改成功')
        self.close()
        return

    #取消修改
    def btn2Event(self):
        self.close()
