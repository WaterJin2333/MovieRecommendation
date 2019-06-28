from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yansong561@127.0.0.1:3306/user'
# 'mysql+pymysql://用户名称:密码@localhost:端口/数据库名称'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)




# sql = ''' select film_id,user_name,score from comment; '''
# df2 = pd.read_sql_query(sql, app.config['SQLALCHEMY_DATABASE_URI'])
# df2.rename(columns={'film_id':'film_id', 'user_name':'user_name', 'score':'rating'}, inplace=True)
#
# pd.io.sql.to_sql(df2, 'user_rating', con=app.config['SQLALCHEMY_DATABASE_URI'], index=False, if_exists='append')

# class Filmbaseinfo(db.Model):
#     __tablename__ = 'filmbaseinfo'
#     film_id = db.Column(db.String(20), primary_key=True,)
#     film_name = db.Column(db.String(255), nullable=True)
#     film_director = db.Column(db.String(255), nullable=True)
#     film_screenwriter = db.Column(db.String(255), nullable=True)
#     film_actor = db.Column(db.String(255), nullable=True)
#     film_type = db.Column(db.String(255), nullable=True)
#     film_area = db.Column(db.String(255), nullable=True)
#     film_language = db.Column(db.String(255), nullable=True)
#     film_date = db.Column(db.String(255), nullable=True)
#     film_length = db.Column(db.String(255), nullable=True)
#     film_img = db.Column(db.String(255), nullable=True)
#     film_douban = db.Column(db.String(255), nullable=True)
#     film_content = db.Column(db.String(1000), nullable=True)
#     film_link = db.Column(db.String(255), nullable=True)
#     film_imgpath = db.Column(db.String(255), nullable=True)
#
# class JoinTest(db.Model):
#     __tablename__='test'
#     film_id_test = db.Column(db.String(20),primary_key=True)
#     word = db.Column(db.String(255),nullable=True)


#
# join_test = JoinTest.query.join(Filmbaseinfo,(JoinTest.film_id==Filmbaseinfo.film_id))
# x = join_test.all()
# for y in x:
#     z = y.film_name
#     print(z)
# list1=[]
# film_list = Filmbaseinfo.query.all()
# print(film_list)

# for item in film_list:
#     id = item.film_id
#     list1.append(id)
# print(list1[0:29])

# sql = ''' select filmbaseinfo.film_id, filmbaseinfo.film_name,filmbaseinfo.film_type,filmbaseinfo.film_imgpath,filmbaseinfo.film_content, pre_rating.movie,pre_rating.user_name
#         from filmbaseinfo, pre_rating
#         where filmbaseinfo.film_id = pre_rating.movie; '''
# df = pd.read_sql_query(sql, app.config['SQLALCHEMY_DATABASE_URI'])
# pd.io.sql.to_sql(df, 'cachelist', con=app.config['SQLALCHEMY_DATABASE_URI'], index=False, if_exists='replace')
#写推荐页面的

# abc = JoinTest.query.join(Filmbaseinfo, (Filmbaseinfo.film_id == JoinTest.film_id_test))
# for item in abc:
#     xyz = item.film_id_test
#     print(xyz)
# print(abc)









#
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run()