# from flask import Flask
# from flask import request
# import pickle
# app = Flask(__name__)

# @app.route("/", methods=[ "POST"])
# def hello_world():
#     data = request.get_data()
#     data  = pickle.loads(data)
#     print(type(data))
#     data = pickle.dumps(data)
#     print(data)
#     return data
# app.run(host="localhost",port=8080,debug=True)

from peewee import *
import configparser
from http.server import HTTPServer, BaseHTTPRequestHandler
import pickle,os
from src import aes,createMd5Verifye
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
current_file_path = os.path.abspath(__file__)
base_dir = os.path.dirname(current_file_path)
host,port,user,password,dbName,charset = configRead(base_dir + "\\config.ini")

RemoteDatabase = MySQLDatabase(

database= dbName,  # 数据库名
host = host,  # 数据库地址
port = port,  # 数据库端口
password = password,  # 数据库密码
charset = charset,  # 字符集
user = user

)#083e8ef25874
class BaseRemote(Model):
   class Meta:
         database = RemoteDatabase
class RemoteAdmin(BaseRemote):
    id = BigAutoField(primary_key=True)
    mac_address = CharField(null=True)
    verifye = CharField(unique=True)
    vector = BlobField(null=True)
    id_number = CharField(null=True)
    isResgister = BooleanField(null=False)
    

    
    class Meta:
        table_name = 'ver_admin'
RemoteAdmin.create_table([RemoteAdmin])
host = ('localhost', 8888)
class Resquest(BaseHTTPRequestHandler):
    def do_POST(self):
        datas = self.rfile.read(int(self.headers['content-length']))
        data  = pickle.loads(datas)
        self.flag_true= pickle.dumps(True)
        self.flag_fals = pickle.dumps(False)
        self.send_response(200)
        self.send_header('', '')
        self.end_headers()
        if data["flag"]=='resgister': 
            self.resgister(data)
            return
        if data['flag']=='login':
            self.login(data)
            return
        if data['flag']=='is_admin':
            id_number = pickle.dumps('12345678910')
            self.wfile.write(id_number)
            return

    def resgister(self,data):

       
        tem_data = RemoteAdmin.get_or_none(RemoteAdmin.id == data["id"])
        
        if tem_data:
            verifye_md5 = aes.decrypt(data['verifye'],tem_data.verifye)
            vector_md5 = aes.decrypt(data['vector'],tem_data.verifye)
    
            if not tem_data.isResgister:
                
                self.responses = self.flag_fals
                self.wfile.write(self.flag_fals)
                return
            if not verifye_md5 or not vector_md5:
                self.responses = self.flag_fals
                self.wfile.write(self.flag_fals)
                return
            
            if verifye_md5 != createMd5Verifye(tem_data.verifye, data["mac_address"]):
                self.responses = self.flag_fals
                self.wfile.write(self.flag_fals)
                return
               

            self.responses = self.flag_true

            self.wfile.write(self.flag_true)
        else:
            self.responses = self.flag_fals
            
            self.wfile.write(self.flag_fals)
            return
        RemoteAdmin.update({RemoteAdmin.mac_address: data["mac_address"],
                            RemoteAdmin.vector:vector_md5,RemoteAdmin.id_number:data['id_number'] ,RemoteAdmin.isResgister:False}
        ).where(RemoteAdmin.id == data["id"]).execute()
        return True
        
    def login(self,data):
        flag1 = RemoteAdmin.get_or_none(RemoteAdmin.mac_address == data["mac_address"])
        flag2 = RemoteAdmin.get_or_none(RemoteAdmin.id_number == data["id_number"])
        
        if flag1 and flag2:
            self.responses = self.flag_true

            self.wfile.write(self.flag_true)
        else:
            self.responses = self.flag_fals
            
            self.wfile.write(self.flag_fals)

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
