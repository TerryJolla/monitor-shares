import pandas as pd
import akshare as ak
import requests
import datetime
from datetime import timedelta
import time
from emailsend import emailpush
from localmode import ask_data



def ask_symbol():
    entering = True
    while entering:
        s = input('您想看的股票代码是： ')
        if s != '':
            return s
        else:
            entering = False


stock_symbol = ask_symbol()

symbol = stock_symbol[2:]

sina_finance_url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={}&scale=5&ma=5&datalen=2'.format(stock_symbol)
daily_k_chart_url = 'http://image.sinajs.cn/newchart/daily/n/{}.gif'.format(stock_symbol)
min_k_chart_url = 'http://image.sinajs.cn/newchart/min/n/{}.gif'.format(stock_symbol)

stock_data = requests.get(sina_finance_url).json()  # 新浪每5分钟数据
daily_k_chart = requests.get(daily_k_chart_url)  # 日K图
min_k_chart = requests.get(min_k_chart_url)  # 分时图

now_time = datetime.datetime.now()
standard_time = now_time.strftime('%H:%M:%S')
standard_date = now_time.strftime('%Y%m%d')

five_days_ago = (now_time + timedelta(days=-5)).strftime('%Y%m%d')
yesterday = (now_time + timedelta(days=-1)).strftime('%Y%m%d')
# print('请求发送时间：{}'.format(standard_time))

stock_zh_a_tick_tx_js_df = ak.stock_zh_a_tick_tx_js(code=stock_symbol)  # 获取当日每笔交易情况
recent_five_days_data = ak.stock_zh_a_hist(symbol=symbol, start_date=five_days_ago, end_date=yesterday, adjust='qfq')
today_data = ak.stock_zh_a_hist(symbol=symbol, start_date=standard_date, adjust='qfq')
live_data = ak.stock_zh_a_spot_em().query('代码 == "{}"'.format(symbol))


if __name__ == '__main__':
    print(live_data)


# 执行邮件推送
# emailpush(addr=['1005760706@qq.com', 'jiarui.xing@outlook.com', 'wisdomterry1998@hotmail.com'], text='多收件人带附件测试', attchfile1='daily_k.jpg', attchfile2='min_k.jpg', )

ask_data()