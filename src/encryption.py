from random import Random
import hashlib
import string
import uuid
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

#密码加密

def createSalt(length=6):
    salt = ""
    chars = string.ascii_letters + string.digits
    len_chars = len(chars) - 1
    random = Random()
    for i in range(length):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]
    return salt

def createMd5(password, salt,id_number):#随机盐加三位用户id混淆
    md5 = hashlib.md5()
    md5.update((password + salt[1:4] + id_number[-4:-1]).encode("utf-8"))
    return md5.hexdigest()

class aes():
    Key = uuid.uuid1().hex[-12:][1:6]+'abc'
    mac_address = uuid.uuid1().hex[-12:]
    days = 3

    @staticmethod
    def encrypt(data,mac_address):
       
        key = pad(mac_address.encode("utf8"),AES.block_size)
        cipher = AES.new(key,AES.MODE_ECB)
        plaintext = data.encode('utf8')
        msg = cipher.encrypt(pad(plaintext,AES.block_size))
        result = str(base64.b64encode(msg).decode('utf8'))
        return result
        
    @staticmethod
    def decrypt(data,mac_address):
       
        key = pad(mac_address.encode("utf8"),AES.block_size)
        cipher = AES.new(key,AES.MODE_ECB)
        try:
            plaintext = base64.b64decode(data.encode("utf8"))
            msg = unpad(cipher.decrypt(plaintext),AES.block_size)
            result = str(msg.decode('utf8'))
            return result
        except:
            return False
