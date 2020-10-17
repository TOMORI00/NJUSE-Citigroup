tmpdata = selldata.loc[date, :]
                    sell_a = {}
                    if type(selldata.loc[date, '赎回份额'])==str:
                        sell_a[selldata.loc[date, '基金代码']] = float(selldata.loc[date, '赎回份额'])
                        s += 1
                    else:
                        for j in range(len(tmpdata)):
                            sell_a[tmpdata.iloc[j, 0]] = float(tmpdata.iloc[j, 2])
                        s += len(tmpdata)
                    if date not in data.index:
                        close = 1
                    else:
                        close = data.loc[date, code] 
                    for code in sell_a.keys():
                        sell_a[code]*=close
                        m+=sell_a[code]