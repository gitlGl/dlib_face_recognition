from peewee import *
import configparser
database = SqliteDatabase('resources/company.db')

class BaseModel(Model):
    class Meta:
        database = database


class verAdmin(BaseModel):
    id_number = CharField(primary_key=True)
    password = CharField()
    salt = CharField()
    vector = BlobField(null=True)

    class Meta:
        table_name = 'ver_admin'

class AdminLogTime(BaseModel):
    id_number = CharField()
    log_time = DateTimeField()

    class Meta:
        table_name = 'admin_log_time'
        primary_key = False

class Student(BaseModel):
    count = IntegerField(null=True)
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
database.create_tables([verAdmin, AdminLogTime, Student, StudentLogTime])


def configRead(filePath:str):
    cfg = configparser.ConfigParser() 
    cfg.read(filePath)
    if "sql" in cfg.sections():
        host=cfg.get('sql','host')
        port=cfg.getint('sql','port')
        user=cfg.get('sql','user')
        passwd=cfg.get('sql','password')
        dbName=cfg.get('sql','db_name')
        charset=cfg.get('sql','charset')
        return host,port,user,passwd,dbName,charset
    else:
        return None,None,None,None,None,None,None


host,port,user,password,dbName,charset = configRead("config.ini")
print(host,port,user,password,dbName,charset)
RemoteDatabase = MySQLDatabase(

database= dbName,  # 数据库名
host = host,  # 数据库地址
port = port,  # 数据库端口
password = password,  # 数据库密码
charset = charset,  # 字符集
user = user

)
class BaseRemote(Model):
   class Meta:
         database = RemoteDatabase
class RemoteAdmin(BaseRemote):
    id = BigAutoField(primary_key=True)
    mac_address = CharField(null=True)
    verifye = CharField(unique=True)
    vector = BlobField(null=True)
    isResgister = BooleanField(null=False)

    
    class Meta:
        table_name = 'ver_admin'

RemoteAdmin.create_table([RemoteAdmin])


