import datetime as dt
import pandas as pd
import pandas_datareader as pdr

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)

# df = pdr.DataReader(['TSLA', 'APPL', 'MSFT'], 'yahoo',start, end )
# print(df)

stock_df = pd.read_csv('stock_df.csv')
# stock_df['date'] = pd.to_datetime(stock_df.date)
first_date = stock_df.sort_values('date')['date'].iloc[0]
last_date = stock_df.sort_values('date')['date'].iloc[(len(stock_df)-3)]

list_o_stock = ['AAPL',
                'MSFT',
                'AMZN',
                'BP',
                'GOOG',
                'IBM',
                'BRK',
                'JNJ',
                'JPM',
                'BAC',
                'NFLX',
                'XOM',
                'CVS',
                'TSLA',
                'DIS',
                'NKE',
                'SNE',
                'PYPL',
                'BAC',
                'GS',
                'GE',
                #'AZN',
                'CHK',
                #'GSK',
                #'TTM',
                #'CCL',
                'X',
                'V',
                #'TXN',
                'BA',
                'WFC',
                'C',
                'VZ',
                'SBUX',
                'UA',
                'DAL',
                'ATVI',
                'LMT',
                'AMD',
                'F',
                'WMT',
                'MCD',
                'MU',
                # 'PGNX',
                'CSCO',
                'INTC',
                'NVDA',
                'HSBC',
                'FB']
upper_list = [k.upper() for k in list_o_stock]

df = pdr.DataReader(upper_list, 'yahoo',first_date, last_date)
open_df = df['Open']
open_df = open_df.reset_index()

def find_month(x):
    str_x = str(x['Date'])
    cat_x = str_x[0:7]
    return cat_x

def month_n_stock(x):
    str_x = str(x['Month'])
    cat_x = str_x + '-' + x['stock']
    return cat_x

def higher_or_lower(x, shift_period):
    col_shift = 'open_avg_' + shift_period
    if x[col_shift]> 1.01 * x['open_avg']:
        higher = 1
    elif x[col_shift]< 0.99 * x['open_avg']:
        higher = -1
    else:
        higher = 0
    return higher


open_df['Month'] = open_df.apply(find_month, axis =1)
month_means = open_df.groupby(by = 'Month').mean()
#month_means = month_means.reset_index()
# print(list(month_means))
df_list = []
for col in list(month_means):
    # for i in [-1, -2]:
    #     new_col = col + '_%s' % i
    #     #print(new_col)
    #     month_means[new_col] = month_means[col].shift(periods=i)


    df = pd.DataFrame({'stock': col,
                       'open_avg' : month_means[col],
                       'open_avg_-1' : month_means[col].shift(periods=-1),
                       'open_change_-1' : month_means[col].shift(periods=-1)/ month_means[col],
                       'open_avg_-2' : month_means[col].shift(periods=-2),
                       'open_change_-2': month_means[col].shift(periods=-2)/ month_means[col],
                       'open_avg_-3' : month_means[col].shift(periods=-3),
                       'open_change_-3': month_means[col].shift(periods=-3)/ month_means[col],

                       })
    df_list.append(df)

stock_t = pd.concat(df_list)

stock_t['open_-1_h/l'] = stock_t.apply(higher_or_lower, axis = 1, args = ('-1',))
stock_t['open_-2_h/l'] = stock_t.apply(higher_or_lower, axis = 1, args = ('-2',))
stock_t['open_-3_h/l'] = stock_t.apply(higher_or_lower, axis = 1, args = ('-3',))
stock_t = stock_t.reset_index()
stock_t['doc_tag'] = stock_t.apply(month_n_stock, axis = 1)

stock_t.to_csv('stock_timeseries.csv')
