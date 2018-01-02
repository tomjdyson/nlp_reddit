import joblib
import pandas as pd
import nltk
import numpy as np
import scipy.sparse as sp
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.utils import to_unicode
from sklearn.base import BaseEstimator, TransformerMixin
import operator

def custom_transformer(tokens):
    return tokens


class TaggedLineDocument(object):

    def __init__(self, corpus, tokenizer=nltk.RegexpTokenizer(r'(?u)\b(?:\d+?(?:[\.\-/_:,]\d+)*|\w\w+)\b')):
        self.corpus = corpus
        self.tokenizer = tokenizer
        self.transformer = custom_transformer
        self.documents = None

    def __iter__(self):
        """Iterate through the lines in the source."""
        if self.documents is None:
            documents = []
            self.corpus = self.corpus.reset_index()
            for index, row in self.corpus.iterrows():
                tokens = self.tokenizer.tokenize(to_unicode(row['body']))
                documents.append(TaggedDocument(self.transformer(tokens), [index, row['stock'], row['doc_tag']]))
            self.documents = documents

        return self.documents.__iter__()

    def shuffle(self):
        if self.documents is None:
            raise ValueError

        np.random.shuffle(self.documents)
        return self.documents

    def reorder(self):
        self.documents = sorted(self.documents, key=lambda x: x.tags[0])

class DocumentTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X, copy=True):
        return TaggedLineDocument(X)

class Doc2VecTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, size=300, window=8, min_count=5, sample=1e-3, negative=5, epochs=20):
        self.size = size
        self.window = window
        self.min_count = min_count
        self.sample = sample
        self.negative = negative
        self.epochs = epochs
        self._model = None

    def fit(self, X, y=None):
        X = DocumentTransformer().transform(X)
        model = Doc2Vec(X, size=self.size, window=self.window, min_count=self.min_count, sample=self.sample, negative=self.negative)

        try:
            for epoch in range(self.epochs):
                print('Epoch: {}'.format(epoch))
                model.train(X.shuffle(), total_examples=model.corpus_count, epochs= 1)

            self._model = model
            return self
        finally:
            X.reorder()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y)
        return self._model.docvecs

    def transform(self, X, copy=True):
        assert self._model is not None, 'model is not fitted'
        print('transform')

        X = DocumentTransformer().transform(X)
        return np.asmatrix(np.array([self._model.infer_vector(document.words) for document in X]))

stock_list = joblib.load('stock_comment_list.pkl')

stock_df = pd.DataFrame(stock_list)

def str_n_cat(x):
    str_x = str(x['date'])
    cat_x = str_x[0:7]
    con_x = cat_x + '-' + x['stock']
    return con_x

stock_df['doc_tag'] = stock_df.apply(str_n_cat, axis=1)
stock_df.to_csv('stock_df.csv')


# tokenizer = nltk.RegexpTokenizer(r'(?u)\b(?:\d+?(?:[\.\-/_:,]\d+)*|\w\w+)\b')
# documents = []
#
# for index, row in stock_df.iterrows():
#     tokens = tokenizer.tokenize(to_unicode(row['body']))
#     documents.append(TaggedDocument(custom_transformer(tokens), [index, row['stock'], row['doc_tag']]))

ah = Doc2VecTransformer(epochs=100).fit_transform(stock_df)
joblib.dump(ah, 'doc2vecmodel.pkl')



    # tagged_docs = DocumentTransformer().transform(stock_df[['body', 'doc_tag', 'stock']])
#
# print(tagged_docs)


# print(stock_df.head())

# stock_df['date_str'] = str(stock_df['date'])
# print(stock_df['date_str'][0:7])