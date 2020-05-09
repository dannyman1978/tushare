import tushare as ts
import pandas as pd
import datetime
import time
from datetime import timedelta

ts.set_token('9c3c86e6a202410d0b9f3f406dca2b4216d9e5ed48ef7f36b26f324d') #请注册使用自己的TS key，这个key没用
pro = ts.pro_api()

def get_name(x): #返回股票名字
    #df = pro.namechange(ts_code=x, fields='name')
    df = ts.get_realtime_quotes(x) #Single stock symbol
    return df.iloc[0,0]

#回测函数
def get_stock_close(day,code):
    # 查询指定代码，日期之后一天的收盘价
    bdate=datetime.datetime.strptime(day,"%Y-%m-%d")
    closeDay=bdate+timedelta(days=1)
    closeDayStr=closeDay.date().strftime("%Y-%m-%d")
    filename = './result/' +'hcclose_result.txt'
    fp1 = open(filename, 'a')
    #print('%s %s',preDaystr,now_day)
    # 用try为了避免有些股票没有数据而报错
    try:
        # 获取股票数据从前一天开始到当天的数据
        df = ts.get_hist_data(code, start=closeDayStr, end=closeDayStr)
        #print(df)
        ma_line = pd.DataFrame(df, columns=('close','high', 'low', 'p_change'))
        close = float('%.2f' % ma_line.iloc[0,0])
        high = float('%.2f' % ma_line.iloc[0,1])
        low = float('%.2f' % ma_line.iloc[0,2])
        p_change = float('%.2f' % ma_line.iloc[0,3])
        #sname ='哈哈哈哈'
        sname= get_name(code)
        if p_change>0:
            print('【%s】:%s 回测上涨 收盘价:%s 最高价:%s 最低价:%s 涨跌幅:%s' % (code,sname, close,high,low,p_change))
            fp1.write('【%s】:%s 回测上涨 收盘价:%s 最高价:%s 最低价:%s 涨跌幅:%s\n' % (code,sname, close,high,low,p_change))
        elif p_change<0:
            print('%s:%s 回测下跌 收盘价:%s 最高价:%s 最低价:%s 涨跌幅:%s' % (code,sname, close,high,low,p_change))
            fp1.write('%s:%s 回测下跌 收盘价:%s 最高价:%s 最低价:%s 涨跌幅:%s\n' % (code,sname, close,high,low,p_change))
        else:
            print('%s:%s 回测平盘 收盘价:%s 最高价:%s 最低价:%s 涨跌幅:%s' % (code,sname, close,high,low,p_change))
            fp1.write('%s:%s 回测平盘 收盘价:%s 最高价:%s 最低价:%s 涨跌幅:%s\n' % (code,sname, close,high,low,p_change))
    except:
        pass
    fp1.close()

if __name__ == '__main__':
    fp = open('./result/hcclose.txt')
    lines = fp.readlines()
    #print(lines)
    # 遍历所有的股票
    for linestr in lines:
        tmpstr=linestr.strip('\n').split(',')
        date = tmpstr[0]
        code = tmpstr[1]    
        print(date+'---'+code)
        get_stock_close(date,code)
    fp.close()

