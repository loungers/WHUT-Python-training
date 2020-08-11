import tushare as ts
import pymysql
import pandas as pd
from sklearn.cluster import KMeans


def Stock_pool():
    ts.set_token('eb13b3bfd2bd07fd9eb40234f19941c73f230e1e98cc212b8cd407c7')
    pro = ts.pro_api()
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    stocks = data[data['industry'] == '化学制药'].ts_code
    data1 = pd.DataFrame(columns=['ts_code', 'end_date', 'n_income', 'cash_flow'])
    for stock in stocks:
        df = pro.income(ts_code=stock, period='20191231', fields='ts_code,end_date,n_income')
        df['cash_flow'] = pro.cashflow(ts_code=stock, period='20191231').im_net_cashflow_oper_act
        print(df)
        data1 = pd.concat([data1, df], axis=0)

    data1 = data1.dropna()  # 去除空值
    data1 = data1.set_index('ts_code')

    model = KMeans(n_clusters=3, random_state=0)
    model = model.fit(data1[['n_income', 'cash_flow']])
    data1['pre'] = model.predict(data1[['n_income', 'cash_flow']])
    print(data1['pre'].value_counts())

    stock_pool = list(data1['pre'][data1['pre'].values == 1].index)
    return stock_pool

