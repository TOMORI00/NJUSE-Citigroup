from flask import Flask, request
from flask_cors import *
import json

from vo.ResponseVO import build_success

app = Flask(__name__)
# 跨域
CORS(app, supports_credentials=True)


@app.route('/')
def hello_world():
    return 'Hello World!'


# 测试用
@app.route('/api/hello/get', methods=["GET", "POST"])
def get():
    print("Flask get")
    response = build_success("hh")
    print(response)
    return response


# 测试用
@app.route('/api/hello/post', methods=["GET", "POST"])
def post():
    data = request.get_json(silent=True)
    print(data)
    print("Flask post")
    return '1'


# 导入excel
@app.route('/api/upload/importExcel', methods=["GET", "POST"])
def import_excel():
    data = request.get_json(silent=True)
    print("import_excel", data)
    return build_success(None)


if __name__ == '__main__':
    # 与axios配置对应
    app.run(host="localhost", port='8080')
