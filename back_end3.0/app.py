from flask import Flask
from financial_products_viewer import main
from fund_viewer import main_fv
from flask import jsonify

import json

app = Flask(__name__)


#gy
from flask import make_response , send_file
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])


#why
@app.route('/')
def hello():
    return 'Welcome to my watchlist'






# zym return       
# input 基金 fund_viewer main_fv.py
@app.route('/test_fv')
def test_fv():


    success = True
    message = ""


    date_re, chart1, chartadd1, in1, duration, chart2_high, chart2_mid, chart2_low, chartadd2_high, chartadd2_mid, chartadd2_low, in2_high, in2_mid, in2_low, history_high, history_mid, history_low = main_fv.fun()


    #历史推荐投资组合先存入history.txt
    history_high = str(history_high) + "\n"
    history_mid = str(history_mid) + "\n"
    history_low = str(history_low) + "\n"
    history = [history_high,history_mid,history_low]

    f = open("history.txt", 'w').close()   #先清空
    f = open('history.txt','a')
    f.writelines(history)
    f.close()

    data = {
        "success": success,
        "message":message, 
        "content":{
            "date":date_re, "chart1":chart1, "chartadd1":chartadd1, "in1":in1,
            "duration":duration,
            "chart2_high":chart2_high, "chart2_mid":chart2_mid, "chart2_low":chart2_low,
            "chartadd2_high":chartadd2_high, "chartadd2_mid":chartadd2_mid, "chartadd2_low":chartadd2_low,
            "in2_high":in2_high, "in2_mid":in2_mid, "in2_low":in2_low
        }
    }

    return jsonify(data)
    #test_data.append(3)
    #test_data.append(9)

    #return "heihei"



# zym
# input 理财 financial_products_viewer main.py
@app.route('/test_fpv')  
def test_fpv():
    

    success = True
    message = ""

    date_re, chart1, in1, duration, chart2_high, chart2_mid, chart2_low, chartadd2_high, chartadd2_mid, chartadd2_low, in2_high, in2_mid, in2_low, history_high,history_mid,history_low = main.fun()

    #历史推荐投资组合先存入history.txt
    history_high = str(history_high) + "\n"
    history_mid = str(history_mid) + "\n"
    history_low = str(history_low) + "\n"
    history = [history_high,history_mid,history_low]

    f = open("history.txt", 'w').close()   #先清空
    f = open('history.txt','a')
    f.writelines(history)
    f.close()

    data = {
        "success": success,
        "message":message, 
        "content":{
            "date":date_re, "chart1":chart1, "in1":in1,
            "duration":duration,
            "chart2_high":chart2_high, "chart2_mid":chart2_mid, "chart2_low":chart2_low,
            "chartadd2_high":chartadd2_high, "chartadd2_mid":chartadd2_mid, "chartadd2_low":chartadd2_low,
            "in2_high":in2_high, "in2_mid":in2_mid, "in2_low":in2_low
        }
    }

    return jsonify(data)



# zym
# 推荐组合及历史推荐组合 请注意先经过test_fv或test_fpv才能得到组合数据
@app.route('/getChart')
def test_chart():
    f = open("history.txt","r")
    history = f.readlines()
    f.close()
    history[0] = history[0].rstrip('\n') 
    history[1] = history[1].rstrip('\n') 
    history[2] = history[2].rstrip('\n') 
    
    success = True
    message = ""

    data_chart = {
        "success":success,
        "message":message,
        "content":{
            "history_high":history[0], "history_mid":history[1],"history_low":history[2]
        }
    }

    return jsonify(data_chart)
    #data_chart = {"history_high":history_high, "history_mid":history_mid,"history_low":history_low}
    #return json.dumps(data_chart)




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