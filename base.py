import praw
from praw.models import MoreComments
import datetime
import joblib


class RedditScraper:
    def __init__(self, reddit_instance, subreddit_list):
        """Scrape reddit comments about stocks
            Parameters:
            ----------
            reddit_instance: PrawReddit agent.
                Agent to use for scraping.

            subreddit_list : list of string
                list of subreddits by name that will be searched and sraped.
        """

        self.reddit_instance = reddit_instance
        self.subreddits = self.subreddit_concat(subreddit_list)
        self.stock_list = None

    def subreddit_concat(self, subreddit_list):
        """Concatenate list of subreddits into one long string - how praw uses it.
            Parameters:
            ----------

            subreddit_list : list of string
                list of subreddits by name that will be searched and sraped.

            Returns:
            --------

            string of joined list
        """
        return '+'.join(subreddit_list)

    def retrieve_stock_comments(self, stock_to_search):
        """Retrieve comments about a stock in each subreddit.

            Parameters:
            ----------
            stock_to_search: string.
                string stock that praw will search

            Returns:
            --------
            scraped_comment_list: list of dictionaries
                dictionaries that contain information about a comment that relates to the stock

        """
        scraped_comment_list = []
        # search through all the subreddits for a particular string
        subreddit_instance = self.reddit_instance.subreddit(self.subreddits).search(query=stock_to_search, sort='new')
        multi_stock_list = self.stock_list.copy()
        multi_stock_list.remove(stock_to_search)

        #loop through every submission returned in the search
        for submission in subreddit_instance:
            title = submission.title  # Output: the submission's title
            multi_stock = False
            #look for if people are talking about more than one stock
            if multi_stock_list is not None:
                for new_stock in multi_stock_list:
                    if new_stock in title:
                        multi_stock = True
            #retrieve all the comments in a comment tree, will only have a few without this
            submission.comments.replace_more(limit=0)

            #loop through comments on particular post
            for comment in submission.comments.list():
                if comment.body == '[deleted]':
                    continue
                comment_dict = {}
                comment_dict['title'] = title
                comment_dict['body'] = comment.body
                comment_dict['date'] = datetime.datetime.fromtimestamp(comment.created).date()
                comment_dict['stock'] = stock_to_search
                comment_dict['multi_stock'] = multi_stock
                scraped_comment_list.append(comment_dict)
        return scraped_comment_list

    def retrieve_list_comments(self, stock_list):
        com_list_o_lists = []
        self.stock_list = stock_list
        for stock in stock_list:
            comments = self.retrieve_stock_comments(stock)
            print(stock, ':', len(comments))
            # com_list_o_lists.append(comments)
            com_list_o_lists += comments
        return com_list_o_lists


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
                  # 'X',
                  # 'V',
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
                  # 'F',
                  'WMT',
                  'MCD',
                  'MU',
                  # 'PGNX',
                  'CSCO',
                  'INTC',
                  'NVDA',
                  'HSBC',
                  'FB']

    reddit = praw.Reddit(user_agent='Comment Extraction (by /u/Vengefulsausage1)',
                         client_id='FLEcBnZJ-fEUqg', client_secret="f8cCHFqKQpr1wCFyEpuXr3vIvME")

    subreddit_list = ['stocks', ' investing', ' StockMarket', ' RobinHood', ' Stock_Picks', ' pennystocks',
                      ' portfolios', ' investing_discussion', ' finance', ' investmentclub', ' economics']

    stock_comment_list = RedditScraper(reddit, subreddit_list).retrieve_list_comments(stock_list)
    joblib.dump(stock_comment_list, 'stock_comment_list.pkl')

    print(len(stock_comment_list))
    print(stock_comment_list[13000])
