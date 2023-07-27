from random import Random
import hashlib
import string


#密码加密
class MyMd5():
    @staticmethod
    def createSalt(length=6):
        salt = ""
        chars = string.ascii_letters + string.digits
        len_chars = len(chars) - 1
        random = Random()
        for i in range(length):
            # 每次从chars中随机取一位
            salt += chars[random.randint(0, len_chars)]
        return salt
    @staticmethod
    def createMd5(password, salt,id_number):#随机盐加三位用户id混淆
        md5 = hashlib.md5()
        md5.update((password + salt[1:4] + id_number[-4:-1]).encode("utf-8"))
        return md5.hexdigest()
