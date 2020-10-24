from jqdatasdk import finance
from jqdatasdk import *
from sqlalchemy import *
import pandas as pd
import numpy as np
from . import data_preparation as dp
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import math
from . import strategy as st


def buy(own, w, sd, cost, data, money = 1e7):
    close = data.loc[sd, 'close']
    old_hold = own * close
    buy_w = min(money, w * (money + old_hold)) / close
    new_own = own + buy_w
    new_cost = buy_w * close
    hold = new_own * close
    new_money = money - new_cost
    #new_own = w + own
    #new_cost = (w * close + own * cost) / new_own
    #tmp = pd.DataFrame({'p': 1 + (tmp_profit + new_own * (close - new_cost)) / new_cost}, index=pd.Index(data=[sd,]))
    print(sd, 'buy', own, new_own, new_money, hold)
    tmp = pd.DataFrame({'p': (hold + new_money) / 1e7}, index=pd.Index(data=[sd,]))
    return new_cost, tmp, new_own, new_money


def sell(own, w, sd, cost, data, money = 1e7, rate = 0):
    close = data.loc[sd, 'close']
    sell_w = min(own, w * (own * close + money) / close)
    new_own = own - sell_w
    hold = new_own * close
    new_money = money + sell_w * close * (1 - rate)
    print(sd, 'sell', own, new_own, new_money, hold, rate)
    tmp = pd.DataFrame({'p': (hold + new_money) / 1e7}, index=pd.Index(data=[sd,]))
    return tmp, new_own, new_money


def nochange(own, sd, cost, data, money = 1e7):
    close = data.loc[sd, 'close']
    hold = own * close
    tmp = pd.DataFrame({'p': (hold + money) / 1e7}, index=pd.Index(data=[sd,]))
    return tmp


def get_maxdrawdown(return_list):
    # 计算最大回撤率
    i = np.argmax((np.maximum.accumulate(return_list) - return_list) / (np.maximum.accumulate(return_list) + 1e-3))  # 结束位置
    if i == 0:
        return 0
    j = np.argmax(return_list[:i])  # 开始位置
    return (return_list[j] - return_list[i]) / (return_list[j])

def get_maxdrawdown_value(value_list):
    # 按照市值计算最大回撤率和最大回撤金额
    md_value=0 # 最大回撤率
    maxloss=0 # 最大回撤金额
    for index1 in range(0,len(value_list)):
        for index2 in range(index1,len(value_list)):
            if (value_list[index1]-value_list[index2])/value_list[index1]>md_value:
                md_value=(value_list[index1]-value_list[index2])/value_list[index1]
                maxloss=value_list[index1]-value_list[index2]
    return md_value, maxloss
    

def get_result(value, riskfree_rate,value_list=[]):         #zym 图二信息
    #rates = value.pct_change()
    tmpv = value.dropna()
    rates = tmpv - tmpv.shift(1)
    r = round(tmpv.iloc[-1, 0] / tmpv.iloc[0, 0] - 1, 4)
    #v = round(np.std(rates.close), 4)
    #s = round((r - riskfree_rate) / v, 4)
    s = math.sqrt(252) * (rates.p - riskfree_rate/252).mean()/(rates.p - riskfree_rate/252).std()
    s = round(s, 4)
    if value_list: # 用市值算
        md, maxloss=get_maxdrawdown_value(value_list)
        md = round(md,4)
    else: # 用收益率算
        md = round(get_maxdrawdown(list(tmpv.p)), 4)
        maxloss=0
    rmd = round(r/md, 4)
    result = {'r': r, 'sharpe': s, 'md': md, 'r/md': rmd}
    return result, maxloss


def get_maxdown(data):
    last_p = 0
    max_num = 0
    num = 0
    max_r = 0
    cont_r = 0
    max_cont_r = 0
    down = False
    hold = 0
    time_dict = st.read_file('buy_sell_dates.csv')
    for index in data.index:
        if time_dict.get(index) != None:
            position = time_dict.get(index)
            # 清仓 计算收益
            if position == 0 and hold != 0:
                p = data.loc[index, 'p']
                r = (p - last_p)/last_p
                if r < 0:
                    if down:
                        num += 1
                        cont_r += r
                    else:
                        num = 1
                        cont_r = r
                    down = True
                else:
                    down = False
                if r < max_r:
                    max_r = r
                if num > max_num:
                    max_num = num
                if cont_r < max_cont_r:
                    max_cont_r = cont_r
                hold = 0
            else:
                if hold == 0:
                    last_p = data.loc[index, 'p']
                hold = position
    return max_num, max_r, max_cont_r

