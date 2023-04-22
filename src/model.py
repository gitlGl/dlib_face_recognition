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

item  = Admin.select().where(Admin.id_number == '123456')
print(item.count())
print(item[0].password)
for i in item:  
    print(i.password)
#print(type(item))




