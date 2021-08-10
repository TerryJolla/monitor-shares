
def ask_data():   # 本地询问模式
    from shares import live_data, stock_zh_a_tick_tx_js_df, recent_five_days_data, daily_k_chart, min_k_chart, \
        today_data
    import datetime

    now_time = datetime.datetime.now()
    standard_time = now_time.strftime('%H:%M:%S')

    a = input('是否要获取交易数据（请输入：YES/NO)： ')
    if a == 'YES':
        if '09:25:00' < standard_time < '09:30:00':
            print('集合竞价数据\n{}'.format(stock_zh_a_tick_tx_js_df))
        elif standard_time < '09:25:00':
            print('近五天的数据\n{}'.format(recent_five_days_data))
        elif '09:30:00' < standard_time < '15:01:00':
            print('截至目前，今天交易数据最后10笔\n')
            print(stock_zh_a_tick_tx_js_df.tail(10))
            with open('daily_k.jpg', 'wb') as code:
                code.write(daily_k_chart.content)
            with open('min_k.jpg', 'wb') as code:
                code.write(min_k_chart.content)
        elif standard_time > '15:01:00':
            print(today_data)
    elif a == 'NO':
        print(live_data)
    else:
        print('请您输入正确的指令')


if __name__ == '__main__':
    ask_data()
