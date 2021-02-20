import os
import shutil

import pymongo

from flask import Flask
from flask_cors import CORS

from financial_products_viewer import main
from fund_viewer import main_fv
from flask import jsonify

import json

app = Flask(__name__)
# 跨域
CORS(app, supports_credentials=True)

# gy
from flask import make_response, send_file
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])


# why
@app.route('/')
def hello():
    return 'Welcome to my watchlist'


# zym return
# input 基金 fund_viewer main_fv.py
@app.route('/api/output/getFvData')
def get_fv_data():
    success = True
    message = ""

    date_re, chart1, chartadd1, in1, duration, chart2_high, chart2_mid, chart2_low, chartadd2_high, chartadd2_mid, chartadd2_low, in2_high, in2_mid, in2_low, history_high, history_mid, history_low = main_fv.fun()

    # 历史推荐投资组合先存入history.txt
    history_high = str(history_high) + "\n"
    history_mid = str(history_mid) + "\n"
    history_low = str(history_low) + "\n"
    history = [history_high, history_mid, history_low]

    f = open("history.txt", 'w').close()  # 先清空
    f = open('history.txt', 'a')
    f.writelines(history)
    f.close()

    data = {
        "success": success,
        "message": message,
        "content": {
            "date": date_re, "chart1": chart1, "chartadd1": chartadd1, "in1": in1,
            "duration": duration,
            "chart2_high": chart2_high, "chart2_mid": chart2_mid, "chart2_low": chart2_low,
            "chartadd2_high": chartadd2_high, "chartadd2_mid": chartadd2_mid, "chartadd2_low": chartadd2_low,
            "in2_high": in2_high, "in2_mid": in2_mid, "in2_low": in2_low
        }
    }

    return jsonify(data)
    # test_data.append(3)
    # test_data.append(9)

    # return "heihei"


# zym
# input 理财 financial_products_viewer main.py
@app.route('/api/output/getFpvData')
def get_fpv_data():
    success = True
    message = ""

    date_re, chart1, in1, duration, chart2_high, chart2_mid, chart2_low, chartadd2_high, chartadd2_mid, chartadd2_low, in2_high, in2_mid, in2_low, history_high, history_mid, history_low = main.fun()

    # 历史推荐投资组合先存入history.txt
    history_high = str(history_high) + "\n"
    history_mid = str(history_mid) + "\n"
    history_low = str(history_low) + "\n"
    history = [history_high, history_mid, history_low]

    f = open("history.txt", 'w').close()  # 先清空
    f = open('history.txt', 'a')
    f.writelines(history)
    f.close()

    data = {
        "success": success,
        "message": message,
        "content": {
            "date": date_re, "chart1": chart1, "in1": in1,
            "duration": duration,
            "chart2_high": chart2_high, "chart2_mid": chart2_mid, "chart2_low": chart2_low,
            "chartadd2_high": chartadd2_high, "chartadd2_mid": chartadd2_mid, "chartadd2_low": chartadd2_low,
            "in2_high": in2_high, "in2_mid": in2_mid, "in2_low": in2_low
        }
    }

    return jsonify(data)


# zym
# 推荐组合及历史推荐组合 请注意先经过test_fv或test_fpv才能得到组合数据
@app.route('/api/output/getChart')
def get_chart():
    f = open("history.txt", "r", encoding='utf-8')
    history = f.readlines()
    f.close()
    history[0] = eval(history[0].rstrip('\n'))
    history[1] = eval(history[1].rstrip('\n'))
    history[2] = eval(history[2].rstrip('\n'))
    format_history = []

    for i in range(0, len(history)):
        tmp_history = []
        for one_history in history[i]:
            one_history_dict = {'year': one_history[0], 'month': one_history[1]}
            pie_list = [['name', 'contribution']]
            for j in range(0, len(one_history[2])):
                pie_list.append([one_history[2][j] + ' ' + one_history[3][j], one_history[4][j]])
            one_history_dict['pieData'] = pie_list
            tmp_history.append(one_history_dict)
        format_history.append(tmp_history)

    success = True
    message = ""

    data_chart = {
        "success": success,
        "message": message,
        "content": {
            "history_high": format_history[0], "history_mid": format_history[1], "history_low": format_history[2]
        }
    }
    print(data_chart)

    return jsonify(data_chart)
    # data_chart = {"history_high":history_high, "history_mid":history_mid,"history_low":history_low}
    # return json.dumps(data_chart)


# gy
# @app.route('/haha')
# def haha():
#    return 'Hello World!'

# gy download
@app.route('/testdownload', methods=['GET'])
def testdownload():
    response = make_response(send_file("demo.docx"))
    response.headers["Content-Disposition"] = "attachment; filename=demo.docx;"
    return response


# gy
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# gy upload
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join("/Users/guyi/Desktop/repoo", filename))
            file.save(os.path.join("C:/Users/zym0325/Desktop", filename))
            return "fine"
    return render_template('gui_data.html')


@app.route("/api/upload/uploadExcel", methods=['GET', 'POST'])
def upload_excel():
    success = True
    message = ''
    print("uploadExcel")
    type = request.form.get('type')
    print(type)
    # fv_input_dir_path = 'financial_products_viewer/input'
    # fpv_input_dir_path = 'fund_viewer/input'
    fv_dir_name = 'fund_viewer'
    fpv_dir_name = 'financial_products_viewer'
    fv_input_dir_path = os.path.join(fv_dir_name, 'input')
    fpv_input_dir_path = os.path.join(fpv_dir_name, 'input')

    # 清空基金input文件夹
    print(os.path.exists(fv_input_dir_path))
    if not os.path.exists(fv_input_dir_path):
        os.mkdir(fv_input_dir_path)
    else:
        shutil.rmtree(fv_input_dir_path)
        os.mkdir(fv_input_dir_path)

    # 清空理财input文件夹
    if not os.path.exists(fpv_input_dir_path):
        os.mkdir(fpv_input_dir_path)
    else:
        shutil.rmtree(fpv_input_dir_path)
        os.mkdir(fpv_input_dir_path)

    if request.method == 'POST':
        files = request.files.getlist('files')
        if type == '基金':
            success, message = save_excel(files, fv_input_dir_path)
        elif type == '理财':
            success, message = save_excel(files, fpv_input_dir_path)
    else:
        success = False
        message = "上传失败"
    data = {"success": success,
            "message": message,
            "content": ''
            }
    return jsonify(data)


def save_excel(files, dir_path):
    print(files)
    success = True
    message = ''
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(dir_path, filename))
        else:
            success = False
            message = '上传失败'
            break
    return success, message


# 登录函数
@app.route("/api/upload/loginIn", methods=['GET', 'POST'])
def login_in():
    success = True
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dataClient = pymongo.MongoClient('mongodb://localhost:27017/')
        if "citidb" not in dataClient.list_database_names():
            success = False
            message = "数据库不存在"
        else:
            db = dataClient['citidb']
            if 'user' not in db.list_collection_names():
                success = False
                message = "用户表不存在"
            else:
                collection = db['user']
                result = collection.find({"username": username})
                if len(result) == 0:
                    success = False
                    message = "用户名不存在"
                else:
                    if password != result[0]['password']:
                        success = False
                        message = "密码不正确"
        data = {
            "success": success,
            "message": message
        }
        print(data)
        return jsonify(data)


# 注册函数
@app.route("/api/upload/signUp", methods=['GET', 'POST'])
def sign_up():
    success = True
    message = ""
    if request.method == 'GET':
        username = request.form['username']
        password = request.form['password']
        dataClient = pymongo.MongoClient('mongodb://localhost:27017/')
        if "citidb" not in dataClient.list_database_names():
            success = False
            message = "数据库不存在"
        else:
            db = dataClient['citidb']
            if 'user' not in db.list_collection_names():
                success = False
                message = "用户表不存在"
            else:
                collection = db['user']
                insertData = {"username": username, "password": password}
                result = collection.find({"username": username})
                if len(result) != 0:
                    success = False
                    message = "用户名已存在"
                else:
                    collection.insert_one(insertData)
        data = {
            "success": success,
            "message": message
        }
        return jsonify(data)


if __name__ == '__main__':
    # 与axios配置对应
    app.run(host="localhost", port='8080')
