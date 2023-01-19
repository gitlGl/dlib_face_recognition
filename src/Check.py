from PyQt5.QtWidgets import QMessageBox
from .Database import Database
from .MyMd5 import MyMd5
import datetime
def check_user_id(user_id):

    if not user_id.isdigit() or len(user_id) > 100:
        return False
    return True


def check_user_pwd(user_pwd):
    if len(user_pwd) < 6 or len(user_pwd) > 13:
            return False
    return True
def verifye_pwd(user_id,user_pwd,tabel_name):
    admin = Database()
    user = admin.c.execute(
                "select id_number,salt, password  from {0} where id_number = {1} "
                .format(tabel_name,user_id)).fetchall()

    if len(user) != 1:
        return False              

    item = user[0]
    pass_word = MyMd5().create_md5(user_pwd, item["salt"])
    if pass_word == item["password"]: 
        return True
    
    return False
# QMessageBox.information(parent, 'Information', '警告 username or Password')