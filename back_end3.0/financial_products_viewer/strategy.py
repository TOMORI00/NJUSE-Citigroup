# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 18:09:14 2019

@author: Cheng
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:43:22 2019

@author: Cheng
"""

from jqdatasdk import finance
from jqdatasdk import *
from sqlalchemy import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pylab import date2num
from datetime import datetime, timedelta
from . import backtest as bt
import math


#plt.rcParams['savefig.dpi'] = 200 #图片像素
#plt.rcParams['figure.dpi'] = 200 #分辨率


def get_last_date(date):
    tmp_date = date - timedelta(1)#zym
    last_date = get_trade_days(end_date=tmp_date.__str__(), count=1)[0]
    return last_date


def read_file(filename):
    time_dict = {}
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            #print(line)
            lst = line.strip().split(',')
            if len(lst) == 1:
                continue
            if lst[1] == '':
                continue
            #time_dict[datetime.strptime(lst[0], "%Y-%m-%d %H:%M:%S")] = float(lst[1])
            time_dict[datetime.strptime(lst[0], "%Y-%m-%d")] = float(lst[1])
    return time_dict


def get_profits(data, r, filename):
    time_dict = read_file(filename)
    profit = pd.DataFrame()
    cost = 0
    own = 0
    own_position = 0
    money = 1e7
    record = []
    for index, row in data.iterrows():
        if time_dict.get(index) != None:
            # 当前时间持仓
            position = time_dict.get(index)
            # 交易方向
            direction = position - own_position
            # 买入
            if direction > 0:
                # 对每次买入份额压栈
                record.append([index, direction])
                cost, tmp, own, money = bt.buy(own, direction, index, cost, data, money)
                profit = pd.concat([profit, tmp])
            # 卖出
            elif direction < 0:
                unsell = - direction
                while abs(unsell) > 1e-6:
                    first_time, first_direction = record.pop(0)
                    tmp_direction = first_direction - unsell
                    day = (index - first_time).days
                    rate = r
                    # rate = 0.005
                    # if day <= 6:
                    #     rate = 0.015
                    # elif day <= 364:
                    #     rate = 0.005
                    # elif day <= 729:
                    #     rate = 0.0025
                    # 卖出的份额大于买入的份额
                    if tmp_direction < -1e-6:
                        tmp, own, money = bt.sell(own, first_direction, index, cost, data, money, rate)
                        unsell -= first_direction
                    # 卖出的份额小于等于买入的份额
                    else:
                        tmp, own, money = bt.sell(own, unsell, index, cost, data, money, rate)
                        unsell = 0
                        # 卖出的份额小于买入的份额，重新压栈
                        if tmp_direction > 1e-6:
                            record.insert(0, [first_time, tmp_direction])
                profit = pd.concat([profit, tmp])
            else:
                tmp = bt.nochange(own, index, cost, data, money)
                profit = pd.concat([profit, tmp])
            own_position = position
        else:
            tmp = bt.nochange(own, index, cost, data, money)
            profit = pd.concat([profit, tmp])
    return profit


