#from EmQuantAPI import *
from jqdatasdk import finance
from jqdatasdk import *
from sqlalchemy import *
from datetime import date
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import os

# 基金池
fund_pool = None
# 基金净值信息
fund_nav_rates = None


# ----------------------------------------------------------------------------------------#
#                   函数功能：获取基金池
#       默认参数：
#           1、不更新基金池，一般一周更新一次
#           2、如若更新，更新日期为运行当天
#           3、只返回基金代码，不返回其他详细信息
# ----------------------------------------------------------------------------------------#

def get_fund_pool(fund_pool_update=False, update_date=date.today(), return_detail=False, 
                  fund_pool_fun='return', fund_filename='2015_1.txt'):
    """
    1、基金代码处理，默认获取当前所有基金；或者直接给定初始基金池
    2、过滤掉不公布净值的基金和规模过小的基金
    3、对池中基金进行排序、过滤和评分

    :param start_dates:
    :param fund_pool_fun: "return": 根据区间内收益率取基金池
                "drawdown1": 根据区间内最大涨幅/最大回撤取基金池
                "drawdown2": 根据区间内最大涨幅和最大回撤交集取基金池
    :param fund_pool_update: 是否进行基金池更新
    :param update_date: 更新日期
    :param return_detail: 是否返回基金池详细信息
    :return: 返回基金池列表，简单信息只含代码，详细信息包含多维信息

    """

    global fund_pool

    # 更新标志为假，无需更新，返回默认池data\snapshots\fundpool.csv
    if not fund_pool_update:
        print("--------------")
        print("不更新基金池")
        print("--------------")
        # 读取候选基金池                    #zym os.getcwd()
        res = pd.read_csv(os.path.join(os.path.dirname(__file__), "vill","snapshots","fundpool_" + fund_pool_fun + "_" + update_date.__str__() + ".csv"), index_col=0, header=None, dtype=object)
        fund_pool = list(res.index)
        if return_detail:
            return res
        else:
            return fund_pool

    with open(fund_filename, 'r') as f:
        codes = f.readlines()
        #codes = codes.strip().split('')
        codes = [code.strip() for code in codes]
    if codes == ['']:
        # 更新标志为真，更新基金池，保存到默认池以及快照池
        print("--------------")
        print("现在更新基金池")
        print("--------------")

        # -----------------------------------------#
        # 基金代码处理，若是给定基金池，则不需处理 #
        # -----------------------------------------#

        # 股票型基金代码
        #data = c.sector("507030", update_date.__str__())
        #stock = data.Data[::2]

        # 混合型基金代码
        #data = c.sector("507029", update_date.__str__())
        #hybrid = data.Data[::2]

        # 股票型基金
        s = finance.run_query(query(finance.FUND_MAIN_INFO).filter(finance.FUND_MAIN_INFO.underlying_asset_type_id == 402001).limit(5000))
        # 混合型基金
        h = finance.run_query(query(finance.FUND_MAIN_INFO).filter(finance.FUND_MAIN_INFO.underlying_asset_type_id == 402004).limit(5000))

        # 黑名单，由于各种原因被排除在外的基金，如申赎费率、停止申赎、限大额等
        #blacklist = "470021.OF,003362.OF,001309.OF,002166.OF,005434.OF,960000.OF,160421.OF"
        #blacklist = "470021,003362,001309,002166,005434,960000,160421"

        # 将字符串列表化
        #blacklist = blacklist.split(',')

        with open('blacklist.txt', 'r') as f:
            tmp = f.readline()
            blacklist = tmp.strip().split(' ')
        # 所有可选基金
        # fund_pool_code = stock.__add__(hybrid)
        data = pd.merge(s, h, how="outer")

        # 去除黑名单基金
        #fund_pool_code = list(set(fund_pool_code) - set(blacklist))
        data = data[~data.main_code.isin(blacklist)]

        # 测试时用，减少数据流量
        # fund_pool_code = fund_pool_code[0:400]

        fund_pool_code = list(data.main_code)
        print("候选基金个数：", fund_pool_code.__len__())

        # --------------------------------------------#
        # ---过滤掉不公布净值的基金和规模过小的基金---#
        # --------------------------------------------#

        # 读取基金池中各个基金的最新净值更新日期
        # data = c.css(fund_pool_code, "NAVLATESTDATE", "EndDate=" + update_date.__str__() + ",RowIndex=1,Ispandas=1")
        # print(data)
        # 去掉停更基金
        # tmp = data[data.iloc[:, 1] >= data.iloc[:, 1].max()]  #这个语句可能有问题  201938会大于2019319，更新的日期还有可能有“”值或者None
        # 1、去掉更新日期为“”的基金
        #dat = data[data.iloc[:, 1] != ""]
        # 2、对于更新日期为None的基金，一律设置为很早，剔除掉
        #dat.iloc[:, 1].fillna('2000/01/01', inplace=True)
        # 3、将字符串格式的日期转化为规范化的日期类型，这个是东方财富不专业的地方
        #dat.iloc[:, 1] = dat.iloc[:, 1].apply(lambda x: datetime.strptime(x, '%Y/%m/%d'))
        # 选择出最近两天有更新的基金列表
        #tmp = dat[dat.iloc[:, 1] >= dat.iloc[:, 1].max()-timedelta(2)]
        tmp = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(fund_pool_code), finance.FUND_NET_VALUE.day == update_date.__str__()))


        # 更新基金池
        # fund_pool_code = list(tmp.index)
        fund_pool_code = list(tmp.code)
        print("去掉停止更新基金后的候选基金个数： ", fund_pool_code.__len__())

        # 过滤掉规模小于一亿的基金，流动性会受到影响
        #data = c.css(fund_pool_code, "FUNDSCALE", "EndDate=" + update_date.__str__() + ",RowIndex=1,Ispandas=1")
        #tmp = data[data.iloc[:, 1] >= 1e8]
        data = finance.run_query(
            query(finance.FUND_FIN_INDICATOR).filter(finance.FUND_FIN_INDICATOR.code.in_(fund_pool_code)).order_by(
                finance.FUND_FIN_INDICATOR.id.desc()).group_by(finance.FUND_FIN_INDICATOR.code))
        tmp = data[data.total_tna >= 1e8]
        # 更新基金池
        fund_pool_code = list(tmp.code)
    else:
        #tmp = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(codes), finance.FUND_NET_VALUE.day == update_date.__str__()))
        # 更新基金池
        # fund_pool_code = list(tmp.index)
        #fund_pool_code = list(tmp.code)
        fund_pool_code = list(set(codes))
        print("去掉停止更新基金后的候选基金个数： ", fund_pool_code.__len__())

    #fund_pool_code = ['519712', '519772', '001938', '110011', '000527', '001714', '519069', '519736',
    #                  '710002', '040008', '163402', '270002', '000194', '000191', '217003', '002865',
    #                  '006077']
    print("去掉小规模基金后的候选基金个数： ", fund_pool_code.__len__())


    # ---------------------------------------- #
    # -----对池中基金进行排序、过滤和评分----- #
    # ---------------------------------------- #

    # 选取前top_n个基金入池，至少是前半区
    top_n = min(int(fund_pool_code.__len__()/2), 800)
    
    # 考察基金的时间区间：1,3,6,12,24个月
    #interval = [30, 90, 180, 365, 730]
    #interval = [30, 60, 90, 120, 180]
    interval = [14, 30, 60]
    previous_dates = get_previous_date(interval, update_date)
    # 存放每个时间区间的基金排序结果
    results = []
    # store the showing times and scores for each fund
    rank_times = pd.concat([pd.Series(fund_pool_code), pd.Series(np.zeros(len(fund_pool_code))),
                            pd.Series(np.zeros(len(fund_pool_code)))], axis=1)
    # 分别给三个序列命名
    rank_times.columns = ["codes", 'times', 'scores']
    # 设置索引，记住复制，否则不保存！！！
    rank = rank_times.set_index("codes")
    
    # 对每个时间区间的基金进行排序
    for previous_date in previous_dates:
        #previous_date = previous_date.__str__()
        #previous_date = update_date - timedelta(ind)
        #根据区间内收益率进行排序
        if fund_pool_fun == 'return':
            # 区间内净值表现
            #result_ori = c.css(fund_pool_code, "NAVADJRETURNP",
            #                   "StartDate=" + previous_date.__str__() + ", EndDate=" + update_date.__str__() + ",RowIndex=1,Ispandas=1")
            # 将其按照净值排序
            #result_sort = result_ori.sort_values("NAVADJRETURNP", ascending=False)
            # 选择前topN基金,只取收益率,注意必须去掉NaN值，因为不是所有被选出来的都有净值收益
            #temp = result_sort.iloc[0:top_n, 1].dropna()
            # 区间内净值表现
            previous_value = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(fund_pool_code), finance.FUND_NET_VALUE.day==previous_date.__str__()))
            previous_value = previous_value.set_index('code')
            now_value = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(fund_pool_code), finance.FUND_NET_VALUE.day==update_date.__str__()))
            now_value = now_value.set_index('code')
            previous_value.fillna(1, inplace=True)
            result_ori = now_value.sum_value / previous_value.sum_value
            result_ori.columns = ['scores']
            # 将其按照净值排序
            result_sort = result_ori.sort_values(ascending=False)
            # 选择前topN基金,只取收益率,注意必须去掉NaN值，因为不是所有被选出来的都有净值收益
            temp = result_sort.iloc[0:top_n].dropna()
            #print(result_ori, temp)
            # 该时间区间的基金代码列表
            result = list(temp.index)
            # 将收益率值变换成序号，即大值小序号
            temp = temp.rank(ascending=False)
            # 列表中的每个基金出现次数加1
            rank._set_value(result, "times", np.ones(result.__len__()) + rank.loc[result, :].times)
            # 列表中每个基金累计上新的得分
            #print(rank, temp)
            rank._set_value(result, "scores", temp + rank.loc[result, :].scores)

            results.append(result)
        elif fund_pool_fun == 'md':
            data = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(fund_pool_code),finance.FUND_NET_VALUE.day >= previous_date.__str__(), finance.FUND_NET_VALUE.day<=update_date.__str__()))
            # data = pd.DataFrame()
            # bd = previous_date
            # ed = bd
            # while ed <= update_date:
            #     ed = bd + timedelta(10)
            #     if ed >= update_date:
            #         ed = update_date + timedelta(1)
            #     tmp = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(fund_pool_code),
            #                                                                  finance.FUND_NET_VALUE.day >= bd,
            #                                                                  finance.FUND_NET_VALUE.day < ed))
            #     data = pd.concat([data, tmp])
            #     bd = ed
            fund_value = data.reset_index().pivot("day", "code", "sum_value")
            #fund_nav_rates = fund_value.pct_change()
            fund_value.fillna(1, inplace=True)
            result_ori = pd.DataFrame(columns=('scores',))
            #result_ori.index.name = "code"
            #fund_nav_rates.fillna(0, inplace=True)
            #fund_nav_rates = fund_nav_rates.drop(list(fund_nav_rates.index)[0])
            for code in list(fund_value.columns):
                md = get_maxdrawdown(fund_value[code])
                result_ori.loc[code] = md
            #print(result_ori)
            result_sort = result_ori.sort_values(by='scores', ascending=False)
            
            temp = result_sort.iloc[0:top_n].dropna()
            #print(result_ori, temp)
            # 该时间区间的基金代码列表
            result = list(temp.index)
            # 将收益率值变换成序号，即大值小序号
            temp = temp.rank(ascending=False)
            # 列表中的每个基金出现次数加1
            rank._set_value(result, "times", np.ones(result.__len__()) + rank.loc[result, :].times)
            # 列表中每个基金累计上新的得分
            #print(rank, temp)
            rank._set_value(result, "scores", temp.scores + rank.loc[result, :].scores)
            #print(rank)
            results.append(result)
        # 按收益回撤比排序
        elif fund_pool_fun == 'rmd':
            data = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(fund_pool_code),finance.FUND_NET_VALUE.day >= previous_date.__str__(), finance.FUND_NET_VALUE.day<=update_date.__str__()))
            # data = pd.DataFrame()
            # bd = previous_date
            # ed = bd
            # while ed <= update_date:
            #     ed = bd + timedelta(10)
            #     if ed >= update_date:
            #         ed = update_date + timedelta(1)
            #     tmp = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(fund_pool_code),
            #                                                                  finance.FUND_NET_VALUE.day >= bd,
            #                                                                  finance.FUND_NET_VALUE.day < ed))
            #     data = pd.concat([data, tmp])
            #     bd = ed
            fund_value = data.reset_index().pivot("day", "code", "sum_value")
            #fund_nav_rates = fund_value.pct_change()
            fund_value.fillna(1, inplace=True)
            result_ori = pd.DataFrame(columns=('scores',))
            
            #result_ori.index.name = "code"
            #fund_nav_rates.fillna(0, inplace=True)
            #fund_nav_rates = fund_nav_rates.drop(list(fund_nav_rates.index)[0])
            for code in list(fund_value.columns):
                md = get_maxdrawdown(fund_value[code])
                r = fund_value[code][-1] / fund_value[code][0] - 1
                result_ori.loc[code] = r / md
            #print(result_ori)
            result_sort = result_ori.sort_values(by='scores', ascending=False)
            
            temp = result_sort.iloc[0:top_n].dropna()
            #print(result_ori, temp)
            # 该时间区间的基金代码列表
            result = list(temp.index)
            # 将收益率值变换成序号，即大值小序号
            temp = temp.rank(ascending=False)
            # 列表中的每个基金出现次数加1
            rank._set_value(result, "times", np.ones(result.__len__()) + rank.loc[result, :].times)
            # 列表中每个基金累计上新的得分
            #print(rank, temp)
            rank._set_value(result, "scores", temp.scores + rank.loc[result, :].scores)
            #print(rank)
            results.append(result)
            
            '''
            # 按照最大涨幅/最大回撤排序
            result_fall = c.css(fund_pool_code, "MAXFALL",
                               "StartDate=" + previous_date.__str__() + ", EndDate=" + update_date.__str__() + ",RowIndex=1,Ispandas=1")
            result_rise = c.css(fund_pool_code, "MAXRISE",
                               "StartDate=" + previous_date.__str__() + ", EndDate=" + update_date.__str__() + ",RowIndex=1,Ispandas=1")
            result_fall['MAXFALL'] = -result_fall['MAXFALL']
            result_fall.fillna(999)
            result_fall['MAXFALL'][result_fall['MAXFALL'] == 0] = 0.01
            result_ori = result_rise['MAXRISE'] / result_fall['MAXFALL']
            #print(result_ori)
            result_sort = result_ori.sort_values(ascending=False)
            temp = result_sort.iloc[0:top_n].dropna()
            '''
        elif fund_pool_fun == 'drawdown2':
            pass
        '''
        # 该时间区间的基金代码列表
        result = list(temp.index)
        # 将收益率值变换成序号，即大值小序号
        temp = temp.rank(ascending=False)
        # 列表中的每个基金出现次数加1
        rank._set_value(result, "times", np.ones(result.__len__()) + rank.loc[result, :].times)
        # 列表中每个基金累计上新的得分
        #print(rank, temp)
        rank._set_value(result, "scores", temp.scores + rank.loc[result, :].scores)
        s
        # 对没有排名的基金特别照顾,但必须大于半年的业绩才可特别入池
        if ind > 180:
            #is_na = result_sort.iloc[:, 1].isna()
            is_na = result_sort.isna()
            tt = list(result_sort[is_na].index)
            result = result + tt
        
        results.append(result)
        #print(rank)
        '''
    # 基金进行过滤，每个区间列表相交
    ss = list(results[0])
    for ind in results:
        ss = list(set(ss).intersection(set(ind)))
    #print(ss)
    # 计算每个基金的评分信息
    res = rank.loc[ss, :]
    res.scores = res.scores / res.times
    res = res.sort_values("scores").iloc[:, 1]
    # 存储候选池基金全部信息         #zym
    res.to_csv(os.path.join(os.path.dirname(__file__) ,"vill","results","fundpool_" + fund_pool_fun + ".csv"), index=True, encoding="utf_8_sig")
    res.to_csv(os.path.join(os.path.dirname(__file__) ,"vill","snapshots","fundpool_" + fund_pool_fun + "_" + update_date.__str__() + ".csv"), index=True,
              encoding="utf_8_sig")

    return res
    '''
    # 将基金池的全部信息都存储在表格中
    #data = c.css(res.index.tolist(),
    #             "NAME,FOUNDDATE,INVESTSTYLE,FUNDSCALE,MAXPURCHFEERATIO,MAXREDEMFEERATIO,FUNDMANAGER,"
    #             "BENCHMARK,PURCHSTATUS,REDEMSTATUS,PURCHFEERATIO,REDEMFEERATIO", "EndDate="
    #             + update_date.__str__() + ", TradeDate=" + update_date.__str__() + ",FeeType=1, Ispandas=1, "
    #                                                                                "RowIndex=1")
    
    # 获取基金的得分信息
    res_rank = res[data.index].astype("int")
    # 删除日期信息
    da = data.drop("DATES", axis=1)
    # 加入得分信息
    da.insert(0, "Scores", res_rank)
    # 根据得分对基金进行排序
    da = da.sort_values(by="Scores")
    # 存储候选池基金全部信息
    da.to_csv(os.getcwd() + "\\vill\\results\\fundpool_" + fund_pool_fun + ".csv", index=True, encoding="utf_8_sig")
    da.to_csv(os.getcwd() + "\\vill\\snapshots\\fundpool_" + fund_pool_fun + "_" + update_date.__str__() + ".csv", index=True,
              encoding="utf_8_sig")

    print("基金池更新完毕")
    fund_pool = ss

    if return_detail:
        return da
    else:
        return fund_pool
    '''

    # 判断数据源类型：EM：东方财富choice；WIND：万得金融wind


# ----------------------------------------------------------------------------------------#
#                   函数功能：基金收益率序列
#       默认参数：
#           1、不更新基金收益率序列，一般一周更新一次
#           2、不更新基金池，一般一周更新一次
#           3、如若更新，更新截止日期为运行当
# ----------------------------------------------------------------------------------------#

def get_nav_rates(fund_nav_update=False, fund_pool_update=False, begin_date="2019-10-17",
                  end_date=date.today(), fund_pool_fun='return'):
    """
    :param fund_pool_fun:
    :param fund_nav_update: 基金收益率序列是否更新
    :param fund_pool_update: 基金池是否更新
    :param begin_date: 序列起始日期
    :param end_date: 序列截止日期
    :return: 基金收益率序列

    """

    global fund_nav_rates

    # 提前一天的净值才可以
    _end_date = end_date - timedelta(1)

    # 更新标志为假，无需更新
    if not fund_nav_update:
        print("----------------")
        print("基金净值无需更新")
        print("----------------")

        # 读取候选基金池                #zym
        fund_nav_rates = pd.read_csv(os.path.join(os.path.dirname(__file__) , "vill","snapshots","fund_nav_rate_" + fund_pool_fun + "_" + end_date.__str__() + ".csv"), index_col=0, header=None, dtype=object)  # 读取基金收益率数据
        return fund_nav_rates

    print("----------------")
    print("开始更新基金净值")
    print("----------------")
    # 读取基金池信息
    res = get_fund_pool(fund_pool_update=fund_pool_update, update_date=end_date, return_detail=False, fund_pool_fun=fund_pool_fun)
    data = pd.DataFrame()
    #print(res, begin_date)
    bd = datetime.strptime(begin_date, "%Y-%m-%d").date()
    while True:
        ed = bd + timedelta(10)
        tmp = finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code.in_(res), finance.FUND_NET_VALUE.day>bd, finance.FUND_NET_VALUE.day<=ed))
        
        data = pd.concat([data, tmp])
        if ed >= end_date:
            break
        bd = ed
        
    #print(data)
        #print(ed)
    # 读取候选基金净值信息
    #data = c.csd(res, "ADJUSTEDNAVRATE", begin_date, _end_date.__str__(), "period=1,adjustflag=1,curtype=1,"
    #                                                                      "pricetype=1,order=1,market=CNSESH,"
    #                                                                      "Ispandas=1,RowIndex=2")

    # 格式变换
    #fund_nav_rates = data.reset_index().pivot("DATES", "CODES", "ADJUSTEDNAVRATE") / 100.

    fund_value = data.reset_index().pivot("day", "code", "sum_value")
    #print(fund_value)
    fund_nav_rates = fund_value.pct_change()
    #print(fund_nav_rates)
    #print(fund_nav_rates)

    '''
    重要操作，这里将收益率变换成和沪深300相比的超额收益率，与择时标准匹配
    '''
    #hs300 = c.csd("000300.SH", "PCTCHANGE", begin_date, _end_date.__str__(),
    #              "period=1, adjustflag=1, curtype=1, pricetype=1, order=1, market=CNSESH, Ispandas=1, RowIndex=2")
    #hs300 = hs300.reset_index().pivot("DATES", "CODES", "PCTCHANGE") / 100.
    hs300 = get_price('000300.XSHG', start_date=begin_date, end_date=end_date.__str__(), frequency='daily')
    hs300_ret = hs300.close / hs300.open - 1
    hs300 = pd.DataFrame(hs300_ret, index=hs300.index)
    # 每一列都减去hs300当天增长率
    fund_nav_rates = fund_nav_rates.sub(hs300.iloc[:, 0], axis=0)
    fund_nav_rates = pd.DataFrame(fund_nav_rates)
    # 净值信息进行存储                                     #zym
    pd.DataFrame.to_csv(pd.DataFrame(fund_nav_rates), os.path.join(os.path.dirname(__file__) ,"vill","results","fund_nav_rate_" + fund_pool_fun + ".csv"), index=True)
    pd.DataFrame.to_csv(pd.DataFrame(fund_nav_rates),
                        os.path.join(os.path.dirname(__file__), "vill","snapshots","fund_nav_rate_" + fund_pool_fun + "_" + end_date.__str__() + ".csv"), index=True)
    # 读取基金收益率数据
    # fund_nav_rates = pd.read_csv(os.getcwd() + "\\vill\\snapshots\\fund_nav_rate_" + fund_pool_fun + "_" + end_date.__str__() + ".csv", index_col=0)
    print("----------------")
    print("基金净值更新完毕")
    print("----------------")

    return fund_nav_rates


def get_previous_date(interval, end_date):
    previous_dates = []
    for ind in interval:
        tmp_date = end_date - timedelta(ind)   #zym 
        #print(tmp_date)
        previous_dates.append(get_trade_days(end_date=tmp_date.__str__(), count=1)[0])
    return previous_dates


def get_maxdrawdown(return_list):
    # 计算最大回撤率
    i = np.argmax((np.maximum.accumulate(return_list) - return_list) / (np.maximum.accumulate(return_list) + 1e-3))  # 结束位置
    if i == 0:
        return 0
    j = np.argmax(return_list[:i])  # 开始位置
    return (return_list[j] - return_list[i]) / (return_list[j])

if __name__ == '__main__':
    #c.start("ForceLogin=1", 'TestLatency =1', '')
    auth('13739188902', 'ZNnb20160801')
    #fund_pool = get_fund_pool(fund_pool_update=True, return_detail=True, fund_pool_fun='return',
    #                          update_date=datetime.strptime('20191225', "%Y%m%d").date())
    nav_rates = get_nav_rates(fund_nav_update=True, fund_pool_update=False, fund_pool_fun='return',
                              end_date=datetime.strptime('20191225', "%Y%m%d").date())

    #print(fund_pool)
    #print(nav_rates)
