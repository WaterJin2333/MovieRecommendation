import numpy as np
from numpy import random
import pandas as pd
import operator
import os

# Define file directories
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
#                       names=['user_id', 'movie_id','rating', 'timestamp'])
#
# ratings_pivot = ratings.pivot(index="user_id", columns="movie_id", values="rating").fillna(0)
# ratings_zip = np.array(ratings_pivot)[:200, :100]


class superSVD(object):
    def __init__(self, trainset, n_factors=30, n_steps=10, biased=True, lr_all=0.005, reg_all=0.2, verbose=True):
        self.n_factors = n_factors
        self.n_steps = n_steps
        self.biased = biased
        self.lr_bu = lr_all
        self.lr_bi = lr_all
        self.lr_pu = lr_all
        self.lr_qi = lr_all
        self.reg_bu = reg_all
        self.reg_bi = reg_all
        self.reg_pu = reg_all
        self.reg_qi = reg_all
        self.reg_all = reg_all
        self.verbose = verbose
        self.trainset = trainset
        self.global_mean = np.mean(np.array(self.trainset)[:, :])


    def sgd(self):
        # rng = np.random.RandomState(23455)

        # bu = np.zeros(self.trainset.shape[0])
        bu = np.zeros(self.trainset.iloc[:, 0].size)
        # bi = np.zeros(self.trainset.shape[1])
        bi = np.zeros(self.trainset.columns.size)
        pu = random.randint(-5, 5, size=(self.trainset.iloc[:, 0].size, self.n_factors))
        qi = random.randint(-5, 5, size=(self.trainset.columns.size, self.n_factors))



        for current_step in range(self.n_steps):
            target_f = 0


            for u in range(self.trainset.iloc[:, 0].size):
                # for i in range(self.trainset.shape[1]):
                for i in range(self.trainset.columns.size):
                    dot = 0
                    qi_f2 = 0
                    pu_f2 = 0
                    bu_reg = bu[u]
                    bi_reg = bi[i]
                    for f in range(self.n_factors):
                        dot += qi[i, f] * pu[u, f]
                        qi_f2 += qi[i, f]**2
                        pu_f2 += pu[u, f]**2
                    err = self.trainset.iloc[u, i] - (self.global_mean + bu[u] + bi[i] + dot)
                    target_f += err**2 + self.reg_all*(qi_f2 + pu_f2 + bu_reg**2 + bi_reg**2)

            # update biases
                    if self.biased:
                       bu[u] += self.lr_bu * (err - self.reg_bu * bu[u])
                       bi[i] += self.lr_bi * (err - self.reg_bi * bi[i])

            # update factors
                    for f in range(self.n_factors):
                      puf = pu[u, f]
                      qif = qi[i, f]
                      pu[u,f] += self.lr_pu * (err * qif - self.reg_pu * puf)
                      qi[i,f] += self.lr_qi * (err * puf - self.reg_qi * qif)

            if self.verbose:
                print("Processing step {current_step}" + ":" + str(target_f))


        self.bu = bu
        self.bi = bi
        self.pu = pu
        self.qi = qi

    def pred(self):
        prediction = {}
        result = {}
        result.setdefault('user_name', [])
        result.setdefault('movie', [])
        # prediction.setdefault('user_name', [])
        # prediction.setdefault('movie', [])
        # prediction.setdefault('rating', [])

        # for uid in self.trainset.iloc[:, 0].index.tolist():
            # prediction['user_name'].append(uid)
        uid = self.trainset.iloc[:, 0].index.tolist()[0]
        result['user_name'].append(uid)
        for iid in self.trainset.loc[uid, :].index.tolist():
                # prediction['movie'].append(iid)
                prediction.setdefault(iid, [])
                # a = self.trainset.iloc[0, 0].index.tolist()
                b = self.trainset.loc[uid, :].index.tolist()
                rat = self.global_mean + self.bu[0] + self.bi[b.index(iid)] + self.pu[0] * self.qi[b.index(iid)]
                # prediction['rating'].append(rat[0])
                prediction[iid].append(rat[0])
        m = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        count = 0
        for movie in m:
                result['movie'].append(movie[0])
                count += 1
                if count == 20:
                    break
        return result


# test1 = SVD(ratings_zip)
# test1.sgd()
# test1.pred(0, 1)
