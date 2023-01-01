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
def verifye_pwd(user_id,user_pwd):
    admin = Database()
    user = admin.c.execute(
                "select id_number,salt, password  from admin where id_number = {} "
                .format(user_id)).fetchall()

    if len(user) == 0:
      return False

    if len(user) != 1:
        return False              

    item = user[0]
    pass_word = MyMd5().create_md5(user_pwd, item["salt"])
    if pass_word == item["password"]:
        admin.c.execute("INSERT INTO admin_log_time (id_number,log_time ) \
VALUES (?,?)", (item["id_number"], datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))
        admin.conn.commit()
        admin.conn.close()
        return item["id_number"]
    
    return False
# QMessageBox.information(parent, 'Information', '警告 username or Password')