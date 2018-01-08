import praw
from praw.models import MoreComments
import datetime
import joblib


class RedditScraper():
    def __init__(self, reddit_instance, subreddit_list):
        self.reddit_instance = reddit_instance
        self.subreddits = self.subreddit_concat(subreddit_list)

    def subreddit_concat(self, subreddit_list):
        return '+'.join(subreddit_list)

    def retrieve_stock_comments(self, stock_to_search):
        scraped_comment_list = []
        subreddit_instance = self.reddit_instance.subreddit(self.subreddits).search(query=stock_to_search, sort='new')

        for submission in subreddit_instance:
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
                scraped_comment_list.append(comment_dict)

        return scraped_comment_list

    def retrieve_list_comments(self, stock_list):
        com_list_o_lists = []
        for stock in stock_list:
            comments = self.retrieve_stock_comments(stock)
            print(stock, ':', len(comments))
            com_list_o_lists.append(comments)
        return [item for sublist in com_list_o_lists for item in sublist]


if __name__ == '__main__':
    stock_list = ['AAPL',
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
                  # 'AZN',
                  'CHK',
                  # 'GSK',
                  # 'TTM',
                  # 'CCL',
                  'X',
                  'V',
                  # 'TXN',
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

    reddit = praw.Reddit(user_agent='your agent',
                         client_id='your id', client_secret="your secret")

    subreddit_list = ['stocks', ' investing', ' StockMarket', ' RobinHood', ' Stock_Picks', ' pennystocks',
                      ' portfolios', ' investing_discussion', ' finance', ' investmentclub', ' economics']

    stock_comment_list = RedditScraper(reddit, subreddit_list).retrieve_list_comments(stock_list)
    joblib.dump(stock_comment_list, 'stock_comment_list.pkl')

    print(len(stock_list))
    print(stock_list[13000])
