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


from http.server import HTTPServer, BaseHTTPRequestHandler
import pickle
from src  import RemoteAdmin
from src import aes
from src import createMd5

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

    def resgister(self,data):

       
        tem_data = RemoteAdmin.get_or_none(RemoteAdmin.id == data["id"])
        
       
        if tem_data:
            verifye_md5 = aes.decrypt(data['verifye'],tem_data.verifye)
            vector_md5 = aes.decrypt(data['vector'],tem_data.verifye)
            if not verifye_md5 or not vector_md5:
                self.responses = self.flag_fals
                self.wfile.write(self.flag_fals)
                return
            
            if verifye_md5 != createMd5(tem_data.verifye, data["mac_address"]):
                self.responses = self.flag_fals
                self.wfile.write(self.flag_fals)
                return
               

            self.responses = self.flag_true

            self.wfile.write(self.flag_true)
        else:
            self.responses = self.flag_fals
            
            self.wfile.write(self.flag_fals)
            return
        RemoteAdmin.update({RemoteAdmin.mac_address: data["mac_address"],RemoteAdmin.vector:vector_md5}
        ).where(RemoteAdmin.id == data["id"]).execute()
        return True
        
    def login(self,data):
        flag = RemoteAdmin.get_or_none(RemoteAdmin.mac_address == data["mac_address"])
        
        if flag:
            self.responses = self.flag_true

            self.wfile.write(self.flag_true)
        else:
            self.responses = self.flag_fals
            
            self.wfile.write(self.flag_fals)

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
