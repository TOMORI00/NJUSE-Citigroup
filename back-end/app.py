from flask import Flask
import main
import json

#gy
from flask import make_response , send_file
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])


#why
@app.route('/')
def hello():
    return 'Welcome to my watchlist'


# zym return
@app.route('/test')
def test():
    main.fun()     # 开始运行
   

    success = True
    message = ""

    date = main.date_re    # 复现周期 即x轴开始和结束的时间

    chart1, chartadd1, in1, duration, chart2_high, chart2_mid, chart2_low, chartadd2_high, chartadd2_mid, chartadd2_low, in2_high, in2_mid, in2_low, in3_high, in3_mid, in3_low= main.fun()
    
    data = {"success": success,"message":message, "date":date, "chart1":chart1, "chartadd1":chartadd1, "in1":in1,
    "duration":duration,
    "chart2_high":chart2_high, "chart2_mid":chart2_mid, "chart2_low":chart2_low,
    "chartadd2_high":chartadd2_high, "chartadd2_mid":chartadd2_mid, "chartadd2_low":chartadd2_low,
    "in2_high":in2_high, "in2_mid":in2_mid, "in2_low":in2_low,
    "in3_high":in3_high, "in3_mid":in3_mid, "in3_low":in3_low}
    
    return json.dumps(data)



#gy
#@app.route('/haha')
#def haha():
#    return 'Hello World!'

#gy download
@app.route('/testdownload', methods=['GET'])
def testdownload():
    response = make_response(send_file("demo.docx"))
    response.headers["Content-Disposition"] = "attachment; filename=demo.docx;"
    return response

#gy
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#gy upload
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join("/Users/guyi/Desktop/repoo", filename))
            file.save(os.path.join("C:/Users/zym0325/Desktop", filename))   
            return "fine"
    return render_template('gui_data.html')
