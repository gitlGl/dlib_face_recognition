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
import pickle,uuid
from src  import RemoteAdmin

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

       
        flag = RemoteAdmin.get_or_none(RemoteAdmin.verifye == data["verifye"])
        if flag:
            self.responses = self.flag_true

            self.wfile.write(self.flag_true)
        else:
            self.responses = self.flag_fals
            
            self.wfile.write(self.flag_fals)
            return
        RemoteAdmin.update({RemoteAdmin.mac_address: data["mac_address"],RemoteAdmin.vector:data["vector"]}
        ).where(RemoteAdmin.verifye == data["verifye"]).execute()
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
