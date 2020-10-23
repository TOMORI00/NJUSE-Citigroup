# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from progressbar import *
from datetime import date
from scipy.stats.mstats import gmean
from cvxopt import matrix, solvers
import os


def describe(return_table=None, is_print=True):
    """
    输出收益率矩阵的描述性统计量，包括：
        年化收益率
        年化标准差
        相关系数矩阵

    :param return_table: (DataFrame)收益率矩阵，列为资产，值为按日期升序排列的收益率
    :param is_print: (bool)是否直接输出

    :return: (dict)描述性统计量字典，键为"annualized_return", "annualized_volatility", "covariance_matrix"和"coefficient_matrix"
    """

    # 求期望收益时，必须去掉NaN
    output = {'annualized_return': pd.DataFrame(dict(zip(return_table.columns,
                                                         [gmean(return_table.loc[:, ind].dropna() + 1.) ** 250 - 1. for
                                                          ind in return_table.columns])), index=[0],
                                                columns=return_table.columns),
              'annualized_volatility': pd.DataFrame(return_table.std() * np.sqrt(250)).T,
              'covariance_matrix': return_table.cov() * 250., 'coefficient_matrix': return_table.corr()}

    if is_print:
        for key, val in output.items():
            print("{}:\n{}\n".format(key, val))

    return output


def get_efficient_frontier(return_table=None, up_limit=None, allow_short=False, n_samples=50):
    """
    计算Efficient Frontier

    :param return_table: (DataFrame) 收益率矩阵，列为资产，值为按日期升序排列的收益率
    :param up_limit: (list) 每个资产占组合中的比例上限
    :param allow_short: (bool) 是否允许做空
    :param n_samples: (int) 用于计算Efficient Frontier的采样点数量

    :return: (DataFrame) Efficient Frontier的结果，列为"returns", "risks", "weights"
    """

    assets = return_table.columns
    n_asset = len(assets)
    if n_asset < 2:
        raise ValueError("There must be at least 2 assets to calculate the efficient frontier!")

    output = describe(return_table=return_table, is_print=False)
    covariance_matrix = matrix(output['covariance_matrix'].values)
    expected_return = output['annualized_return'].iloc[0, :].values

    risks, returns, weights = [], [], []

    # 进度计次
    times = 0
    # 开始进度条
    pbar = ProgressBar().start()

    # 对期望收益进行穷举采样
    for level_return in np.linspace(min(expected_return), max(expected_return), n_samples):
        # 更新进度条
        #pbar.update(int((times / n_samples) * 100))

        # --------- 二次规划参数设置 ---------- #
        #
        #  minimize     (1/2)*x'*P*x + q'*x
        #  subject to   G*x <= h
        #               A*x = b.
        #
        # - P is a n x n dense or sparse 'd' matrix with the lower triangular part of P stored in the lower triangle.
        # Must be positive semidefinite.
        #
        # - q is an n x 1 dense 'd' matrix.
        #
        # - G is an m x n dense or sparse 'd' matrix.
        #
        # - h is an m x 1 dense 'd' matrix.
        #
        # - A is a p x n dense or sparse 'd' matrix.
        #
        # - b is a p x 1 dense 'd' matrix or None.
        #
        #  solver is None or 'mosek'.
        #
        #  The default values for G, h, A and b are empty matrices with zero rows.
        # ----------------------------------- #

        P = 2 * covariance_matrix
        # print("P=\n", np.matrix(P))
        q = matrix(np.zeros(n_asset))
        # print("q=\n", np.matrix(q))

        if allow_short:
            G = matrix(np.row_stack((matrix(0., (n_asset, n_asset)), np.diag(1. * np.ones(n_asset)))))
        else:
            G = matrix(np.row_stack((np.diag(-1 * np.ones(n_asset)), np.diag(1. * np.ones(n_asset)))))
        # print("G=\n", np.matrix(G))
        h = matrix(np.row_stack((matrix(0., (n_asset, 1)), matrix(list(up_limit)))))
        # print("h=\n",np.matrix(h))
        A = matrix(np.row_stack((np.ones(n_asset), expected_return)))
        # print("A=\n", np.matrix(A))
        b = matrix([1.0, level_return])
        # print("b=\n", np.matrix(b))
        solvers.options['show_progress'] = False

        # 迭代次数默认为100，如果失败，则每次降低15
        maxiters = 100
        while maxiters > 40:
            try:
                sol = solvers.qp(P, q, G, h, A, b)
                maxiters = 0
            except Exception as e:
                print(e, maxiters)
                maxiters -= 10
                solvers.options['maxiters'] = maxiters

        # 此处加一个判断，去除非最优解的情况 Terminated (singular KKT matrix).
        if sol['status'] == 'optimal':
            risks.append(np.sqrt(sol['primal objective']))
            returns.append(level_return)
            weights.append(dict(zip(assets, list(sol['x'].T))))
        # print("状态：", sol['status'])
        # print("weights=\n", np.matrix(sol['x']))
        times += 1
    pbar.finish()
    output = {"returns": returns,
              "risks": risks,
              "weights": weights}
    output = pd.DataFrame(output)
    return output


def draw_efficient_frontier(efficient_frontier_output):
    """
    绘出Efficient Frontier

    Args:
        efficient_frontier_output: Efficient Frontier的计算结果，即get_efficient_frontier的输出
    """

    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot(111)
    ax.plot(efficient_frontier_output['risks'], efficient_frontier_output['returns'])
    ax.set_title('Efficient Frontier', fontsize=14)
    ax.set_xlabel('Standard Deviation', fontsize=12)
    ax.set_ylabel('Expected Return', fontsize=12)
    ax.tick_params(labelsize=12)
    #plt.show()





def get_minimum_variance_portfolio(return_table=None, allow_short=False, show_details=True):
    """
    计算最小方差组合

    Args:
        return_table (DataFrame): 收益率矩阵，列为资产，值为按日期升序排列的收益率
        allow_short (bool): 是否允许卖空
        show_details (bool): 是否显示细节

    Returns:
        dict: 最小方差组合的权重信息，键为资产名，值为权重
    """

    assets = return_table.columns
    n_asset = len(assets)
    if n_asset < 2:
        weights = np.array([1.])
        weights_dict = {assets[0]: 1.}
    else:
        output = describe(return_table, is_print=False)
        covariance_matrix = matrix(output['covariance_matrix'].as_matrix())
        # expected_return = output['annualized_return'].iloc[0, :].as_matrix()

        P = 2 * covariance_matrix
        q = matrix(np.zeros(n_asset))

        if allow_short:
            G = matrix(0., (n_asset, n_asset))
        else:
            G = matrix(np.row_stack((np.diag(-1 * np.ones(n_asset)), np.diag(1. * np.ones(n_asset)))))

        h1 = matrix(0., (n_asset, 1))
        h2 = matrix(0.35, (n_asset, 1))
        h = matrix(np.row_stack((h1, h2)))
        A = matrix(np.ones(n_asset)).T
        b = matrix([1.0])
        solvers.options['show_progress'] = False
        sol = solvers.qp(P, q, G, h, A, b)
        weights = np.array(sol['x'].T)[0]
        weights_dict = dict(zip(assets, weights))

    r = np.dot(weights, output['annualized_return'].iloc[0, :].as_matrix())
    v = np.sqrt(np.dot(np.dot(weights, covariance_matrix), weights.T))

    if show_details:
        print(
            """
Minimum Variance Portfolio:
    Short Allowed: {}
    Portfolio Return: {}
    Portfolio Volatility: {}
    Portfolio Weights: {}
""".format(allow_short, r, v, "\n\t{}".format("\n\t".join("{}: {:.1%}".format(k, v) for k, v in weights_dict.items()))).strip())

    return weights_dict


def get_maximum_utility_portfolio(return_table, risk_aversion=3., allow_short=False, show_details=True, up_limit=None, max_num=4):
    """
    计算最大效用组合，目标函数为：期望年化收益率 - 风险厌恶系数 * 期望年化方差

    Args:
        return_table (DataFrame): 收益率矩阵，列为资产，值为按日期升序排列的收益率
        risk_aversion (float): 风险厌恶系数，越大表示对风险越厌恶，默认为3.0
        allow_short (bool): 是否允许卖空
        show_details (bool): 是否显示细节

    Returns:
        dict: 最小方差组合的权重信息，键为资产名，值为权重
        :param up_limit:
    """

    assets = return_table.columns
    n_asset = len(assets)
    if n_asset < 2:
        weights = np.array([1.])
        weights_dict = {assets[0]: 1.}
        return weights_dict, ' '
    else:
        output = describe(return_table, is_print=False)
        covariance_matrix = matrix(output['covariance_matrix'].as_matrix())
        expected_return = output['annualized_return'].iloc[0, :].as_matrix()

        if abs(risk_aversion) < 0.01:
            max_ret = max(expected_return)
            weights = np.array([1. if expected_return[i] == max_ret else 0. for i in range(n_asset)])
            weights_dict = {asset: weights[i] for i, asset in enumerate(assets)}
        else:
            P = risk_aversion * covariance_matrix
            q = matrix(-expected_return.T)
            '''
            if allow_short:
                G = matrix(0., (n_asset, n_asset))
            else:
                G = matrix(np.diag(-1 * np.ones(n_asset)))

            h = matrix(0., (n_asset, 1))
            '''

            if allow_short:
                G = matrix(np.row_stack((matrix(0., (n_asset, n_asset)), np.diag(1. * np.ones(n_asset)))))
            else:
                G = matrix(np.row_stack((np.diag(-1 * np.ones(n_asset)), np.diag(1. * np.ones(n_asset)))))
            # print("G=\n", np.matrix(G))
            h = matrix(np.row_stack((matrix(0., (n_asset, 1)), matrix(list(up_limit)))))

            A = matrix(np.ones(n_asset)).T
            b = matrix([1.0])
            solvers.options['show_progress'] = False
            sol = solvers.qp(P, q, G, h, A, b)
            weights = np.array(sol['x'].T)[0]
            weights_dict = dict(zip(assets, weights))
    ww = pd.DataFrame.from_dict(weights_dict, orient='index')
    tmp = ww[ww.iloc[:, 0] > 0.001]

    if len(tmp) > max_num:
        asset_index = sorted(weights_dict, key=weights_dict.__getitem__,reverse=True)[:max_num]
        column = list(return_table.columns)
        up_limit_index = []
        for ai in asset_index:
            up_limit_index.append(column.index(ai))
        up_limit = np.array(up_limit)[up_limit_index]
        return_table = return_table.loc[:, asset_index].dropna()
        output = describe(return_table, is_print=False)
        covariance_matrix = matrix(output['covariance_matrix'].as_matrix())
        expected_return = output['annualized_return'].iloc[0, :].as_matrix()
        assets = return_table.columns
        n_asset = len(assets)

        P = risk_aversion * covariance_matrix
        q = matrix(-expected_return.T)

        if allow_short:
            G = matrix(np.row_stack((matrix(0., (n_asset, n_asset)), np.diag(1. * np.ones(n_asset)))))
        else:
            G = matrix(np.row_stack((np.diag(-1 * np.ones(n_asset)), np.diag(1. * np.ones(n_asset)))))
        h = matrix(np.row_stack((matrix(0., (n_asset, 1)), matrix(list(up_limit)))))
        A = matrix(np.ones(n_asset)).T
        b = matrix([1.0])
        solvers.options['show_progress'] = False
        sol = solvers.qp(P, q, G, h, A, b)
        weights = np.array(sol['x'].T)[0]
        weights_dict = dict(zip(assets, weights))

    r = np.dot(weights, output['annualized_return'].iloc[0, :].as_matrix())
    v = np.sqrt(np.dot(np.dot(weights, covariance_matrix), weights.T))

    if show_details:
        print(
            """
Maximum Utility Portfolio:
    Risk Aversion: {}
    Short Allowed: {}
    Portfolio Return: {}
    Portfolio Volatility: {}
    Portfolio Weights: {}
""".format(risk_aversion, allow_short, r, v,
           "\n\t{}".format("\n\t".join("{}: {:.1%}".format(k, v) for k, v in weights_dict.items()))).strip())

    details = """Return: {}   Volatility: {}""".format(str(round(100 * r, 2)) + "%", str(round(100 * v, 2)) + "%").strip()

    return weights_dict, details


def get_maximum_sharpe_portfolio(return_table=None, up_limit=None, riskfree_rate=0.03, allow_short=False, show_details=True,
                                 low_limit=None, max_num=4):
    """
    计算最大效用组合，目标函数为：（期望年化收益率 - 无风险收益率）/ 期望年化方差

    :rtype:
    :param return_table: (DataFrame) 收益率矩阵，列为资产，值为按日期升序排列的收益率
    :param up_limit:
    :param riskfree_rate: (float) 无风险收益率
    :param allow_short: (bool) 是否允许卖空
    :param show_details: (bool) 是否显示细节
    :param low_limit:

    :return: (dict) 最小方差组合的权重信息，键为资产名，值为权重
    """

    assets = return_table.columns
    n_asset = len(assets)
    if n_asset < 2:
        output = describe(return_table, is_print=False)
        r = output['annualized_return'].iat[0, 0]
        v = output['annualized_volatility'].iat[0, 0]
        weights_dict = {assets[0]: 1.}
    else:
        #print(return_table)
        efs = get_efficient_frontier(return_table=return_table, up_limit=up_limit, allow_short=allow_short, n_samples=500)
        #draw_efficient_frontier(efs)
        if efs.empty:
            print(efs)
            w = 1 / len(assets)
            weights_dict = {}
            for a in assets:
                weights_dict[a] = w
        else:
            i_star = max(range(efs.__len__()), key=lambda x: (efs.at[x, "returns"] - riskfree_rate) / efs.at[x, "risks"])
            r = efs.at[i_star, "returns"]
            v = efs.at[i_star, "risks"]
            weights_dict = efs.at[i_star, "weights"]
    ww = pd.DataFrame.from_dict(weights_dict, orient='index')
    tmp = ww[ww.iloc[:, 0] > 0.001]
    if len(tmp) > max_num:
        asset_index = sorted(weights_dict, key=weights_dict.__getitem__,reverse=True)[ : max_num]
        column = list(return_table.columns)
        up_limit_index = []
        for ai in asset_index:
            up_limit_index.append(column.index(ai))
        up_limit = np.array(up_limit)[up_limit_index]
        return_table = return_table.loc[: , asset_index].dropna()
        efs = get_efficient_frontier(return_table=return_table, up_limit=up_limit, allow_short=allow_short, n_samples=500)
        #draw_efficient_frontier(efs)
        i_star = max(range(efs.__len__()), key=lambda x: (efs.at[x, "returns"] - riskfree_rate) / efs.at[x, "risks"])
        r = efs.at[i_star, "returns"]
        v = efs.at[i_star, "risks"]
        weights_dict = efs.at[i_star, "weights"]
        
    '''
    s = (r - riskfree_rate) / v
    #print("有效结果数：%0.2f%%" % (efs.__len__()/500*100))
    details1 = """
Maximum Sharpe Portfolio:
    Riskfree Rate: {}
    Short Allowed: {}
    Portfolio Return: {}
    Portfolio Volatility: {}
    Portfolio Sharpe: {}
    Portfolio Weights: {}
""".format(riskfree_rate, allow_short, r, v, s,
           "\n\t{}".format("\n\t".join("{}: {:.1%}".format(k, v) for k, v in weights_dict.items()))).strip()

    details = """Return: {}   Volatility: {}   Sharpe Ratio: {}
    """.format(str(round(100 * r, 2)) + "%", str(round(100 * v, 2)) + "%", round(s, 2)).strip()

    if show_details:
        print(details1)
    '''
    return weights_dict


def draw_picture(results=None, details=None, portfolio_scale=0, end_date=date.today(), fun='', fund_pool_fun=''):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.figure(figsize=(8, 9), dpi=300)  # 以上代码为画图初始化设置
    labels = list(results.index)  # 标签，即种类
    sizes = list(results.iloc[:, 0] * 1000)  # 比例
    # Colors used. Recycle if not enough.
    colors = ['#eaff56', '#ff7500', '#f9906f', '#44cef6', '#cca4e3', '#ff03a7']  # 设置颜色（循环显示）
    # colors=['#fcefe8','#e9e7ef','#fff2df','#f0f0f4','#f2ecde','#f0fcff']#,'#e3f9fd','#d6ecf0','#fffbf0','#f3f9f1']
    # colors = ['#9d2933','#003472',"#cca4e3","#50616d","#48c0a3", "#ffa631"]
    # For China, make the piece explode a bit
    expl = np.ones(labels.__len__()) * 0.05
    # expl[results.iloc[:,0].values.argmax()]=0.1    # 第一块即China离开圆心0.1

    patches, l_text, p_text = plt.pie(sizes, explode=expl, labels=labels, rotatelabels=True, colors=colors,
                                      autopct='%1.2f%%',
                                      shadow=False, labeldistance=0.6, pctdistance=0.4,
                                      textprops={'fontsize': 12, 'color': '#065279'})  # 画图函数
    # 图例中加上百分比信息
    sizes = [float("%.2f" % (x / sum(sizes) * 100)) for x in sizes]
    pct = [str(x) + "%" for x in sizes]
    labels = [labels[i] + "-" + pct[i] for i in range(len(pct))]
    plt.legend(handles=patches, labels=labels, ncol=3, loc="best", mode="expand", framealpha=0, fontsize=12,
               title=None)
    # 获取legend中的文字
    x = plt.gca().get_legend().get_texts()
    # 将文字颜色修改
    for t in x:
        t.set_color("#065279")
    plt.title('Fund Portfolio', fontsize=20, fontweight='black', color='#065279')
    plt.axis('equal')  # 让保持圆形
    #plt.annotate(details, xy=(0, 0), xytext=(-1, -1.2), color='#065279', size=13)
    plt.savefig(os.path.dirname(__file__) + "\\vill\\results\\portfolio_" + end_date.__str__() + ".png",
                format='png', bbox_inches='tight')
    plt.savefig(os.path.dirname(__file__) + "\\vill\\snapshots\\portfolio_" + end_date.__str__() + ".png",
                format='png', bbox_inches='tight')
    #plt.show()  # 让图形显现
    # plt.close()


if __name__ == '__main__':           #zym
    df = pd.read_csv(os.path.dirname(__file__) + "\\vill\\results\\fund_nav_rate.csv", index_col=0)  # 读取基金收益率数据
    df = df.iloc[:, 0:10]

#    describe(df, is_print=True)
#    efficient_frontier = get_efficient_frontier(return_table=df, up_limit=np.ones(len(df.columns)),allow_short=False, n_samples=1000)
#    draw_efficient_frontier(efficient_frontier)

    # get_minimum_variance_portfolio(return_table, allow_short=False, show_details=True)
    #w, detail = get_maximum_sharpe_portfolio(return_table=df, up_limit=np.ones(len(df.columns))*.35, riskfree_rate=0.03, allow_short=False, show_details=True)
    w, detail = get_maximum_utility_portfolio(return_table=df, risk_aversion=3., allow_short=False, show_details=True, up_limit=np.ones(len(df.columns))*.35,
                                              max_num=4)
    detail = detail + "\n" + "                Portfolio scale: " + int(10000000).__str__()
    ww = pd.DataFrame.from_dict(w, orient='index')
    result = ww[ww.iloc[:, 0] > 0.001]
    result.columns = ["weights"]
    result.index.name = "codes"
    result = result.sort_values("weights", ascending=False)

    draw_picture(result, detail)
