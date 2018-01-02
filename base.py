import praw
from praw.models import MoreComments
import datetime
import joblib

reddit = praw.Reddit(user_agent='Comment Extraction (by /u/Vengefulsausage1)',
                     client_id='FLEcBnZJ-fEUqg', client_secret="f8cCHFqKQpr1wCFyEpuXr3vIvME")

stock = 'chk'


chk_list = []
submissions = 0

def retrieve_comments(reddit_obj, stock_to_search):
    subreddit = reddit_obj.subreddit('stocks+investing+StockMarket+RobinHood+Stock_Picks+pennystocks+portfolios+investing_discussion+finance+investmentclub+economics').search(query=stock_to_search, sort='new')
    chk_list = []
    for submission in subreddit:
        title = submission.title  # Output: the submission's title
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            if comment.body == '[deleted]':
                continue
            comment_dict = {}
            comment_dict['title'] = title
            comment_dict['body'] = comment.body
            comment_dict['date'] = datetime.datetime.fromtimestamp(comment.created).date()
            comment_dict['stock'] = stock_to_search
            chk_list.append(comment_dict)

    return chk_list

def multi_list(reddit_inst, stock_list):
    com_list_o_lists = []
    for stock in stock_list:
        comms = retrieve_comments(reddit_inst, stock)
        print(stock , ':', len(comms))
        com_list_o_lists.append(comms)
    return [item for sublist in com_list_o_lists for item in sublist]


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

stock_list = multi_list(reddit, list_o_stock)
joblib.dump(stock_list, 'stock_comment_list.pkl')

print(len(stock_list))
print(stock_list[13000])