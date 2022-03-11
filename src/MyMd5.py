from random import Random
import hashlib
import string


#密码加密
class MyMd5():
    def __init__(self):
        pass

    def create_salt(self, length=4):
        salt = ""
        chars = string.ascii_letters + string.digits
        len_chars = len(chars) - 1
        random = Random()
        for i in range(length):
            # 每次从chars中随机取一位
            salt += chars[random.randint(0, len_chars)]
        return salt

    def create_md5(self, password, salt):
        md5 = hashlib.md5()
        md5.update((password + salt).encode("utf-8"))
        return md5.hexdigest()
