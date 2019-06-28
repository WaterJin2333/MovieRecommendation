import os
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from SVD import superSVD
from collections import Iterable

# Define file directories
# MOVIELENS_DIR = 'D:\Programming\ml-1m'
# USER_DATA_FILE = 'users.dat'
# MOVIE_DATA_FILE = 'movies.dat'
# RATING_DATA_FILE = 'ratings.dat'
#
#
# # Specify User's Age and Occupation Column
# AGES = {1:"Under 18", 18:"18-24", 25:"25-34", 35:"35-44", 45:"45-49", 50:"50-55", 56:"56+"}
# OCCUPATIONS = {0: "other or not specified", 1:"academic/educator", 2:"artist", 3:"clerical/admin",
#                4: "college/grad student", 5:"customer service", 6:"doctor/health care",
#                7: "executive/managerial", 8:"farmer", 9:"homemaker", 10:"K-12 student",
#                11: "lawyer", 12:"programmer", 13:"retired", 14:"sales/marketing",
#                15: "scientist", 16:"self-employed", 17:"technician/engineer",
#                18: "tradesman/craftsman", 19:"unemployed", 20:"writer"}
#
#
# # Define csv files to be saved into
# USERS_CSV_FILE = 'users.csv'
# MOVIES_CSV_FILE = 'movies.csv'
# RATINGS_CSV_FILE = 'ratings.csv'

# Read the Ratings File
# ratings = pd.read_csv(os.path.join(MOVIELENS_DIR, RATING_DATA_FILE),
#                       sep='::',
#                       engine='python',
#                       encoding='latin-1',
#                       names=['user_id', 'movie_id','rating','timestamp'])
#
# ratings_pivot = ratings.pivot(index="user_id", columns="movie_id", values="rating").fillna(0)
# ratings_zip = ratings_pivot.iloc[:200, :100]



# # 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:yansong561@127.0.0.1:3306/user')
# # 创建DBSession类型:
#
sql = ''' select film_id,user_name,score from comment; '''
df = pd.read_sql_query(sql, engine)
#
df_pivot = df.pivot(index="user_name", columns="film_id", values="score").fillna(0)
df_zip = df_pivot.iloc[:50, :50]

test1 = superSVD(df_zip)
test1.sgd()

pre_df = pd.DataFrame(test1.pred(10))
pd.io.sql.to_sql(pre_df, 'rating', con=engine, index=False, if_exists='append')

