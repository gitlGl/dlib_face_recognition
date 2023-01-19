"""
pickle序列化对象和类到数据库,需修改mysql数据库表结构,字段类型设为二进制,如blob类型,参考:
https://www.cnblogs.com/wangchunlan1299/p/7725062.html
| test  | CREATE TABLE `test` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `obj` mediumblob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 |
<__main__.Person object at 0x0000000002A82A20> zhangsan 18
name:zhangsan,age:18
"""
import pickle
import pymysql
from src.Creatuser import CreatUser
import numpy as np
 
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
 
    def introduce(self):
        print('name:%s,age:%s' % (self.name, self.age))
 
 
"""
# 序列化对象
person = Person('zhangsan', 18)
ret = pickle.dumps(person)
# print(ret)
# obj = pickle.loads(ret)
# print(obj, obj.name, obj.age)
# obj.introduce()
conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', database='test', charset='utf8')
cursor = conn.cursor()
cursor.execute('insert into test(obj) values (%s);', [ret])
conn.commit()
cursor.execute('select * from test')
result = cursor.fetchall()
ret = result[0][1]
obj = pickle.loads(ret)
print(obj, obj.name, obj.age)
obj.introduce()
"""
 
# 序列化类
ret = pickle.dumps(Person)

 
conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='study', charset='utf8')
cursor = conn.cursor()
vector = CreatUser().get_vector("img_information/admin/12345678910/12345678910.jpg")
cursor.execute('insert into test(obj) values (%s)', vector)
cursor.execute('update test set obj = "%s" where id = 5', vector)
print(vector)

cursor.execute('select  obj  from test where obj = "%s"', vector)
test = print(cursor.fetchall()[0][0])
np.loads(test)
print(test)

conn.commit()

cursor.execute('select * from test')
result = cursor.fetchall()
ret = result[1][1]
 
person_class = pickle.loads(ret)
person = person_class('zhangsan', 18)
print(person.name, person.age)
person.introduce()