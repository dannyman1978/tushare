
# -*- coding: utf-8 -*-
 
import tushare as ts
import pandas as pd
import time
import datetime
from datetime import timedelta
from texttable import Texttable
 
# 读取Tushare的版本
vs = ts.__version__
print(vs)
# Your Account SID from twilio.com/console
account_sid = "AC4732c9c9cd73bef49e378c1479b3afed"
# Your Auth Token from twilio.com/console
auth_token  = "8df1d9d548fd3b2506d0b2a1d7241736"


def check(code):
    df=ts.get_realtime_quotes(code)
    e = df[['code', 'name', 'pre_close','price','high','low']]
    cp = float('%.3f' %df[u'price'])
    pp = float('%.3f' %df[u'pre_close'])
    pwave = float('%.3f' %((cp-pp)/pp*100.00))
    if pwave < 0:
        return 0,cp,pwave
    elif pwave > 0:
        return 1,cp,pwave
    else:
        return 2,cp,pwave


def show_price(tr_code,dfh):
    while True:

        df=ts.get_realtime_quotes(tr_code)
        dfr = pd.DataFrame(df, columns=('code','name','open','pre_close','price','high','low'))
        #dfr['涨跌']=pd.concat([(df['high']-df['low']),(df['high'] - df['pre_close'].shift(1)).abs(),(df['low'] - df['pre_close'].shift(1))], axis=1).max(axis=1)
        dfr['涨跌']=df.apply(lambda x: ((float(x['price']) - float(x['pre_close']))/float(x['pre_close']))*100, axis=1)
        dfr['持仓价']=dfh['hold_price']
        dfr['持股数']=dfh['hold_cnt']
        dfr['当日盈亏']=dfr.apply(lambda x: (float(x['price']) - float(x['pre_close']))*float(x['持股数']), axis=1)
        dfr['总盈亏']=dfr.apply(lambda x: (float(x['price']) - float(x['持仓价']))*float(x['持股数']), axis=1)
        total_twl=dfr['当日盈亏'].sum()
        total_wl=dfr['总盈亏'].sum()
        dfr=dfr.sort_values(by='总盈亏', ascending=False)
        tb=Texttable()
        tb.set_cols_align(['l','r','r','r','r','r','r','r','r','r','r','r'])
        tb.set_cols_dtype(['t','t','f','f','f','f','f','f','f','i','f','f'])
        tb.set_cols_width([8,12,10,10,10,10,10,10,10,10,12,12])
        tb.header(list(dfr))
        #tb.add_rows(dfr.values,header=False)
        #这里改成逐行遍历再添加，用于增加判断涨跌幅度并发送短信提醒
        for dfr_row in dfr.itertuples():
            #print(dfr)
            zdf=getattr(dfr_row, '涨跌')
            name=getattr(dfr_row, 'name')
            if(zdf>7.000):
                name='***涨幅超过7%：'+name
            elif(zdf>5.000):
                name='**涨幅超过5%：'+name
            elif(zdf>3.000):
                name='涨幅超过3%：'+name
            tb.add_row([getattr(dfr_row,'code'),name,getattr(dfr_row, 'open'),getattr(dfr_row, 'pre_close'),getattr(dfr_row, 'price'),getattr(dfr_row, 'high'),getattr(dfr_row, 'low'),zdf,getattr(dfr_row, '持仓价'),getattr(dfr_row, '持股数'),getattr(dfr_row, '当日盈亏'),getattr(dfr_row, '总盈亏')])
            #print(getattr(dfr_row,'code'),getattr(dfr_row, 'name'),getattr(dfr_row, 'open'),getattr(dfr_row, 'pre_close'),getattr(dfr_row, 'price'),getattr(dfr_row, 'high'),getattr(dfr_row, 'low'),getattr(dfr_row, '涨跌'),getattr(dfr_row, '持仓价'),getattr(dfr_row, '持股数'),getattr(dfr_row, '当日盈亏'),getattr(dfr_row, '总盈亏'))
        print(tb.draw()) 
        print('当日总盈亏 %.2f,总盈亏 %.2f' %(total_twl,total_wl))
        total_twl=0
        total_wl=0
        time.sleep(1)
    
if __name__ == '__main__':
    #with open('monitor_code.txt') as f:
    #    codes = f.read().splitlines()
    df=pd.read_csv('hold_stock.csv',dtype={'code':str,'hold_price':float,'hold_cnt':int})
    codes=df['code'].tolist()
    hprice=df['hold_price']
    hcnt=df['hold_cnt']
    #print(codes)
    #print(hprice)
    #print(hcnt)
    #print(type(codes))
    #coeds=pd.read_csv('hold_stock.csv',usecols=[0])
    #print(codes)
    show_price(codes,df)
