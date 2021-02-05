# -*- coding: utf-8 -*-
"""
Created on Fri May 22 19:38:52 2020

@author: Cheng
"""

import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from jqdatasdk import finance
from jqdatasdk import *
from sqlalchemy import *
import dateutil
import numpy as np
from datetime import timedelta
import random

from . import backtest as bt
from . import portfolio_construction as pc
from . import write_docx as wd

import warnings

warnings.filterwarnings('ignore')

auth('13739188902', 'ZNnb20160801')


# zym 

date_re = ["0","0"]



def buy(buy_w, w, data, date, money, asset, rate = 0, rate_cost = 0, add_money = 0):
    hold = 0
    #print(buy_w)
    # for code in buy_w.index:
    #     close = data.loc[date, code]
    #     close = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code,finance.FUND_NET_VALUE.day == date))
    #     if close.empty:
    #         buy_w = buy_w.drop(code)
    #         buy_w = buy_w * (1 / np.sum(w))
    #         continue
    total_cost = 0
    #print(date, money, asset, add_money)
    for code in buy_w.index:
        #close = float(finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code,finance.FUND_NET_VALUE.day == date))['refactor_net_value'])
        close = data.loc[date, code]
        cost = add_money * float(buy_w.loc[code])
        total_cost += cost
        wb = cost * (1-rate) / close
        if w.get(code):
            w[code] += wb
        else:
            w[code] = wb
        rate_cost += close * w[code] * rate
    if money >= total_cost:
        money -= total_cost
    else:
        asset += total_cost - money
        money = 0
    #money -= total_cost
    for code in w.keys():
        close = data.loc[date, code]
        hold += close * w[code]
    tmp = pd.DataFrame({'p': (hold + money) / asset}, index=pd.Index(data=[date,]))
    #print(asset, hold, money, w)
    return w, money, tmp, rate_cost, asset


def sell(sell_w, w, data, date, money, asset, rate = 0):
    hold = 0
    sold_money = 0
    for code in sell_w.keys():
        close = data.loc[date, code]
        tmp = sell_w[code]
        w[code] = w[code] - tmp
        money += close * tmp * (1 - rate)
        sold_money += close * tmp * (1 - rate)
    for code in w.keys():
        #close = float(finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code,finance.FUND_NET_VALUE.day == date))['refactor_net_value'])
        close = data.loc[date, code]
        hold += w[code] * close
    tmp = pd.DataFrame({'p': (hold + money) / asset}, index=pd.Index(data=[date,]))
    #print(sell_w, w, money, hold, asset)
    return w, money, tmp, sold_money


def nochange(w, data, date, money, asset):
    hold = 0
    for code in w.keys():
        #close = float(finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code,finance.FUND_NET_VALUE.day == date))['refactor_net_value'])
        close = data.loc[date, code]
        hold += close * w[code]
    tmp = pd.DataFrame({'p': (hold + money) / asset}, index=pd.Index(data=[date,]))
    #print(asset, hold, money, cost)
    return tmp


# def nochange_finance_products(w_finance_products,date,money,cost,yrate=0.036):
#     drate=yrate/250
#     w_finance_products += cost*drate
#     tmp = pd.DataFrame({'p': (w_finance_products + money) / cost}, index=pd.Index(data=[date,]))
#     return tmp,w_finance_products


# def buy_finance_products(buy_f,w_finance_products,date, money, cost, principal, r_list):
#     yrate=0.036 # 理财产品年化利率
#     drate=yrate/250
    
#     w_finance_products+= principal*drate+buy_f
#     cost+=buy_f
#     principal+=buy_f
    
#     tmp = pd.DataFrame({'p': (w_finance_products + money) / cost}, index=pd.Index(data=[date,]))
#     return cost,w_finance_products,tmp,principal


# def sell_finance_products(sell_f,w_finance_products,money,principal):
#     w_finance_products-=sell_f
#     money+=sell_f
#     principal-=sell_f
#     tmp = pd.DataFrame({'p': (money+w_finance_products) / cost}, index=pd.Index(data=[date,]))
#     return w_finance_products,money,tmp,principal


def nochange_finance_products(w, w_finance_products,date,money,cost,yrate):
    for code in w.keys():
        drate = yrate[code]/250
        w_finance_products[code] += w[code]*drate
    tmp = pd.DataFrame({'p': (sum(w_finance_products.values()) + money) / cost}, index=pd.Index(data=[date,]))
    return tmp,w_finance_products


def buy_finance_products(buy_f,w,w_finance_products,date, money, cost, yrate):
    #print(date,money,cost,w_finance_products)
    for code in buy_f:
        if w.get(code):
            w[code] += buy_f[code]
        else:
            w[code] = buy_f[code]
            w_finance_products[code] = buy_f[code]
        #cost += buy_f[code]
        if money >= buy_f[code]:
            money -= buy_f[code]
        else:
            cost += buy_f[code] - money
            money = 0
    for code in w.keys():
        drate = yrate[code]/250
        w_finance_products[code] += w[code]*drate
    #print(date,money,cost,w_finance_products)
    tmp = pd.DataFrame({'p': (sum(w_finance_products.values()) + money) / cost}, index=pd.Index(data=[date,]))
    return w, cost,w_finance_products,tmp, money


def sell_finance_products(sell_f,w, w_finance_products,money, cost, yrate,date):
    for code in sell_f:
        money += w_finance_products[code] * sell_f[code] / w[code]
        w_finance_products[code] -= w_finance_products[code] * sell_f[code] / w[code]
        w[code] -= sell_f[code]
    for code in w.keys():
        drate = yrate[code]/250
        w_finance_products[code] += w[code]*drate
    tmp = pd.DataFrame({'p': (money+sum(w_finance_products.values())) / cost}, index=pd.Index(data=[date,]))
    #print(date,money)
    return w, w_finance_products,money,tmp


def get_fund_data(start_date, end_date, w):
    codes = list(w.index)
    #print(w)
    data = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(codes),
                                                                  finance.FUND_NET_VALUE.day >= start_date,
                                                                  finance.FUND_NET_VALUE.day <= end_date))

    value = data.reset_index().pivot("day", "code", "refactor_net_value")
    value.fillna(method='backfill', inplace=True)
    value.fillna(method='ffill', inplace=True)
    return value


def get_quarter_date(date):
    quarter = (date.month - 1) // 3 + 1
    first_date = datetime(date.year, quarter*3-2, 1)
    return first_date.date()


def revise_w_gao(buy_w, limit):
    w = buy_w.copy()
    change = 0
    while min(w.weights) < limit or change != 0:
        for code in w.index:
            if w.loc[code, 'weights'] < limit:
                change += limit - w.loc[code, 'weights']
                w.loc[code, 'weights'] = limit
            elif w.loc[code, 'weights'] > limit:
                w.loc[code, 'weights'] -= change
                change = 0
    return w


def revise_w(buy_w, filename, limit):
    with open(filename, 'r') as f:
        codes = f.readlines()
        codes = [code.strip() for code in codes]
    if codes == []:
        return buy_w
    i = random.randint(0,len(codes)-1)
    code = codes[i]
    # with open(filename, 'r') as f:
    #     code = f.readline().strip()
    buy_w.loc[code, 'weights'] = limit / (1-limit)
    buy_w = buy_w * (1 / np.sum(buy_w))
    return buy_w


def draw_finance(c, filename):            #zym 画图1
    plt.rcParams['figure.figsize'] = (20, 10)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(c, color='darkgrey')
    plt.savefig(filename)
    #plt.show()
    plt.close()

def draw_profits(a, c, r, filename,profit=0,maxloss=0, dates = []):          #zym 画图2
    plt.rcParams['figure.figsize'] = (20, 10)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(a, color='red')
    ax.plot(c, color='darkgrey')
    ax.set_title(r)
    for date in dates:
        ax.vlines(date, min(min(c.p),min(a.p)), max(max(c.p),max(a.p)), colors = "grey", linestyles = "dashed")
    if profit!=0 and maxloss!=0:
        ax.set_xlabel('profit:'+str(round(profit/10000,2))+', loss:'+str(round(maxloss/10000,2))+'(ten thousand)')
    #plt.legend()
    plt.savefig(filename)
    #plt.show()
    plt.close()

def draw_w(buy_w, filename):
    plt.rcParams['figure.figsize'] = (20, 10)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    #plt.figure(figsize=(8, 9), dpi=300)  # 以上代码为画图初始化设置
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for i in range(len(buy_w)):
        buy_w.iloc[i,0] = float(buy_w.iloc[i,0])
    labels = list(buy_w.index)  # 标签，即种类
    sizes = list(buy_w.iloc[:, 0] * 1000)  # 比例
    # Colors used. Recycle if not enough.
    colors = ['#eaff56', '#ff7500', '#f9906f', '#44cef6', '#cca4e3', '#ff03a7']  # 设置颜色（循环显示）
    # For China, make the piece explode a bit
    expl = np.ones(labels.__len__()) * 0.05
    # expl[results.iloc[:,0].values.argmax()]=0.1    # 第一块即China离开圆心0.1

    patches, l_text, p_text = ax.pie(sizes, explode=expl, labels=labels, rotatelabels=True, colors=colors,
                                      autopct='%1.2f%%',
                                      shadow=False, labeldistance=0.6, pctdistance=0.4,
                                      textprops={'fontsize': 12, 'color': '#065279'})  # 画图函数
    # 图例中加上百分比信息
    sizes = [float("%.2f" % (x / sum(sizes) * 100)) for x in sizes]
    pct = [str(x) + "%" for x in sizes]
    labels = [labels[i] + "-" + pct[i] for i in range(len(pct))]
    ax.legend(handles=patches, labels=labels, ncol=3, loc="best", mode="expand", framealpha=0, fontsize=12,
                title=None)
    ax.set_title('Fund Portfolio', fontsize=20, fontweight='black', color='#065279')
    ax.axis('equal')  # 让保持圆形
    #ax.annotate(details, xy=(0, 0), xytext=(-1, -1.2), color='#065279', size=13)
    plt.savefig(filename)
    #plt.show()
    plt.close()


#zym
def findPeriod_HM(test_year,test_month):
    find_year = 0
    find_period = 0
    if(test_year == 2017 and 1<= test_month <= 11):
        find_year = 2017
        find_period = 1
    elif(test_year == 2017 and test_month == 12):
        find_year = 2017
        find_period = 12
    elif(test_year == 2018 and 1<= test_month <=10):
        find_year = 2017
        find_period = 12
    elif(test_year == 2018 and 11<=test_month<=12):
        find_year = 2018
        find_period = 11
    elif(test_year == 2019 and 1<=test_month <=9):
        find_year = 2018
        find_period = 11
    elif(test_year == 2019 and 10 <= test_month <=12):
        find_year = 2019
        find_period = 10
    elif(test_year == 2020 and 1<= test_month <=8):
        find_year = 2019
        find_period = 10
    elif(test_year == 2020 and test_month >=9):
        find_year = 2020
        find_period = 9
    return find_year, find_period


def findPeriod_L(test_year,test_month):
    find_year = 0
    find_period = 0
    if(test_year == 2017 and 1<= test_month <= 7):
        find_year = 2017
        find_period = 1
    elif(test_year == 2017 and 8<= test_month <= 12):
        find_year = 2017
        find_period = 8
    elif(test_year == 2018 and 1<= test_month <=2):
        find_year = 2017
        find_period = 8
    elif(test_year == 2018 and 3<=test_month<=9):
        find_year = 2018
        find_period = 3
    elif(test_year == 2018 and 10<=test_month <=12):
        find_year = 2018
        find_period = 10
    elif(test_year == 2019 and 1 <= test_month <=4):
        find_year = 2018
        find_period = 10
    elif(test_year == 2019 and 5<= test_month <=11):
        find_year = 2019
        find_period = 5
    elif(test_year == 2019 and test_month == 12):
        find_year = 2019
        find_period = 12
    elif(test_year == 2020 and 1<= test_month <=6):
        find_year = 2019
        find_period = 12
    elif(test_year == 2020 and test_month >=7):
        find_year = 2020
        find_period = 7
    return find_year, find_period



#zym
def round_2(w):
    length = len(w['weights']) 
    sum = 0
    for i in range(length-1):
        w.weights[i] = float(w.weights[i])
        w.weights[i] = round(w.weights[i],2)
        sum = sum + w.weights[i]
    w.weights[length-1] = 1-sum
    w.weights[length-1] = round(w.weights[length-1],2)
    return w




def fun():
    #pmonth = [6, 12]
    pmonth = [11,11]   #zym
    fun = ['md', 'rmd']
    gd = ['高风险', '中风险']


    #zym 历史推荐投资组合

    #history_quarter = [datetime(2015, 2, 15, 12, 20),datetime(2015, 5, 15, 12, 20),datetime(2015, 8, 15, 12, 20),datetime(2015, 10, 15, 12, 20), datetime(2016, 2, 15, 12, 20),datetime(2016, 5, 15, 12, 20),datetime(2016, 8, 15, 12, 20),datetime(2016, 10, 15, 12, 20),datetime(2017, 2, 15, 12, 20),datetime(2017, 5, 15, 12, 20),datetime(2017, 8, 15, 12, 20),datetime(2017, 10, 15, 12, 20),datetime(2018, 2, 15, 12, 20),datetime(2018, 5, 15, 12, 20),datetime(2018, 8, 15, 12, 20),datetime(2018, 10, 15, 12, 20),datetime(2019, 2, 15, 12, 20),datetime(2019, 5, 15, 12, 20),datetime(2019, 8, 15, 12, 20),datetime(2019, 10, 15, 12, 20),datetime(2020, 2, 15, 12, 20),datetime(2020, 5, 15, 12, 20),datetime(2020, 8, 15, 12, 20),datetime(2020, 10, 15, 12, 20) ]
    history_high = []  # 高风险历史投资组合
    history_mid = []   # 中
    history_low = []   #低

    history_high_quarter = [datetime(2017,3,25,12,20),datetime(2018,3,25,12,20),datetime(2019,3,25,12,20),datetime(2020,3,25,12,20),datetime(2020,10,14,12,20)]
    history_mid_quarter = [datetime(2017,3,25,12,20),datetime(2018,3,25,12,20),datetime(2019,3,25,12,20),datetime(2020,3,25,12,20),datetime(2020,10,14,12,20)]
    history_low_quarter = [datetime(2017,3,25,12,20),datetime(2017,9,14,12,20),datetime(2018,3,25,12,20),datetime(2018,10,25,12,20),datetime(2019,5,26,12,20),datetime(2020,3,25,12,20),datetime(2020,10,14,12,20)]


    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'input')):
        for z in range(0,len(files), 2):
            filename = files[z]
            sellfilename = files[z+1]
            buydata = pd.read_excel(os.path.join(os.path.dirname(__file__), 'input', filename), dtype=str)
            #buydata = buydata[:-1]
            buydata = buydata.sort_values(by="购买时间" , ascending=True)
            buydata['购买时间'] = '20' + buydata['购买时间']
            #data['基金代码']=[str(i).zfill(6) for i in data['基金代码']]
            for index in buydata.index:
                #data.rename(index=str.zfill(7))
                t = datetime.strptime(buydata.loc[index, '购买时间'], "%Y%m%d")
                buydata.loc[index, '购买时间'] = get_trade_days(start_date=t)[0]
            buydata.index = pd.to_datetime(buydata['购买时间'])
 
            selldata = pd.read_excel(os.path.join(os.path.dirname(__file__), 'input', sellfilename), dtype=str)
            if not selldata.empty:
                #selldata = selldata[:-1]
                selldata = selldata.sort_values(by="赎回或到期时间" , ascending=True)
                selldata['赎回或到期时间'] = '20' + selldata['赎回或到期时间']
                #data['基金代码']=[str(i).zfill(6) for i in data['基金代码']]
                for index in selldata.index:
                    #data.rename(index=str.zfill(7))
                    t = datetime.strptime(selldata.loc[index, '赎回或到期时间'], "%Y%m%d")
                    selldata.loc[index, '赎回或到期时间'] = get_trade_days(start_date=t)[0]
                    selldata.loc[index, '赎回金额'] = float(selldata.loc[index, '赎回或到期份额'])*(1+float(selldata.loc[index, '年化收益率']))

                selldata.index = pd.to_datetime(selldata['赎回或到期时间'])
                
                
            today = datetime.today()
            sd = buydata.index[0]
            print("sd")
            print(sd)
            date_re[0] = sd.date().__str__()   # zym return
            ed = today.date()        # why 
            #-----------------
            #ed = datetime(2020, 10, 15, 12, 20).date()
            date_re[1] = today.date().__str__() # zym return
            dates = get_trade_days(start_date=buydata.index[0], end_date=ed)[:-1]
            
            
            w_finance_products={}
            cost = 0
            money = 0
            profit2 = pd.DataFrame()
            value_df2=pd.DataFrame()
            w = {}
            yrate={}
            i = 0
            s = 0
            
            for date in dates:
                flag = True
                if s < len(selldata) and selldata.index[s].date() == date:
                    tmpdata = selldata.loc[date, :]
                    sell_f = {}
                    if tmpdata.index[0]=='产品名称':
                        sell_f[selldata.loc[date, '产品名称']] = float(selldata.loc[date, '赎回或到期份额'])
                        s += 1
                    else:
                        for j in range(len(tmpdata)):
                            sell_f[tmpdata.iloc[j, 0]] = float(tmpdata.iloc[j, 1])
                        s += len(tmpdata)
                    rate = 0.005
                    w, w_finance_products,money,tmp=sell_finance_products(sell_f,w, w_finance_products,money, cost, yrate,date)
                    flag = False
                if i < len(buydata) and buydata.index[i].date() == date:
                    tmpdata = buydata.loc[date, :]
                    buy_f = {}
                    if tmpdata.index[0]=='产品名称':
                        buy_f[buydata.loc[date, '产品名称']]= float(buydata.loc[date, '购买金额'])
                        i+=1
                        yrate[buydata.loc[date, '产品名称']]=float(buydata.loc[date, '年化收益率'])
                    else:
                        for j in range(len(tmpdata)):
                            buy_f[tmpdata.iloc[j, 0]] = float(tmpdata.iloc[j, 1])
                            yrate[tmpdata.iloc[j, 0]] = float(tmpdata.iloc[j, -1])
                        i+=len(add)
                    w,cost,w_finance_products,tmp,money=buy_finance_products(buy_f,w,w_finance_products, date, money, cost,yrate)
                    flag = False
                if flag:
                    # tmp = nochange2(data, w, date, money, cost)
                    tmp,w_finance_products=nochange_finance_products(w,w_finance_products,date,money,cost,yrate)
                profit2 = pd.concat([profit2, tmp])
                #print(date,cost,principal,w_finance_products)
            profit_f=sum(w_finance_products.values())+money-cost
                    
            figname2 = os.path.join(os.path.dirname(__file__), 'figure', filename[:-5]+ '.png')
            draw_finance(profit2, figname2)
            result,maxloss = bt.get_result(profit2, 0.03)
            p_per2 = result['r']
            















            # ----------------------
            # difengxian
            start_dates = []
            date = buydata.index[0].date()
            while date < today.date():
                date = get_trade_days(start_date=date)[0]
                start_dates.append(date)
                date += dateutil.relativedelta.relativedelta(months=7)    #zym
            start_dates.append(today.date())
            w = {}
            cost = 0
            asset = 0
            money = 0
            rate_cost = 0
            sold_money = 0
            profit = pd.DataFrame()
            value_df = pd.DataFrame()
            i = 1
            end_date = get_trade_days(end_date=start_dates[1] + timedelta(-1) , count=1)[0]
            data = pd.DataFrame()
            for date in dates:
                flag = True
                if date in selldata.index:
                    ori_asset = asset
                    minus = selldata.loc[date, '赎回金额']
                    m = 0
                    if type(minus) == np.float64:
                        # asset -= float(minus)
                        # money -= float(minus)
                        m += float(minus)
                    else:
                        for j in range(len(minus)):
                            # asset -= float(minus.iloc[j])
                            # money -= float(minus.iloc[j])
                            m += float(minus.iloc[j])
                    rate = 0.005
                    sell_w = {}
                    for code in w.keys():
                        sell_w[code] = w[code] * min(m/ori_asset, 1)
                    w, money, tmp, sold_money = sell(sell_w, w, data, date, money, asset, rate)
                    sold_money = 0
                    #print('sell',date,money)
                    flag = False
                if date == end_date:
                    rate = 0.005
                    sell_w = w.copy()
                    w, money, tmp, sold_money = sell(sell_w, w, data, date, money, asset, rate)
                    #print('sell',date,w)
                    flag = False
                if date in buydata.index:
                    add = buydata.loc[date, '购买金额']
                    add_money = 0
                    if type(add) == str:
                        add_money = float(add)
                        # asset += float(add)
                        # money += float(add)
                    else:
                        for j in range(len(add)):
                            add_money += float(add.iloc[j])
                            # asset += float(add.iloc[j])
                            # money += float(add.iloc[j])
                    rate = 0.015
                    start_date = start_dates[0]
                    first_date = get_quarter_date(start_date)
                    end_date = get_trade_days(end_date=start_dates[i] + timedelta(-1) , count=1)[0]
                    quarter = (date.month - 1) // 3 + 1

                    #zym
                    test_year = date.year
                    test_month = date.month
                    find_year,find_period = findPeriod_L(test_year,test_month)


                    buy_w_filename = os.path.join(os.path.dirname(__file__), 'tmp','L'+ str(find_year)+'-'+str(find_period)+'.csv')
                    if os.path.exists(buy_w_filename):
                        buy_w = pd.read_csv(buy_w_filename, dtype=object)
                        buy_w.set_index('Unnamed: 0',inplace=True)
                    else:
                        buy_w = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.9, fund_pool_size=100, fund_pool_update=True,
                                          fund_nav_update=True, end_date=first_date, max_num=2, risk_aversion=3, fund_pool_funs=['rmd'],
                                          fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(date.year)+'_'+str(quarter)+'.txt'))
                        low_limit = random.randint(int(85),int(92)) / 100
                        buy_w = revise_w(buy_w, os.path.join(os.path.dirname(__file__),'funds',str(today.year)+'_'+str(quarter)+'_low.txt'), low_limit)
                        buy_w.to_csv(buy_w_filename)
                    tdata = get_fund_data(start_dates[0], start_dates[-1], buy_w)
                    if data.empty:
                        data = tdata
                    else:
                        cols_to_use = set(data.columns) - set(tdata.columns)
                        data = pd.merge(data[cols_to_use], tdata, left_index=True, right_index=True, how='outer')
                    w, money, tmp, rate_cost, asset = buy(buy_w, w, data, date, money, asset, rate, rate_cost, add_money)
                    #print('buy',date)
                    flag = False
                if i+1 < len(start_dates) and date == start_dates[i]:
                    rate = 0.015
                    start_date = start_dates[i]
                    first_date = get_quarter_date(start_date)
                    end_date = get_trade_days(end_date=start_dates[i+1] + timedelta(-1) , count=1)[0]
                    i += 1
                    quarter = (date.month - 1) // 3 + 1

                    test_year = date.year
                    test_month = date.month
                    find_year,find_period = findPeriod_L(test_year,test_month)


                    buy_w_filename = os.path.join(os.path.dirname(__file__), 'tmp','L'+str(find_year)+'-'+str(find_period)+ '.csv')
                    if os.path.exists(buy_w_filename):
                        buy_w = pd.read_csv(buy_w_filename, dtype=object)
                        buy_w.set_index('Unnamed: 0',inplace=True)
                    else:
                        buy_w = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.9, fund_pool_size=100, fund_pool_update=True,
                                          fund_nav_update=True, end_date=first_date, max_num=2, risk_aversion=3, fund_pool_funs=['rmd'],
                                          fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(date.year)+'_'+str(quarter)+'.txt'))
                        low_limit = random.randint(int(85),int(92)) / 100
                        buy_w = revise_w(buy_w, os.path.join(os.path.dirname(__file__),'funds',str(today.year)+'_'+str(quarter)+'_low.txt'), low_limit)
                        buy_w.to_csv(buy_w_filename)
                    tdata = get_fund_data(start_dates[0], start_dates[-1], buy_w)
                    if data.empty:
                        data = tdata
                    else:
                        cols_to_use = set(data.columns) - set(tdata.columns)
                        data = pd.merge(data[cols_to_use], tdata, left_index=True, right_index=True, how='outer')
                    w, money, tmp, rate_cost, asset = buy(buy_w, w, data, date, money, asset, rate, rate_cost, sold_money)
                    #print('buy',date)
                    flag = False
                if flag:
                    tmp = nochange(w, data, date, money, asset)
                profit = pd.concat([profit, tmp])

                # 市值
                total_value=0 # 今日总市值
                for code,value in w.items():
                    close = data.loc[date, code]
                    total_value += close*value
                if total_value!=0:
                    temp = pd.DataFrame({'value': total_value+money}, index=pd.Index(data=[date,]))
                    value_df=pd.concat([value_df,temp])
            #print(asset)     
            value_list=list(value_df.value)
            result,maxloss = bt.get_result(profit, 0.03,value_list)
            #draw(buy_w, profit, profit2[:-1], result, 'result\\' +filename[:-5] + '低风险组合' + '.png', value_list[-1]-asset, maxloss, start_dates[:-1])
            #draw(profit, profit2[:-1], result, 'result\\' +filename[:-5] + '_low' + str(low_limit) + '_' + str(pmonth[d]) + '_' + fun[d] + '.png', value_list[-1]-asset, maxloss)


            figname_l = os.path.join(os.path.dirname(__file__), 'figure', filename[:-5]+'_low.png')
            draw_profits(profit, profit2, result, figname_l, value_list[-1]-asset, maxloss, dates = start_dates[:-1])  #zym

            p_per_l = result['r']
            p_money_l = p_per_l*asset
            md_l = result['md']
            
            piename = os.path.join(os.path.dirname(__file__), 'figure' ,filename[:-5]+ '_pie.png')
            

            #zym 低风险 历史

      
            for t in range(7):

                test_it = history_low_quarter[t]
                test_year = test_it.year
                test_month = test_it.month
                find_year,find_period = findPeriod_L(test_year,test_month)
    
                test_quarter = (test_it.month -1) //3 +1
                test_date = get_quarter_date(test_it)
                buy_w_test_filename =os.path.join(os.path.dirname(__file__),'tmp','L'+str(find_year)+'-'+str(find_period)+ '.csv')
                if os.path.exists(buy_w_test_filename):
                    buy_w_test = pd.read_csv(buy_w_test_filename, dtype=object)
                    buy_w_test.set_index('Unnamed: 0',inplace=True)
                else:
                    buy_w_test = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.9, fund_pool_size=100, fund_pool_update=True,
                                          fund_nav_update=True, end_date=test_date, max_num=2, risk_aversion=3, fund_pool_funs=['rmd'],
                                          fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(test_year)+'_'+str(test_quarter)+'.txt'))
                    low_limit = random.randint(int(85),int(92)) / 100
                    buy_w_test = revise_w(buy_w_test, os.path.join(os.path.dirname(__file__),'funds',str(test_year)+'_'+str(test_quarter)+'_low.txt'), low_limit)


                #print(buy_w_test)

                #zym
                namei = []
                length = len(buy_w_test['weights']) 
                for i in range(0,length):
                    nametmp = finance.run_query(query(finance.FUND_MAIN_INFO).filter(finance.FUND_MAIN_INFO.main_code==buy_w_test.index[i]))['name']
                    nametmp = str(nametmp[0])
                    namei.append(nametmp)
                    #stri=w.index[i]+name[0]+'——'+str(round(float(w.iloc[i][0])*100))+'万'


                buy_w_test = round_2(buy_w_test) 
                labels_low = list(buy_w_test.index)
                names_low = namei
                sizes_low = list(buy_w_test.weights)
                pt_low = [find_year, find_period, labels_low, names_low, sizes_low] 
                history_low.append(pt_low)




            t_quarter = (today.month - 1) // 3 + 1
            t_date = get_quarter_date(today)

            test_year = today.year
            test_month = today.month
            find_year,find_period = findPeriod_L(test_year,test_month)



            buy_w_filename = os.path.join(os.path.dirname(__file__), 'tmp','L'+str(find_year)+'-'+str(find_period)+ '.csv')
            if os.path.exists(buy_w_filename):
                buy_w = pd.read_csv(buy_w_filename, dtype=object)
                buy_w.set_index('Unnamed: 0',inplace=True)
            else:
                buy_w = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.9, fund_pool_size=100, fund_pool_update=True,
                                          fund_nav_update=True, end_date=t_date, max_num=2, risk_aversion=3, fund_pool_funs=['rmd'],
                                          fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(today.year)+'_'+str(t_quarter)+'.txt'))
                low_limit = random.randint(int(85),int(92)) / 100
                buy_w = revise_w(buy_w, os.path.join(os.path.dirname(__file__),'funds',str(today.year)+'_',str(quarter)+'_low.txt'), low_limit)
                buy_w.to_csv(buy_w_filename)
            

            buy_w = round_2(buy_w)

            draw_w(buy_w, piename)
            wd.write_docx(filename[:-5], sd, '低风险','7个月', figname2, p_per2, profit_f, figname_l, p_per_l, p_money_l, md_l, piename, buy_w)
            
            
            #zym
            #names_low = []
            #length=len(buy_w['weights']) 
            #for i in range(0,length):
                #nametmp = finance.run_query(query(finance.FUND_MAIN_INFO).filter(finance.FUND_MAIN_INFO.main_code==buy_w.index[i]))['name']
                #nametmp = str(nametmp[0])
                #names_low.append(nametmp)
                #stri=w.index[i]+name[0]+'——'+str(round(float(w.iloc[i][0])*100))+'万'

            #zym

            r2_re = result['r']
            sharpe2_re = result['sharpe']
            md2_re = result['md']
            rmd2_re = result['r/md']
            prof2_re = str(round((value_list[-1]-asset)/10000,2))
            loss2_re = str(round(maxloss/10000,2))

            chartadd2_low = []
            chartadd2_low.append(r2_re)
            chartadd2_low.append(sharpe2_re)
            chartadd2_low.append(md2_re)
            chartadd2_low.append(rmd2_re)
            chartadd2_low.append(prof2_re)
            chartadd2_low.append(loss2_re)

            sy2_re = str(round(result['r']*100,2))
            sy20_re = str(round(result['r']*asset/10000))
            sycompare2_re = wd.change(profit_f, result['r']*asset)

            hc20_re = str(round(result['md']*100,2))

            in2_low = [] 
            in2_low.append(sy2_re)
            in2_low.append(sy20_re) 
            in2_low.append(sycompare2_re)
            in2_low.append(hc20_re)

            profit_low = profit






            #zym

            chartadd2_high = []
            in2_high = []
  
            
            # -----------
            # gao
            d = 0
            start_dates = []
            date = buydata.index[0].date()
            while date < today.date():
                date = get_trade_days(start_date=date)[0]
                start_dates.append(date)
                date += dateutil.relativedelta.relativedelta(months=pmonth[d])
            start_dates.append(today.date())
        
            w = {}
            cost = 0
            asset = 0
            money = 0
            rate_cost = 0
            sold_money = 0
            profit = pd.DataFrame()
            value_df=pd.DataFrame()
            i = 1
            end_date = get_trade_days(end_date=start_dates[1] + timedelta(-1) , count=1)[0]
            data = pd.DataFrame()
            # 交易
            #limit
            for date in dates:
                flag = True
                if date in selldata.index:
                    ori_asset = asset
                    minus = selldata.loc[date, '赎回金额']
                    m = 0
                    if type(minus) == np.float64:
                        # asset -= float(minus)
                        # money -= float(minus)
                        m += float(minus)
                    else:
                        for j in range(len(minus)):
                            # asset -= float(minus.iloc[j])
                            # money -= float(minus.iloc[j])
                            m += float(minus.iloc[j])
                    rate = 0.005
                    sell_w = {}
                    for code in w.keys():
                        sell_w[code] = w[code] * min(m/ori_asset, 1)
                    w, money, tmp, sold_money = sell(sell_w, w, data, date, money, asset, rate)
                    sold_money = 0
                    #print('sell',date, w)
                    flag = False
                if date == end_date:
                    rate = 0.005
                    sell_w = w.copy()
                    w, money, tmp, sold_money = sell(sell_w, w, data, date, money, asset, rate)
                    #print('sell',date)
                    flag = False
                if date in buydata.index:
                    add = buydata.loc[date, '购买金额']
                    add_money = 0
                    if type(add) == str:
                        add_money = float(add)
                        # asset += float(add)
                        # money += float(add)
                    else:
                        for j in range(len(add)):
                            add_money += float(add.iloc[j])
                            # asset += float(add.iloc[j])
                            # money += float(add.iloc[j])
                    rate = 0.015
                    start_date = start_dates[0]
                    first_date = get_quarter_date(start_date)
                    end_date = get_trade_days(end_date=start_dates[i] + timedelta(-1) , count=1)[0]
                    quarter = (date.month - 1) // 3 + 1

                    test_year = date.year         #zym
                    test_month = date.month      #zym
                    find_year,find_period = findPeriod_HM(test_year,test_month)     #zym


                    buy_w_filename = os.path.join(os.path.dirname(__file__),'tmp','H'+ str(find_year)+'-'+str(find_period)+'.csv')
                    if os.path.exists(buy_w_filename):
                        buy_w = pd.read_csv(buy_w_filename, dtype=object)
                        buy_w.set_index('Unnamed: 0',inplace=True)
                    else:
                        buy_w = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.5, fund_pool_size=100, fund_pool_update=True,
                                         fund_nav_update=True, end_date=first_date, max_num=3, risk_aversion=3, fund_pool_funs=[fun[d]],
                                         fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(date.year)+'_'+str(quarter)+'.txt'))
                        buy_w = revise_w_gao(buy_w, 0.11)
                        buy_w.to_csv(buy_w_filename)
                    tdata = get_fund_data(start_dates[0], start_dates[-1], buy_w)
                    if data.empty:
                        data = tdata
                    else:
                        cols_to_use = set(data.columns) - set(tdata.columns)
                        data = pd.merge(data[cols_to_use], tdata, left_index=True, right_index=True, how='outer')
                    w, money, tmp, rate_cost, asset = buy(buy_w, w, data, date, money, asset, rate, rate_cost, add_money)
                    #print('buy',date)
                    flag = False
                if i+1 < len(start_dates) and date == start_dates[i]:
                    rate = 0.015
                    start_date = start_dates[i]
                    first_date = get_quarter_date(start_date)
                    end_date = get_trade_days(end_date=start_dates[i+1] + timedelta(-1) , count=1)[0]
                    i += 1
                    quarter = (date.month - 1) // 3 + 1

                    test_year = date.year         #zym
                    test_month = date.month      #zym
                    find_year,find_period = findPeriod_HM(test_year,test_month)     #zym


                    buy_w_filename = os.path.join(os.path.dirname(__file__), 'tmp','H'+str(find_year)+'-'+str(find_period)+'.csv')
                    if os.path.exists(buy_w_filename):
                        buy_w = pd.read_csv(buy_w_filename, dtype=object)
                        buy_w.set_index('Unnamed: 0',inplace=True)
                    else:
                        buy_w = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.5, fund_pool_size=100, fund_pool_update=True,
                                         fund_nav_update=True, end_date=first_date, max_num=3, risk_aversion=3, fund_pool_funs=[fun[d]],
                                         fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(date.year)+'_'+str(quarter)+'.txt'))
                        buy_w = revise_w_gao(buy_w, 0.11)
                        buy_w.to_csv(buy_w_filename)   #zym 
                    tdata = get_fund_data(start_dates[0], start_dates[-1], buy_w)
                    if data.empty:
                        data = tdata
                    else:
                        cols_to_use = set(data.columns) - set(tdata.columns)
                        data = pd.merge(data[cols_to_use], tdata, left_index=True, right_index=True, how='outer')
                    w, money, tmp, rate_cost, asset = buy(buy_w, w, data, date, money, asset, rate, rate_cost, sold_money)
                    #print('buy',date)
                    flag = False
                if flag:
                    tmp = nochange(w, data, date, money, asset)
                profit = pd.concat([profit, tmp])
                
                # 市值
                total_value=0 # 今日总市值
                for code,value in w.items():
                    if date in data.index:
                        close = data.loc[date, code]
                        total_value += close*value
                if total_value!=0:
                    temp = pd.DataFrame({'value': total_value+money}, index=pd.Index(data=[date,]))
                    value_df=pd.concat([value_df,temp])
            #print(asset) 
            value_list=list(value_df.value)
            result2,maxloss2 = bt.get_result(profit, 0.03,value_list)
            fig2 = os.path.join(os.path.dirname(__file__),'figure', filename[:-5]+ gd[d]+ '风险组合.png')
            p_money2 = result2['r']*asset
            md_money2 = result2['md']*asset
            #draw(profit, profit2[:-1], result, 'result\\'+ filename[:-5] + str(pmonth[d]) + 'limit_' + fun[d] + '.png', value_list[-1]-asset, maxloss)
            draw_profits(profit, profit2, result2, fig2, p_money2, maxloss2, start_dates[:-1])

            piename = os.path.join(os.path.dirname(__file__),'figure',filename[:-5] + gd[d] + '风险组合_pie.png')
            


            #zym 高风险 历史
            for t in range(5):

                test_it = history_high_quarter[t]
                test_year = test_it.year
                test_month = test_it.month
                find_year,find_period = findPeriod_HM(test_year,test_month)
                test_quarter = (test_it.month -1) //3 +1
                test_date = get_quarter_date(test_it)
                buy_w_test_filename =os.path.join(os.path.dirname(__file__), 'tmp','H'+ str(find_year)+'-'+str(find_period)+'.csv')
                #print(buy_w_test_filename)
                if os.path.exists(buy_w_test_filename):
                    #print("true")
                    buy_w_test = pd.read_csv(buy_w_test_filename, dtype=object)
                    buy_w_test.set_index('Unnamed: 0',inplace=True) 
                else:
                    buy_w_test = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.5, fund_pool_size=100, fund_pool_update=True,
                                                fund_nav_update=True, end_date=test_date, max_num=3, risk_aversion=3, fund_pool_funs=[fun[d]],
                                                fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(test_it.year)+'_'+str(test_quarter)+'.txt'))
                    buy_w_test = revise_w_gao(buy_w_test, 0.11)

                #print(buy_w_test)
                #print(buy_w_test.index[0])
                #print(buy_w_test.index[1])

                #zym
                namei = []
                length = len(buy_w_test['weights']) 
               
                for i in range(0,length):  #zym
                    nametmp = finance.run_query(query(finance.FUND_MAIN_INFO).filter(finance.FUND_MAIN_INFO.main_code==buy_w_test.index[i]))['name']
                    #print(nametmp)
                    nametmp = str(nametmp[0])
                    #print(nametmp)
                    namei.append(nametmp)
                    #stri=w.index[i]+name[0]+'——'+str(round(float(w.iloc[i][0])*100))+'万'

                buy_w_test = round_2(buy_w_test)    #
                labels_high = list(buy_w_test.index)
                #print(labels_high)
                names_high = namei
                #print(names_high)
                sizes_high = list(buy_w_test.weights)
                pt_high = [find_year, find_period, labels_high, names_high, sizes_high] 
                history_high.append(pt_high)






            t_quarter = (today.month - 1) // 3 + 1
            t_date = get_quarter_date(today)

            test_year = today.year         #zym
            test_month = today.month      #zym
            find_year,find_period = findPeriod_HM(test_year,test_month)     #zym

            buy_w_filename = os.path.join(os.path.dirname(__file__), 'tmp','H'+ str(find_year)+'-'+str(find_period)+'.csv')
            if os.path.exists(buy_w_filename):
                buy_w = pd.read_csv(buy_w_filename, dtype=object)
                buy_w.set_index('Unnamed: 0',inplace=True)
            else:
                buy_w = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.5, fund_pool_size=100, fund_pool_update=True,
                                         fund_nav_update=True, end_date=t_date, max_num=3, risk_aversion=3, fund_pool_funs=[fun[d]],
                                         fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(today.year)+'_'+str(t_quarter)+'.txt'))
                buy_w = revise_w_gao(buy_w, 0.11)
                buy_w.to_csv(buy_w_filename)


            buy_w = round_2(buy_w)
            
            draw_w(buy_w, piename)
            wd.write_docx(filename[:-5], sd,gd[d],str(pmonth[d])+'个月',figname2, p_per2, profit_f, fig2,result2['r'], p_money2,result2['md'],piename,buy_w)




            #zym

            r2_re = result2['r']
            sharpe2_re = result2['sharpe']
            md2_re = result2['md']
            rmd2_re = result2['r/md']
            prof2_re = str(round(p_money2/10000,2))
            loss2_re = str(round(maxloss2/10000,2))

            sy2_re = str(round(result2['r']*100,2))
            sy20_re = str(round(p_money2/10000))
            sycompare2_re = wd.change(profit_f, p_money2)

            hc20_re = str(round(result2['md']*100,2))


            
            
            #zym

            #year_c = str(today.year)
           
            #history_high.append(in3_high)


            chartadd2_high.append(r2_re)
            chartadd2_high.append(sharpe2_re)
            chartadd2_high.append(md2_re)
            chartadd2_high.append(rmd2_re)
            chartadd2_high.append(prof2_re)
            chartadd2_high.append(loss2_re)

            in2_high.append(sy2_re)
            in2_high.append(sy20_re)
            in2_high.append(sycompare2_re)
            in2_high.append(hc20_re)
  
            profit_high = profit











            #zym
            chartadd2_mid = []
            in2_mid = []



            # ----------------------
            # zhong
            start_dates = []
            d = 1
            date = buydata.index[0].date()
            while date < today.date():
                date = get_trade_days(start_date=date)[0]
                start_dates.append(date)
                date += dateutil.relativedelta.relativedelta(months=pmonth[d])
            start_dates.append(today.date())
        
            w = {}
            cost = 0
            asset = 0
            money = 0
            rate_cost = 0
            sold_money = 0
            profit = pd.DataFrame()
            value_df=pd.DataFrame()
            i = 1
            end_date = get_trade_days(end_date=start_dates[1] + timedelta(-1) , count=1)[0]
            data = pd.DataFrame()
            # 交易
            #limit
            for date in dates:
                flag = True
                if date in selldata.index:
                    ori_asset = asset
                    minus = selldata.loc[date, '赎回金额']
                    m = 0
                    if type(minus) == np.float64:
                        # asset -= float(minus)
                        # money -= float(minus)
                        m += float(minus)
                    else:
                        for j in range(len(minus)):
                            # asset -= float(minus.iloc[j])
                            # money -= float(minus.iloc[j])
                            m += float(minus.iloc[j])
                    rate = 0.005
                    sell_w = {}
                    for code in w.keys():
                        sell_w[code] = w[code] * min(m/ori_asset, 1)
                    w, money, tmp, sold_money = sell(sell_w, w, data, date, money, asset, rate)
                    sold_money = 0
                    #print('sell',date, w)
                    flag = False
                if date == end_date:
                    rate = 0.005
                    sell_w = w.copy()
                    w, money, tmp, sold_money = sell(sell_w, w, data, date, money, asset, rate)
                    #print('sell',date)
                    flag = False
                if date in buydata.index:
                    add = buydata.loc[date, '购买金额']
                    add_money = 0
                    if type(add) == str:
                        add_money = float(add)
                        # asset += float(add)
                        # money += float(add)
                    else:
                        for j in range(len(add)):
                            add_money += float(add.iloc[j])
                            # asset += float(add.iloc[j])
                            # money += float(add.iloc[j])
                    rate = 0.015
                    start_date = start_dates[0]
                    first_date = get_quarter_date(start_date)
                    end_date = get_trade_days(end_date=start_dates[i] + timedelta(-1) , count=1)[0]
                    quarter = (date.month - 1) // 3 + 1

                    #zym
                    test_year = date.year         #zym
                    test_month = date.month      #zym
                    find_year,find_period = findPeriod_HM(test_year,test_month)     #zym


                    buy_w_filename = os.path.join(os.path.dirname(__file__),'tmp','M'+ str(find_year)+'-'+str(find_period)+ '.csv')
                    if os.path.exists(buy_w_filename):
                        buy_w = pd.read_csv(buy_w_filename, dtype=object)
                        buy_w.set_index('Unnamed: 0',inplace=True)
                    else:
                        buy_w = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.7, fund_pool_size=100, fund_pool_update=True,
                                         fund_nav_update=True, end_date=first_date, max_num=2, risk_aversion=3, fund_pool_funs=[fun[d]],
                                         fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(date.year)+'_'+str(quarter)+'.txt'))
                        low_limit = random.randint(int(25),int(35)) / 100
                        buy_w = revise_w(buy_w, os.path.join(os.path.dirname(__file__),'funds', str(today.year)+'_'+str(quarter)+'_low.txt'), low_limit)
                        buy_w.to_csv(buy_w_filename)
                    tdata = get_fund_data(start_dates[0], start_dates[-1], buy_w)
                    if data.empty:
                        data = tdata
                    else:
                        cols_to_use = set(data.columns) - set(tdata.columns)
                        data = pd.merge(data[cols_to_use], tdata, left_index=True, right_index=True, how='outer')
                    w, money, tmp, rate_cost, asset = buy(buy_w, w, data, date, money, asset, rate, rate_cost, add_money)
                    #print('buy',date)
                    flag = False
                if i+1 < len(start_dates) and date == start_dates[i]:
                    rate = 0.015
                    start_date = start_dates[i]
                    first_date = get_quarter_date(start_date)
                    end_date = get_trade_days(end_date=start_dates[i+1] + timedelta(-1) , count=1)[0]
                    i += 1
                    quarter = (date.month - 1) // 3 + 1


                    #zym
                    test_year = date.year         #zym
                    test_month = date.month      #zym
                    find_year,find_period = findPeriod_HM(test_year,test_month)     #zym



                    buy_w_filename = os.path.join(os.path.dirname(__file__), 'tmp','M'+ str(find_year)+'-'+str(find_period)+ '.csv')
                    if os.path.exists(buy_w_filename):
                        buy_w = pd.read_csv(buy_w_filename, dtype=object)
                        buy_w.set_index('Unnamed: 0',inplace=True)
                    else:
                        buy_w = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.7, fund_pool_size=100, fund_pool_update=True,
                                         fund_nav_update=True, end_date=first_date, max_num=2, risk_aversion=3, fund_pool_funs=[fun[d]],
                                         fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(date.year)+'_'+str(quarter)+'.txt'))
                        low_limit = random.randint(int(25),int(35)) / 100
                        buy_w = revise_w(buy_w,os.path.join(os.path.dirname(__file__), 'funds',str(today.year)+'_'+str(quarter)+'_low.txt'), low_limit)
                        buy_w.to_csv(buy_w_filename)
                    tdata = get_fund_data(start_dates[0], start_dates[-1], buy_w)
                    if data.empty:
                        data = tdata
                    else:
                        cols_to_use = set(data.columns) - set(tdata.columns)
                        data = pd.merge(data[cols_to_use], tdata, left_index=True, right_index=True, how='outer')
                    w, money, tmp, rate_cost, asset = buy(buy_w, w, data, date, money, asset, rate, rate_cost, sold_money)
                    #print('buy',date)
                    flag = False
                if flag:
                    tmp = nochange(w, data, date, money, asset)
                profit = pd.concat([profit, tmp])
                
                # 市值
                total_value=0 # 今日总市值
                for code,value in w.items():
                    if date in data.index:
                        close = data.loc[date, code]
                        total_value += close*value
                if total_value!=0:
                    temp = pd.DataFrame({'value': total_value+money}, index=pd.Index(data=[date,]))
                    value_df=pd.concat([value_df,temp])
            #print(asset) 
            value_list=list(value_df.value)
            result2,maxloss2 = bt.get_result(profit, 0.03,value_list)
            fig2 = os.path.join(os.path.dirname(__file__),'figure', filename[:-5] + gd[d] + '风险组合' + '.png')
            p_money2 = result2['r']*asset
            md_money2 = result2['md']*asset
            #draw(profit, profit2[:-1], result, 'result\\'+ filename[:-5] + str(pmonth[d]) + 'limit_' + fun[d] + '.png', value_list[-1]-asset, maxloss)
            draw_profits(profit, profit2, result2, fig2, p_money2, maxloss2, start_dates[:-1])
            


            piename = os.path.join(os.path.dirname(__file__),'figure',filename[:-5] + gd[d] + '风险组合_pie.png')
            


            #zym 中风险 历史


            for t in range(5):

                test_it = history_mid_quarter[t]
                test_year = test_it.year
                test_month = test_it.month
                find_year,find_period = findPeriod_HM(test_year,test_month)

                test_quarter = (test_it.month -1) //3 +1
                test_date = get_quarter_date(test_it)
                buy_w_test_filename =os.path.join(os.path.dirname(__file__), 'tmp','M'+ str(find_year)+'-'+str(find_period)+ '.csv')
                if os.path.exists(buy_w_test_filename):
                    buy_w_test = pd.read_csv(buy_w_test_filename, dtype=object)
                    buy_w_test.set_index('Unnamed: 0',inplace=True)
                else:
                    buy_w_test = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.7, fund_pool_size=100, fund_pool_update=True,
                                                fund_nav_update=True, end_date=t_date, max_num=2, risk_aversion=3, fund_pool_funs=[fun[d]],
                                                fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(test_year)+'_'+str(test_quarter)+'.txt'))
                    low_limit = random.randint(int(25),int(35)) / 100
                    buy_w_test = revise_w(buy_w_test,os.path.join(os.path.dirname(__file__), 'funds',str(test_year)+'_'+str(test_quarter)+'_low.txt'), low_limit)

                #print(buy_w_test)

                #zym
                namei = []
                length = len(buy_w_test['weights']) 
                for i in range(0,length):
                    nametmp = finance.run_query(query(finance.FUND_MAIN_INFO).filter(finance.FUND_MAIN_INFO.main_code==buy_w_test.index[i]))['name']
                    nametmp = str(nametmp[0])
                    namei.append(nametmp)
                    #stri=w.index[i]+name[0]+'——'+str(round(float(w.iloc[i][0])*100))+'万'


                buy_w_test = round_2(buy_w_test) 
                labels_mid = list(buy_w_test.index)
                names_mid = namei
                sizes_mid = list(buy_w_test.weights)
                pt_mid = [find_year, find_period, labels_mid, names_mid, sizes_mid] 
                history_mid.append(pt_mid)




            t_quarter = (today.month - 1) // 3 + 1
            t_date = get_quarter_date(today)

            test_year = today.year
            test_month = today.month
            find_year,find_period = findPeriod_HM(test_year,test_month)


            buy_w_filename = os.path.join(os.path.dirname(__file__), 'tmp','M'+ str(find_year)+'-'+str(find_period)+ '.csv')
            if os.path.exists(buy_w_filename):
                buy_w = pd.read_csv(buy_w_filename, dtype=object)
                buy_w.set_index('Unnamed: 0',inplace=True)
            else:
                buy_w = pc.get_portfolio(money_scale=1e+7, up_limit_percent=0.7, fund_pool_size=100, fund_pool_update=True,
                                         fund_nav_update=True, end_date=t_date, max_num=2, risk_aversion=3, fund_pool_funs=[fun[d]],
                                         fund_filename=os.path.join(os.path.dirname(__file__),'funds',str(today.year)+'_'+str(t_quarter)+'.txt'))
                low_limit = random.randint(int(25),int(35)) / 100
                buy_w = revise_w(buy_w, os.path.join(os.path.dirname(__file__),'funds',str(today.year)+'_'+str(quarter)+'_low.txt'), low_limit)
                buy_w.to_csv(buy_w_filename)


            buy_w = round_2(buy_w)

            draw_w(buy_w, piename)
            wd.write_docx(filename[:-5], sd,gd[d],str(pmonth[d])+'个月',figname2, p_per2, profit_f, fig2,result2['r'], p_money2,result2['md'],piename,buy_w)
            


            #zym

            r2_re = result2['r']
            sharpe2_re = result2['sharpe']
            md2_re = result2['md']
            rmd2_re = result2['r/md']
            prof2_re = str(round(p_money2/10000,2))
            loss2_re = str(round(maxloss2/10000,2))

            sy2_re = str(round(result2['r']*100,2))
            sy20_re = str(round(p_money2/10000))
            sycompare2_re = wd.change(profit_f, p_money2)

            hc20_re = str(round(result2['md']*100,2))



            #zym

            
            chartadd2_mid.append(r2_re)
            chartadd2_mid.append(sharpe2_re)
            chartadd2_mid.append(md2_re)
            chartadd2_mid.append(rmd2_re)
            chartadd2_mid.append(prof2_re)
            chartadd2_mid.append(loss2_re)

            in2_mid.append(sy2_re)
            in2_mid.append(sy20_re) 
            in2_mid.append(sycompare2_re)

            in2_mid.append(hc20_re)

            profit_mid = profit








    
    #zym 横轴

    xline = []

    for i in range(0,len(profit2)-1):
        datetmp = str(profit2.index[i])
        datetmp = datetmp.replace(" 00:00:00","")
        xline.append(datetmp)
    
    #zym 投资周期
     
    duration = [11,11,7] 

    #zym 图1 客户理财的复现

    chart1 = [['xline','profit2']]

    for i in range(0,len(profit2)-1):
        stmp = [xline[i],profit2.p[i]]
        chart1.append(stmp)

    sy1_re = str(round(p_per2*100,2))   #期间收益 %
    sy10_re = str(round(profit_f/10000))      #期间收益 万元
    
    in1 = [sy1_re, sy10_re]

    #zym 图2 推荐组合和客户理财对比

    #print(chartadd2_high)
    #print(chartadd2_mid)
    #print(chartadd2_low)
    #print(in2_high)
    #print(in2_mid)
    #print(in2_low)

    chart2_high = [['xline','profit_high','profit2']]    #高风险
    chart2_mid = [['xline','profit_mid','profit2']]      #中风险
    chart2_low = [['xline','profit_low','profit2']]      #低风险

    for i in range(0,len(profit2)-1):
        stmph = [xline[i],profit_high.p[i],profit2.p[i]]
        chart2_high.append(stmph)
        stmpm = [xline[i],profit_mid.p[i],profit2.p[i]]
        chart2_mid.append(stmpm)
        stmpl = [xline[i],profit_low.p[i],profit2.p[i]]
        chart2_low.append(stmpl)


    return date_re, chart1, in1, duration, chart2_high, chart2_mid, chart2_low, chartadd2_high, chartadd2_mid, chartadd2_low, in2_high, in2_mid, in2_low, history_high,history_mid,history_low
