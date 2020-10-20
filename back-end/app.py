from flask import Flask, jsonify
from flask_cors import CORS

import main
import json

# gy
from flask import make_response, send_file
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
# 跨域
CORS(app, supports_credentials=True)
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])


# why
@app.route('/')
def hello():
    return 'Welcome to my watchlist'


# zym return
@app.route('/api/output/getData')
def get_data():
    main.fun()  # 开始运行

    success = True
    message = ""

    date = main.date_re  # 复现周期 即x轴开始和结束的时间

    chart1, chartadd1, in1, duration, chart2_high, chart2_mid, chart2_low, chartadd2_high, chartadd2_mid, chartadd2_low, in2_high, in2_mid, in2_low, in3_high, in3_mid, in3_low = main.fun()

    data = {"success": success,
            "message": message,
            "content":
                {
                    "date": date, "chart1": chart1, "chartadd1": chartadd1, "in1": in1,
                    "duration": duration,
                    "chart2_high": chart2_high, "chart2_mid": chart2_mid, "chart2_low": chart2_low,
                    "chartadd2_high": chartadd2_high, "chartadd2_mid": chartadd2_mid, "chartadd2_low": chartadd2_low,
                    "in2_high": in2_high, "in2_mid": in2_mid, "in2_low": in2_low,
                    "in3_high": in3_high, "in3_mid": in3_mid, "in3_low": in3_low
                }
            }

    print('finish')
    return jsonify(data)


# gy
# @app.route('/haha')
# def haha():
#    return 'Hello World!'

# gy download
@app.route('/download', methods=['GET'])
def download():
    response = make_response(send_file("demo.docx"))
    response.headers["Content-Disposition"] = "attachment; filename=demo.docx;"
    return response


# gy
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# gy upload
# 上传excel文件到input中
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join("/Users/guyi/Desktop/repoo", filename))
            file.save(os.path.join("input", filename))
            return "fine"
    return render_template('gui_data.html')


@app.route("/api/upload/uploadExcel", methods=['GET', 'POST'])
def uploadExcel():
    success = False
    message = "上传失败"
    print("uploadExcel")
    if request.method == 'POST':
        file = request.files['files']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("input", filename))
            success = True
            message = ''
    data = {"success": success,
            "message": message,
            "content": ''
            }
    return jsonify(data)


@app.route("/api/output/getChart", methods=['GET', 'POST'])
def get_chart():
    success = True
    message = ""
    data = {
        "success": success,
        "message": message,
        "content": "/TODO this is a Chart"
    }
    return jsonify(data)


@app.route("/api/output/getPDF", methods=['GET', 'POST'])
def get_pdf():
    success = True
    message = ""
    data = {
        "success": success,
        "message": message,
        "content": "/TODO this is a PDF"
    }
    return jsonify(data)


if __name__ == '__main__':
    # 与axios配置对应
    app.run(host="localhost", port='8080')
