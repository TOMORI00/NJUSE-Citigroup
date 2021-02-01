#from EmQuantAPI import *
from jqdatasdk import finance
from jqdatasdk import *
from sqlalchemy import *
from . import data_preparation as dp
from . import mean_variance as mv
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
import os
from . import backtest as bt
from datetime import timedelta


def start():
    auth('13739188902', 'ZNnb20160801')
    timing = pd.read_table("timing_zn0.txt", dtype=str, header=None)
    _end_date = timing.iloc[:, 0].tolist()
    for _ in _end_date:
        end_date = datetime.strptime(_, "%Y%m%d").date()
        w = get_portfolio(money_scale=1e+7, up_limit_percent=0.35, fund_pool_size=100, fund_pool_update=True,
                          fund_nav_update=True, end_date=end_date, max_num=3, risk_aversion=3)
        print(w)
        '''
        interval = [14, 60, 180]
        for ind in interval:
            rfr = 0.03 * ind / 360
            start_date = end_date - timedelta(ind)
            backtest1 = bt.get_backtest(w[0], start_date=start_date, end_date=end_date, riskfree_rate=rfr)
            print('回测期：', ind, '天')
            print(backtest1)
        '''


def get_portfolio(money_scale=1e+8, up_limit_percent=0.35, fund_pool_size=400, risk_free_rate=0.03, fund_pool_funs=['return'],
                  fund_pool_update=False, fund_nav_update=False, end_date=date.today(), max_num=4, risk_aversion=3.,
                  fund_filename='2015_1.txt'):
    """

    :param risk_aversion:
    :param max_num:
    :param risk_free_rate:
    :param end_date:
    :param money_scale:
    :param up_limit_percent:
    :param fund_pool_size:
    :param fund_pool_update:
    :param fund_nav_update:
    :return:
    """

    print("\n\n\n执行投资指令……")
    w = []
    #fund_pool_funs = ['return', 'drawdown1', 'drawdown2']
    #fund_pool_funs = ['return', 'drawdown1']
    #fund_pool_funs = ['return']
    for fund_pool_fun in fund_pool_funs:
        print("正在计算基金池:", fund_pool_fun)
        # 获取各个基金的最新收益率时间序列数据
        funds = dp.get_fund_pool(fund_pool_update=fund_pool_update, return_detail=True, update_date=end_date,
                                 fund_pool_fun=fund_pool_fun, fund_filename=fund_filename)
        begin_date = end_date - timedelta(60)
        data = dp.get_nav_rates(fund_nav_update=fund_nav_update, fund_pool_update=False, begin_date=begin_date.__str__(),
                                end_date=end_date, fund_pool_fun=fund_pool_fun)  # 读取基金收益率数据
        print("基金池中基金个数: ", len(funds.index))
        # 最多取前200只基金
        return_table = data.iloc[:, 0:fund_pool_size]
        # 临时黑名单
        #blacklist = ["001357", "001103", "260108", "001875"]
        # blacklist = ["006160",  "005711", "006002", "006003", "005774", "001117"]
        '''
        # 去掉暂停大额申购的基金
        to_be_del = list(set(funds.index) - set(funds[funds.PURCHSTATUS == "开放申购"].index))
        blacklist.extend(to_be_del)

        # 去掉含有“定开”字眼的基金
        to_be_del = list(funds[funds.NAME.str.contains("定开")].index)
        blacklist.extend(to_be_del)

        # 去掉含有“定期开放”字眼的基金
        to_be_del = list(funds[funds.NAME.str.contains("定期开放")].index)
        blacklist.extend(to_be_del)

        blacklist = list(set(blacklist).intersection(set(return_table.columns)))
        
        # 基金池净值序列
        fund_nav = return_table.drop(columns=blacklist)
        print("最终基金池中基金个数: ", len(fund_nav.columns))
        '''
        
        fund_nav = return_table
        print("最终基金池中基金个数: ", len(fund_nav.columns))
        
        # 投资总规模
        portfolio_scale = money_scale
        # 单个基金最小投资额
        # fund_min_invest_mount = 0.001e+8
        # 最大基金投资个数
        # max_num = portfolio_scale / fund_min_invest_mount

        # 防止巨额赎回，每个基金最多只能购买其5%资金规模
        #up_limit = funds.FUNDSCALE[list(fund_nav.columns)] * 0.1 / portfolio_scale
        # 加上单支基金最大35%仓位的限制
        #up_limit[up_limit > up_limit_percent] = up_limit_percent
        up_limit = [up_limit_percent] * len(list(fund_nav.columns))
        print("Start to build the portfolio...")
        # 构建投资组合
        # print(fund_nav)
        # pd.DataFrame.to_csv(fund_nav,"xx.csv", index=True)
        # 按照夏普率构建
        w_sharpe = mv.get_maximum_sharpe_portfolio(return_table=fund_nav, up_limit=up_limit,
                                                                   riskfree_rate=risk_free_rate,
                                                                   allow_short=False, show_details=False,
                                                                   max_num=max_num)
        
        #save_data(w_sharpe, portfolio_scale=portfolio_scale, fund_nav=fund_nav, details=details_sharpe,
        #          fun='sharpe', fund_pool_fun=fund_pool_fun, end_date=end_date)
        ww = pd.DataFrame.from_dict(w_sharpe, orient='index')
        results = ww[ww.iloc[:, 0] > 0.001]
        results.columns = ["weights"]
        #values = get_fund_data(begin_date, end_date, results)
        #print(values)
        #details = get_result(values, 0.03)
        #mv.draw_picture(results, end_date=end_date.__str__())
        #w.append(results)
        '''
        # 按照效用函数构建，设置风险厌恶系数
        w_utility, details_utility = mv.get_maximum_utility_portfolio(return_table=fund_nav,
                                                                      risk_aversion=risk_aversion,
                                                                      allow_short=False, show_details=False,
                                                                      up_limit=up_limit, max_num=max_num)
        save_data(w_utility, portfolio_scale=portfolio_scale, fund_nav=fund_nav, details=details_utility,
                  fun='utility', fund_pool_fun=fund_pool_fun, end_date=end_date)
        ww = pd.DataFrame.from_dict(w_utility, orient='index')
        results = ww[ww.iloc[:, 0] > 0.001]
        results.columns = ["weights"]
        w.append(results)
        '''
    return results


def get_last_date(date):
    tmp_date = date - timedelta(1)
    last_date = get_trade_days(end_date=tmp_date.__str__(), count=1)[0]
    return last_date


def get_result(value, riskfree_rate):
    # fund_nav_rates = value.pct_change()
    fund_nav_rates = value - value.shift(1)
    r = round(value.iloc[-1, 0] / value.iloc[0, 0] - 1, 4)
    v = round(np.std(fund_nav_rates.p), 4)
    s = round((r - riskfree_rate) / v, 4)
    md = round(get_maxdrawdown(list(value.p)), 4)
    result = {'收益率': r, '波动率': v, '夏普比': s, '最大回撤率': md}
    return result


def get_maxdrawdown(return_list):
    # 计算最大回撤率
    i = np.argmax(
        (np.maximum.accumulate(return_list) - return_list) / (np.maximum.accumulate(return_list) + 1e-3))  # 结束位置
    if i == 0:
        return 0
    j = np.argmax(return_list[:i])  # 开始位置
    return (return_list[j] - return_list[i]) / (return_list[j])


def get_fund_data(start_date, end_date, w):
    ld = get_last_date(start_date)
    codes = list(w.index)
    data = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(codes),
                                                                  finance.FUND_NET_VALUE.day >= ld,
                                                                  finance.FUND_NET_VALUE.day <= end_date))

    value = data.reset_index().pivot("day", "code", "sum_value")
    # print(value)
    nanlist = value.columns[value.isna().any()].tolist()
    w = w.drop(nanlist)
    w = w * (1 / np.sum(w))
    # print(w)
    codes = list(w.index)
    fund_value = np.zeros(len(value))
    # value['fund_value'] = [0] * len(value)
    # print(value)
    for code in codes:
        # value[code] = value[code] / value[code][0]
        fund_value += w.loc[code, 'weights'] * value[code]
    fund_value = pd.DataFrame(fund_value)
    fund_value.columns = ['p']
    return fund_value


def save_data(w, portfolio_scale=1e+8, fund_nav=None, details='', fun='', fund_pool_fun='', end_date=date.today()):
    # details加上基金规模信息
    details = details + "\n" + "                Portfolio scale: " + int(portfolio_scale).__str__()

    ww = pd.DataFrame.from_dict(w, orient='index')
    results = ww[ww.iloc[:, 0] > 0.001]
    results.columns = ["weights"]
    results.index.name = "codes"
    results = results.sort_values("weights", ascending=False)
    #mv.draw_picture(results, details, int(portfolio_scale), end_date, fun=fun, fund_pool_fun=fund_pool_fun)

    ind = results.index.tolist()

    return_table = fund_nav.loc[:, ind]
    output = mv.describe(return_table, is_print=False)
    keys = output['coefficient_matrix'].keys()
    coefficient = pd.DataFrame(output['coefficient_matrix'].values)
    coefficient.columns = keys
    coefficient.index = keys
                                   #zym
    coefficient.to_csv(os.path.dirname(__file__) + "\\vill\\results\\coefficient_" + fund_pool_fun + "_" + fun + ".csv", index=True,
                       encoding="utf_8_sig")
    coefficient.to_csv(
        os.path.dirname(__file__) + "\\vill\\snapshots\\coefficient_" + fund_pool_fun + "_" + fun + "_" + int(
            portfolio_scale).__str__() + " " + end_date.__str__() + ".csv",
        index=True, encoding="utf_8_sig")

    logfile = open('log.txt', 'a')
    print(_, file=logfile)
    print(results, file=logfile)
    print("\n\n", file=logfile)
    print(results, file=logfile)
    print("\n\n", file=logfile)
    logfile.close()
    return results


if __name__ == '__main__':
    start()

