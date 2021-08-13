import pandas as pd
import akshare as ak
import requests
import datetime
from datetime import timedelta
from emailsend import emailpush
from localmode import ask_data


pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 1000)


def ask_symbol():
    entering = True
    while entering:
        s = input('您想看的股票代码是： ')
        if s != '':
            return s
        else:
            entering = False


if __name__ == '__main__':
    stock_symbol = 'sh600089'
    symbol = stock_symbol[2:]
else:
    stock_symbol = ask_symbol()
    symbol = stock_symbol[2:]

sina_finance_url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol' \
                   '={}&scale=5&ma=5&datalen=2'.format(stock_symbol)
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

every_trades = ak.stock_zh_a_tick_tx_js(code=stock_symbol)  # 获取当日每笔交易情况
every_trades_para = ['成交时间', '成交价格', '价格变动', '成交量', '成交金额', '性质']
today_data_para = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
live_data_para = ['序号', '代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', '最高', '最低', '今开', '昨收', '量比', '换手率', '市盈率-动态', '市净率']
recent_five_days_data = ak.stock_zh_a_hist(symbol=symbol, start_date=five_days_ago, end_date=yesterday, adjust='qfq')
today_data = ak.stock_zh_a_hist(symbol=symbol, start_date=standard_date, adjust='qfq')
live_data = ak.stock_zh_a_spot_em().query('代码 == "{}"'.format(symbol))

last_20_trades = every_trades.tail(20)
sell_counts = last_20_trades['性质'].values.tolist().count('卖盘')
neutral_counts = last_20_trades['性质'].values.tolist().count('中性盘')
buy_counts = last_20_trades['性质'].values.tolist().count('买盘')

name = last_20_trades.groupby('性质')['成交价格'].mean().index.tolist()
mean_price = last_20_trades.groupby('性质')['成交价格'].mean().values.tolist()


text = ''


#  策略
if today_data['涨跌幅'].values >= 5:
    text = '请注意，您的股票当前涨幅大于等于5%，当前涨幅为：{}%'.format(today_data['涨跌幅'].values)
elif today_data['涨跌幅'].values <= -5:
    text = '请注意，您的股票当前跌幅大于等于5%，当前跌幅为：{}%'.format(today_data['涨跌幅'].values)

if __name__ == '__main__':
    print(live_data)
    print('- '*15)
    print(today_data)
    print('-'*15)
    print(last_20_trades)
    print('-' * 15)
    print(last_20_trades.groupby('性质')['成交价格'].mean())
    print(last_20_trades.groupby('性质')['成交价格'].mean().index.tolist())
    print(last_20_trades.groupby('性质')['成交价格'].mean().values.tolist())
    print('-' * 15)
    # 执行邮件推送
    # emailpush(addr=['1005760706@qq.com', 'jiarui.xing@outlook.com', 'wisdomterry1998@hotmail.com'], text='多收件人带附件测试', attch_a=daily_k_chart, attch_b=min_k_chart)
