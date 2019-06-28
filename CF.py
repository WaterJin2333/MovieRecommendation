import numpy as np
import pandas as pd
from sklearn import model_selection as cv
from sklearn.metrics import pairwise_distances,mean_squared_error
from math import sqrt
from sqlalchemy import create_engine
import os
# import pymysql
import sys
import operator
# app = Flask(__name__)
# WIN = sys.platform.startswith('win')
# if WIN:
#     prefix = 'sqlite:///'
# else:
#     prefix = 'sqlite:////'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'base.db'))
# # 'mysql+pymysql://用户名称:密码@localhost:端口/数据库名称'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# header = ['user_id','item_id','rating','timestamp']
# df = pd.read_csv('D:\Programming\ml-100k/u.data',sep='\t',names=header)
# MOVIELENS_DIR = 'D:\Programming\ml-1m'
# USER_DATA_FILE = 'users.dat'
# MOVIE_DATA_FILE = 'movies.dat'
# RATING_DATA_FILE = 'ratings.dat'


# Define csv files to be saved into
# USERS_CSV_FILE = 'users.csv'
# MOVIES_CSV_FILE = 'movies.csv'
# RATINGS_CSV_FILE = 'ratings.csv'
#
#
# ratings = pd.read_csv(os.path.join(MOVIELENS_DIR, RATING_DATA_FILE),
#                       sep='::',
#                       engine='python',
#                       encoding='latin-1',
#                       names=['user_id', 'movie_id','rating', 'timestamp'],
#                       )
#
# ratings_pivot = ratings.pivot(index="user_id", columns="movie_id", values="rating").fillna(0)
# sql = ''' select film_id,user_name,rating from user_rating; '''
# df3 = pd.read_sql_query(sql, app.config['SQLALCHEMY_DATABASE_URI'])

class CF(object):
    def __init__(self, dataset):
        self.trainset = dataset
        self.n_users = np.array(self.trainset).shape[0]
        self.n_items = np.array(self.trainset).shape[1]
        # train_data_matrix = np.zeros((self.n_users, self.n_items))

        # for line in self.trainset.itertuples():
        #     train_data_matrix[line[1] - 1, line[2] - 1] = line[3]
        # self.train_data_matrix = train_data_matrix
        self.user_similarity = pairwise_distances(self.trainset, metric='cosine')
        self.item_similarity = pairwise_distances(self.trainset.T, metric='cosine')

# n_users = df.user_id.unique().shape[0]
# n_items = df.item_id.unique().shape[0]
# print ('Number of users = ' + str(n_users) + '| Number of movies = ' + str(n_items) )

# train_data, test_data = cv.train_test_split(df, test_size=0.25)
#     def data(self):
#         train_data_matrix = np.zeros((self.n_users, self.n_items))
#         for line in self.trainset.itertuples():
#             train_data_matrix[line[1]-1, line[2]-1] = line[3]
#
# # test_data_matrix = np.zeros((n_users,n_items))
# # for line in test_data.itertuples():
#     # test_data_matrix[line[1]-1, line[2]-1] = line[3]
#         self.train_data_matrix = train_data_matrix
#         self.user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
#         self.item_similarity = pairwise_distances(train_data_matrix.T,metric='cosine')

    def predict(self, type='user'):
         pred = 0
         if type == 'user':
            mean_user_rating = self.trainset.mean(axis=1)
            ratings_diff = (self.trainset - mean_user_rating[:, np.newaxis])
            pred = mean_user_rating[:, np.newaxis] + self.user_similarity.dot(ratings_diff) / np.array([np.abs(self.user_similarity).sum(axis=1)]).T
         elif type == 'item':
            pred = self.trainset.dot(self.item_similarity) / np.array([np.abs(self.item_similarity).sum(axis=1)])

         # pred_array = np.array(pred)
         prediction = {}
         # prediction.setdefault('user', [])
         # prediction.setdefault('movie', [])
         # prediction.setdefault('rating', [])
         result = {}
         result.setdefault('user_name', [])
         result.setdefault('movie', [])
         uid = self.trainset.iloc[:, 0].index.tolist()[0]
         result['user_name'].append(uid)
         # for uid in range(0, number):
         for iid in self.trainset.loc[uid, :].index.tolist():
             # prediction['user'].append(uid)
             i_index = self.trainset.loc[uid, :].index.tolist().index(iid)
             prediction.setdefault(iid, [])
             prediction[iid].append(pred[0,i_index])

         m = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
         count = 0
         for movie in m:
             result['movie'].append(movie[0])
             count += 1
             if count == 20:
                 break
         return result
# item_prediction = predict(train_data_matrix, item_similarity, type='item')
# user_prediction = predict(train_data_matrix, user_similarity, type='user')
#
# print(item_prediction,user_prediction)

#评估
# def rmse(prediction,ground_truth):
#     prediction = prediction[ground_truth.nonzero()].flatten()
#     ground_truth = ground_truth[ground_truth.nonzero()].flatten()
#
#
# engine = create_engine('mysql+pymysql://root:123@localhost:3306/test')
#
# test2 = CF(ratings_pivot)
# print(test2.predict(10))
# pre_df = pd.DataFrame(test2.predict(10))
# pd.io.sql.to_sql(pre_df, 'rating_cf', con=engine, index=False, if_exists='append')