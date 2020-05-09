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

def get_stockcode():
    df = ts.get_today_all()
    df1 = pd.DataFrame(df, columns=('code','name'))
    df1.to_csv('stockcode_from_ts.txt',header=None,index=False,sep=' ',encoding='utf_8_sig')

def get_300code():
    df=ts.get_hs300s()
    df1=df['code']
    #df1 = pd.DataFrame(df, columns=('code'))
    return df1.tolist()


def get_stock(code,nday,eday):
    now_day = time.strftime('%Y-%m-%d')
    todaydate=datetime.datetime.strptime(now_day,"%Y-%m-%d")
    lenDay=str(nday-eday)
    filename = './result/' + now_day + '_'+lenDay+'result.txt'
    fp1 = open(filename, 'a')
    while(nday>eday):
        # 以查询截止日期为文件名保存结果文件      
        preDay=todaydate-timedelta(days=nday)
        preDaystr=preDay.date().strftime("%Y-%m-%d")       
        #print('%s %s',preDaystr,now_day)
        # 用try为了避免有些股票没有数据而报错
        try:
            # 获取股票数据从前一天开始到当天的数据
            df = ts.get_hist_data(code, start=preDaystr, end=preDaystr)
            #print(df)
            ma_line = pd.DataFrame(df, columns=('close','ma5', 'ma10', 'ma20','v_ma5','v_ma10','v_ma20'))
            close = float('%.2f' % ma_line.iloc[0,0])
            ma5_value = float('%.2f' % ma_line.iloc[0,1])
            ma10_value = float('%.2f' % ma_line.iloc[0,2])
            ma20_value = float('%.2f' % ma_line.iloc[0,3])
            #sname ='哈哈哈哈'
            sname= get_name(code)
            print('------%s:%s 日均线 ma5:%s ma10:%s ma20:%s--------' % (code,sname, ma5_value,ma10_value,ma20_value))
            #判断策略为收盘价突破5日线，且5日线低于10日线。
            #if close>ma5_value and ma5_value > ma10_value and ma10_value > ma20_value:
            if close>ma5_value and ma5_value < ma10_value:
                print('%s日-->%s:%s 日均线上行 close:%s ma5:%s ma10:%s ma20:%s' % (preDaystr,code,sname, close,ma5_value,ma10_value,ma20_value))
                if(nday==eday+1):
                    fp1.write('%s,%s,%s,日均线上行,close:%s ma5:%s ma10:%s ma20:%s \n' % (preDaystr,code,sname,close, ma5_value,ma10_value,ma20_value))
            else:
                break
        except:
            pass
        nday = nday -1
    fp1.close()

if __name__ == '__main__':
    #fp = open('stockcode_from_ts.txt')
    #fp = open('stock_code_all.txt')
    #fp = open('monitor_code.txt')
    #fp = open('hs300.txt')
    #codes = fp.readlines()
    codes=get_300code()
    print(codes)
    n=2
    e=1
    #遍历所有的股票
    for code in codes:
        #code_all = code.strip('\n')
        get_stock(code,n,e)
    #fp.close()
    #get_stockcode()
