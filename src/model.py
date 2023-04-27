from peewee import *

database1 = SqliteDatabase('resources/company.db')

class BaseModel(Model):
    class Meta:
        database = database1


class Admin(BaseModel):
    id_number = CharField(primary_key=True)
    password = CharField()
    salt = CharField()
    vector = BlobField(null=True)

    class Meta:
        table_name = 'admin'

class AdminLogTime(BaseModel):
    id_number = CharField()
    log_time = DateTimeField()

    class Meta:
        table_name = 'admin_log_time'
        primary_key = False

class Student(BaseModel):
    cout = IntegerField(null=True)
    gender = CharField()
    id_number = CharField(primary_key=True)
    password = CharField()
    salt = CharField()
    user_name = CharField()
    vector = BlobField(null=True)

    class Meta:
        table_name = 'student'

class StudentLogTime(BaseModel):
    gender = BooleanField(null=True)
    id_number = CharField()
    log_time = DateTimeField()

    class Meta:
        table_name = 'student_log_time'
        primary_key = False
database1.create_tables([Admin, AdminLogTime, Student, StudentLogTime])




RemoteDatabase = MySQLDatabase(

"face_recognition",  # 数据库名
host = '127.0.0.1',  # 数据库地址
port = 3306,  # 数据库端口
password = '123456',  # 数据库密码
charset = "utf8",  # 字符集
user = "user"

)
class BaseRemote(Model):
   class Meta:
         database = RemoteDatabase
class RemoteAdmin(BaseRemote):
    mac_address = CharField()
    verifye = CharField(primary_key=True)
    vector = BlobField(null=True)


    
    class Meta:
        table_name = 'admin'


