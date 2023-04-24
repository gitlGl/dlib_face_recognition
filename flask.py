from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/", methods=[ "POST"])
def hello_world():
    data = request.data
    print(type(data))
    print(data)
    return data
app.run()
