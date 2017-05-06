import quandl as qd
import numpy as np

qd.ApiConfig.api_key = 'Uk8aW7H-x7bvsqD2wH98'

my_data = qd.get('WIKI/AAPL', start_date='2008-01-01', end_date='2010-01-01')
# print(my_data)


# input: data file (format pandas)
#        interval options (1d, 1w, 1m)
# output: list (column data)
def provider(data_file, column, start, end, interval='1d'):
    global dt_len
    df = data_file
    df = df[column]
    df = df.loc[start:end]
    df = list(df)
    if interval == '1d':
        dt_len = len(df)
        return iter(df)
    elif interval == '1w':
        df_wk = []
        days = 5
        weeks = len(df) // days  # how many weeks
        for week in range(0, weeks):
            temp = df[week*5:(week+1)*5]
            df_wk.append(np.mean(temp))
        dt_len = len(df_wk)
        return iter(df_wk)
    elif interval == '1m':
        df_mth = []
        days = 30
        months = len(df) // days  # how many weeks
        for week in range(0, months):
            temp = df[week*30:(week+1)*30]
            df_mth.append(np.mean(temp))
        dt_len = len(df_mth)
        return iter(df_mth)
    else:
        print('Wrong interval')

my_dt = provider(my_data, 'Close', start='2008-01-05', end='2008-01-30', interval='1w')
for i in range(dt_len):
    print(next(my_dt))

"""有待优化的问题
1. 日期选择， 对于 week 和 month 的选择不是很准确， 现在只是选周期为5或者30 trading days"""
