import datetime
import tushare as ts
import pymysql
import StockPool
import pandas as pd
from  sklearn.cluster import KMeans
if __name__ == '__main__':

    # 设置tushare pro的token并获取连接
    ts.set_token('eb13b3bfd2bd07fd9eb40234f19941c73f230e1e98cc212b8cd407c7')
    pro = ts.pro_api()
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20180201'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = time_temp.strftime('%Y%m%d')
    # 建立数据库连接,剔除已入库的部分
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='000109', db='stock_list', charset='utf8')
    cursor = db.cursor()
    设定需要获取数据的股票池
    # data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    #     # stocks = data[data['industry'] == '化学制药'].ts_code
    #     # data1 = pd.DataFrame(columns=['ts_code', 'end_date', 'n_income', 'cash_flow'])
    #     # for stock in stocks:
    #     #     df = pro.income(ts_code=stock, period='20191231', fields='ts_code,end_date,n_income')
    #     #     df['cash_flow'] = pro.cashflow(ts_code=stock, period='20191231').im_net_cashflow_oper_act
    #     #     print(df)
    #     #     data1 = pd.concat([data1, df], axis=0)
    #     #
    #     # data1 = data1.dropna()  # 去除空值
    #     # data1 = data1.set_index('ts_code')
    #     #
    #     # model = KMeans(n_clusters=3, random_state=0)
    #     # model = model.fit(data1[['n_income', 'cash_flow']])
    #     # data1['pre'] = model.predict(data1[['n_income', 'cash_flow']])
    #     # print(data1['pre'].value_counts())
    #     #
    #     # stock_pool = list(data1['pre'][data1['pre'].values == 1].index)
    #     # stock_pool = StockPool.Stock_pool()

    stock_pool = ['603912.SH','300666.SZ','300618.SZ','002049.SZ','300672.SZ']
    total = len(stock_pool)
    # 循环获取单个股票的日线行情
    for i in range(len(stock_pool)):
        try:
            df = pro.daily(ts_code=stock_pool[i], start_date=start_dt, end_date=end_dt)
			# 打印进度
            print('Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            c_len = df.shape[0]
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue
        for j in range(c_len):
            resu0 = list(df.loc[c_len-1-j])
            resu = []
            for k in range(len(resu0)):
                if str(resu0[k]) == 'nan':
                    resu.append(-1)
                else:
                    resu.append(resu0[k])
            state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            try:
                sql_insert = "INSERT INTO stock_all(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt" \
                             "_change,pct_change) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f" \
                             "','%.2f','%.2f')" % (state_dt,str(resu[0]),float(resu[2]),float(resu[5]),float(resu[3])
                                                                                ,float(resu[4]),float(resu[9]),float
                                                                                (resu[10]),float(resu[6]),
                                                   float(resu[7]),float(resu[8]))
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                print(err)
                continue
    cursor.close()
    db.close()
    print('All Finished!')
