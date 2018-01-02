import pandas as pd
import joblib
import operator
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.utils import to_unicode
import numpy as np

def change_avg(x ,columns):
    avg = 0
    col_len = len(columns)
    for change_col in columns:
        change_val = x[change_col]
        if change_val > 0:
            avg += change_val
        else:
            col_len -= 1
            continue
    if col_len == 0:
        col_len = 1
    return avg / col_len


ah = joblib.load('doc2vecmodel.pkl')


stock_df = pd.read_csv('stock_df.csv')
stock_timeseries = pd.read_csv('stock_timeseries.csv')
stock_df = stock_df[pd.notnull(stock_df['doc_tag'])]

classes = stock_df['doc_tag'].drop_duplicates()
predictions = []
sim_list = []
max_sim_prob = -1
similar_dict_list = []
for test_tag in classes:
    similar_dict = {}
    for similar in classes:
        if similar == test_tag:
            continue
        else:
            sim = ah.similarity(test_tag, similar)
            similar_dict[similar] = sim
    sorted_sim_dict = sorted(similar_dict.items(), key =operator.itemgetter(1), reverse=True)
    # sorted_sim_dict = sorted_sim_dict.reverse()
    top_most_sim = {}
    col_act_val = 'act_value'
    top_most_sim[col_act_val] = stock_timeseries.loc[stock_timeseries['doc_tag'] == test_tag, 'open_change_-1'].values[
        0]

    cols_to_avg = []
    for i in range(3):
        col_tag_name = str(i) + '_similar_tag'
        col_sim_name = str(i) + '_similar_sim'
        col_map_vote = str(i) + '_similar_map_vote'
        top_most_sim[col_tag_name] = sorted_sim_dict[i][0]
        top_most_sim[col_map_vote] = stock_timeseries.loc[stock_timeseries['doc_tag'] == sorted_sim_dict[i][0], 'open_change_-3'].values[0]
        top_most_sim[col_sim_name] = sorted_sim_dict[i][1]
        cols_to_avg.append(col_map_vote)

    similar_dict_list.append(top_most_sim)
full = pd.DataFrame(similar_dict_list)
classes = classes.reset_index(drop = True)
full['doc_tag'] = classes
full['avg_change'] = full.apply(change_avg, axis = 1, args=(cols_to_avg,))

# full.to_csv('class_n_sim.csv')


merged_df = pd.merge(left=full, right=stock_timeseries, on='doc_tag')

merged_df['price_pred'] = merged_df['avg_change'] * merged_df['open_avg']

merged_df['error'] = merged_df['price_pred'] - merged_df['open_avg_-1']

merged_df.to_csv('price_pred_df.csv')