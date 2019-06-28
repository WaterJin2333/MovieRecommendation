from flask import Flask, render_template, flash, redirect, url_for, session, send_from_directory,abort, request, current_app,jsonify
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length,ValidationError,equal_to,email
from flask_wtf.file import  FileField, FileRequired, FileAllowed
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from random import randrange
from flask_bootstrap import Bootstrap
import numpy as np
import pandas as pd
from SVD import superSVD
from CF import CF

import os
import uuid
import sys

app = Flask(__name__)


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'base.db'))
# 'mysql+pymysql://用户名称:密码@localhost:端口/数据库名称'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

app.config['BLUELOG_POST_PER_PAGE'] = 6

# bootstrap = Bootstrap(app)

csrf = CSRFProtect(app)
class Filmbaseinfo(db.Model):
    __tablename__ = 'filmbaseinfo'
    film_id = db.Column(db.String(20), primary_key=True,)
    film_name = db.Column(db.String(255), nullable=True)
    film_director = db.Column(db.String(255), nullable=True)
    film_screenwriter = db.Column(db.String(255), nullable=True)
    film_actor = db.Column(db.String(255), nullable=True)
    film_type = db.Column(db.String(255), nullable=True)
    film_area = db.Column(db.String(255), nullable=True)
    film_language = db.Column(db.String(255), nullable=True)
    film_date = db.Column(db.String(255), nullable=True)
    film_length = db.Column(db.String(255), nullable=True)
    film_img = db.Column(db.String(255), nullable=True)
    film_douban = db.Column(db.String(255), nullable=True)
    film_content = db.Column(db.String(1000), nullable=True)
    film_link = db.Column(db.String(1000), nullable=True)
    video_path=db.Column(db.String(255), nullable=True)
    film_bg_path=db.Column(db.String(255), nullable=True)
    film_imgpath = db.Column(db.String(255), nullable=True)

class Film_top18(db.Model):
    __tablename__ = 'film_top18'
    film_id = db.Column(db.String(20), primary_key=True, )
    film_name = db.Column(db.String(255), nullable=True)
    film_director = db.Column(db.String(255), nullable=True)
    film_screenwriter = db.Column(db.String(255), nullable=True)
    film_actor = db.Column(db.String(255), nullable=True)
    film_type = db.Column(db.String(255), nullable=True)
    film_area = db.Column(db.String(255), nullable=True)
    film_language = db.Column(db.String(255), nullable=True)
    film_date = db.Column(db.String(255), nullable=True)
    film_length = db.Column(db.String(255), nullable=True)
    film_img = db.Column(db.String(255), nullable=True)
    film_douban = db.Column(db.String(255), nullable=True)
    film_content = db.Column(db.String(1000), nullable=True)
    film_link = db.Column(db.String(255), nullable=True)
    film_imgpath = db.Column(db.String(255), nullable=True)

class Comment(db.Model):
    __tablename__='comment'
    film_id = db.Column(db.String(11), primary_key=True)
    film_name = db.Column(db.String(255),nullable=True)
    user_name = db.Column(db.String(255), primary_key=True)
    user_comment = db.Column(db.String(1000),nullable=True)
    time = db.Column(db.String(255),nullable=True)
    like = db.Column(db.String(255),nullable=True)
    score = db.Column(db.String(255),nullable=True)

class Users(db.Model):
    __tablename__='users'
    user_id=db.Column(db.String(20),primary_key=True)
    user_name = db.Column(db.String(255),nullable=True)
    user_password = db.Column(db.String(255), nullable=True)

class JoinTest(db.Model):
    __tablename__='test'
    film_id=db.Column(db.String(20),primary_key=True)
    word = db.Column(db.String(255),nullable=True)

class Cachelist(db.Model):
    __tablename__='cachelist'
    film_id = db.Column(db.String(20), primary_key=True)
    film_name = db.Column(db.String(255), nullable=True)
    film_type = db.Column(db.String(255), nullable=True)
    film_imgpath = db.Column(db.String(255), nullable=True)
    film_content = db.Column(db.String(1000), nullable=True)
    movie = db.Column(db.String(20), primary_key=True)
    user_name = db.Column(db.String(255), primary_key=True)
    rating = db.Column(db.String(255))

class Pre_rating_test(db.Model):
    __tablename__ = 'pre_rating_test'
    user_name=db.Column(db.String(255), primary_key=True)
    movie = db.Column(db.String(1000), nullable=True)


class Pre_rating_cf(db.Model):
    __tablename__ = 'pre_rating_CF'
    user_name=db.Column(db.String(255), primary_key=True)
    movie = db.Column(db.String(1000), nullable=True)










def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

def user_id():
	temp=randrange(0,16,1)
	return str(uuid.uuid1().int)[temp:temp+16]


class LoginForm(FlaskForm):
    username=StringField('用户名',render_kw={'placeholder':'yourname'},validators=[DataRequired(message=r'请输入用户名')])
    password=PasswordField('密码',render_kw={'placeholder':'password'},validators=[DataRequired(),Length(6,24)])
    remeber=BooleanField('记住密码')
    submit=SubmitField('提交')

class RegisterForm(FlaskForm):
    username = StringField('用户名', render_kw={'placeholder': 'Your Name'}, validators=[DataRequired(message=u'请输入用户名')])
    password = PasswordField('密码', render_kw={'placeholder':'Password'},validators=[DataRequired(message=u'请输入密码'), Length(6, 24)])
    confirm = PasswordField('确认密码', render_kw={'placeholder':'Confirm'},validators=[equal_to('password',message='两次密码不同')])
    email = StringField('邮箱', validators=[email(message='邮箱不存在')])
    submit = SubmitField('立即注册')

class Upload_img_From(FlaskForm):
    photo=FileField('选择图片',validators=[FileRequired(),FileAllowed(['jpg','jpge','png'])])

class LoginForm(FlaskForm):
    username=StringField('用户名',render_kw={'placeholder':'yourname'},validators=[DataRequired(message=r'请输入用户名')])
    password=PasswordField('密码',render_kw={'placeholder':'password'},validators=[DataRequired(),Length(6,24)])
    remeber=BooleanField('记住密码')
    submit=SubmitField('提交')

class CommentForm(FlaskForm):
    content = TextAreaField('评论', validators=[DataRequired(), Length(3, 1000)])
    save = SubmitField('保存')
    submit = SubmitField('提交')

class StarForm(FlaskForm):
    rating = StringField('评分',  validators=[DataRequired()])
    submit = SubmitField('提交')

class SubmitForm(FlaskForm):
    rating = StringField()
    submit = SubmitField('评分提交')
    over = SubmitField('评分结束')

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    session['username']=None
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        try:
            record = Users.query.filter_by(user_name=username).first()
            USERS=record.user_name
            right_password=record.user_password
        except BaseException:
            flash('用户名不存在')
            return render_template('film_login.html', loginForm=form)
        else:
            if password==right_password:
                session['username']=username
                return redirect(url_for('index'))
            else:
                flash('密码错误')
    return render_template('login.html',loginForm=form)

#注册
@app.route('/register',methods=['GET','POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if register_form.submit.data:
            username = register_form.username.data
            password = register_form.password.data
            id = user_id()
            user = Users(user_id = id,user_name=username,user_password=password)
            db.session.add(user)
            db.session.commit()
            flash('注册成功 您的账号为%s' % username)
            return redirect(url_for('index'))
    return render_template('register.html',register_form=register_form)





@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', image_path=url_for('static', filename='images/header_bg1.jpg'))

@app.route('/more', methods=['GET', 'POST'])
def get_more():
    name="[\'"+session['username']+"\']"
    film_id=Pre_rating_test.query.filter_by(user_name=name).first().movie
    film_id=eval(film_id)[session['click']]
    film_info=Filmbaseinfo.query.filter_by(film_id=film_id).first()
    session['click'] += 1
    print(film_info)
    print(session['click'])
    return jsonify(film_id=film_info.film_id,film_name=film_info.film_name,film_director=film_info.film_director,film_type=film_info.film_type,film_content=film_info.film_content,
                   film_douban = film_info.film_douban,film_bg_path=film_info.film_bg_path,video_path=film_info.video_path)


@app.route('/back', methods=['GET', 'POST'])
def get_back():
    name="[\'"+session['username']+"\']"
    film_id=Pre_rating_test.query.filter_by(user_name=name).first().movie
    session['click'] -= 1
    film_id=eval(film_id)[session['click']]
    film_info=Filmbaseinfo.query.filter_by(film_id=film_id).first()
    print(film_info)
    print(session['click'])
    return jsonify(film_name=film_info.film_name,film_director=film_info.film_director,film_type=film_info.film_type,film_content=film_info.film_content,
                   film_douban = film_info.film_douban,film_bg_path=film_info.film_bg_path,video_path=film_info.video_path)

@app.before_first_request
def before_first_request():
    session['click'] = 0

@app.route('/recommend', defaults={'page':1},methods=['GET', 'POST'])
@app.route('/recommend/page/<int:page>',methods=['GET', 'POST'])
def recommend(page):
    recommend_form = SubmitForm()
    top18_filmid = Film_top18.query.all()
    pagination = Film_top18.query.paginate(page, per_page=current_app.config['BLUELOG_POST_PER_PAGE'])
    posts = pagination.items
    if recommend_form.validate_on_submit():
        if recommend_form.submit.data:
            user_rating = {}
            user_rating.setdefault('user_name', [])
            user_rating.setdefault('film_id', [])
            user_rating.setdefault('rating',[])
            username = session['username']
            for item in top18_filmid:
                item_id = item.film_id
                stars = request.form.get(item_id)
                if stars != None:
                    user_rating['user_name'].append(username)
                    user_rating['film_id'].append(item_id)
                    user_rating['rating'].append(stars)
            df = pd.DataFrame(user_rating)
            pd.io.sql.to_sql(df, 'user_rating', con=app.config['SQLALCHEMY_DATABASE_URI'], index=False, if_exists='append')
            print('success1')
    # return redirect(render_template())
        if recommend_form.over.data:
            username2 = session['username']
            sql = ''' select film_id,user_name,rating from user_rating; '''
            df3 = pd.read_sql_query(sql, app.config['SQLALCHEMY_DATABASE_URI'])
        # print('abc')
            print('success2')
        # print(df.head(10))
            df_pivot = df3.pivot(index="user_name", columns="film_id", values="rating").fillna(0)
        # print('xyz')
            print(df_pivot.loc[username2, :])
        #print(df_pivot.head(10))
            a = df_pivot.iloc[:, 0].index.tolist().index(username2)
            df_zip = df_pivot.iloc[a:a+100, 0:50]

            print('第一步')
            test1 = superSVD(df_zip)
            print('第二步')
            test1.sgd()
            print('第三步')
        # print(test1.pred(10))

            print(test1.pred())
            # pre_df = pd.DataFrame(test1.pred())
            #
            # print(pre_df)
            # pd.io.sql.to_sql(pre_df, 'pre_rating_test', con=app.config['SQLALCHEMY_DATABASE_URI'], index=False, if_exists='replace')\
            pred=Pre_rating_test(user_name=str(test1.pred()['user_name']),movie=str(test1.pred()['movie']))
            db.session.add(pred)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('recommend.html',form =recommend_form, pagination = pagination, posts = posts)

@app.route('/rating', methods=['GET', 'POST'])
def rating():
    form = StarForm()
    return render_template('rating input.html',starForm = form)

@app.route('/class',methods=['GET', 'POST'])
def Class():
    return render_template('class.html')








@app.route('/detail/<int:film_id>',methods=['GET','POST'])
def detail(film_id):
    filmdetail = Filmbaseinfo.query.get(film_id)
    filmcomments = Comment.query.filter_by(film_id = film_id)

    username3 = session['username']
    sql = ''' select film_id,user_name,rating from user_rating; '''
    df3 = pd.read_sql_query(sql, app.config['SQLALCHEMY_DATABASE_URI'])
    print('success2')
    df_pivot = df3.pivot(index="user_name", columns="film_id", values="rating").fillna(0)
    # print(df_pivot.loc[username3, :])
    a = df_pivot.iloc[:, 0].index.tolist().index(username3)
    df_zip = df_pivot.iloc[a:a + 100, 0:50]

    test2 = CF(df_zip)
    # print(test2.predict())

    pred = Pre_rating_cf(user_name=str(test2.predict()['user_name']), movie=str(test2.predict()['movie']))
    db.session.add(pred)
    db.session.commit()

    name = "[\'" + session['username'] + "\']"
    film_id = Pre_rating_cf.query.filter_by(user_name=name).first().movie
    # film_id = eval(film_id)
    # film_info = Filmbaseinfo.query.filter_by(film_id=film_id).first()
    # print([film_info.film_name, film_info.film_type, film_info.film_director, film_info.film_douban])
    film_dir = {}
    for a in range(1, 7):
        movie_id = eval(film_id)[a]
        film_info = Filmbaseinfo.query.filter_by(film_id=movie_id).first()
        # film_dir.setdefault(a,[]).extend([film_info.film_name, film_info.film_type, film_info.film_director, film_info.film_douban])
        film_dir.setdefault(a, {})
        film_dir[a]['film_name'] = film_info.film_name
        film_dir[a]['film_type'] = film_info.film_type
        film_dir[a]['film_director'] = film_info.film_director
        film_dir[a]['film_douban'] = film_info.film_douban

    return render_template('detail.html',detail=filmdetail,filmcomments = filmcomments, film_dir=film_dir)


@app.route('/more_detail', methods=['GET', 'POST'])
def get_more_detail():
    name = "[\'"+session['username']+"\']"
    film_id = Pre_rating_test.query.filter_by(user_name=name).first().movie
    film_id = eval(film_id)
    results = {}
    for a in range(0, 6):
        movie_id = film_id[session['click1']]
        print(session['click1'])
        film_info=Filmbaseinfo.query.filter_by(film_id=movie_id).first()
        print(film_info)
        results.setdefault(str(a), {})
        results[str(a)]['film_name'] = film_info.film_name
        results[str(a)]['film_type'] = film_info.film_type
        results[str(a)]['film_director'] = film_info.film_director
        results[str(a)]['film_douban'] = film_info.film_douban
        session['click1'] += 1
    print(session['click1'])
    # return jsonify(film_id=film_info.film_id,film_name=film_info.film_name,film_director=film_info.film_director,film_type=film_info.film_type,film_content=film_info.film_content,
    #                film_douban = film_info.film_douban,film_bg_path=film_info.film_bg_path,video_path=film_info.video_path)
    return jsonify(results)


@app.before_first_request
def before_first_request():
    session['click1'] = 0

# @app.route('/personal_recommend',defaults={'page':1})
# @app.route('/personal_recommend/page/<int:page>')
# def PRecommend(page):
#     sql = ''' select filmbaseinfo.film_id, filmbaseinfo.film_name,filmbaseinfo.film_type,filmbaseinfo.film_imgpath,
#                 filmbaseinfo.film_content, pre_rating.movie, pre_rating.user_name
#             from filmbaseinfo, pre_rating
#             where filmbaseinfo.film_id = pre_rating.movie; '''
#     df = pd.read_sql_query(sql, app.config['SQLALCHEMY_DATABASE_URI'])
#     pd.io.sql.to_sql(df, 'cachelist', con=app.config['SQLALCHEMY_DATABASE_URI'], index=False, if_exists='replace')
#     username = session['username']
#     pagination = Cachelist.query.filter_by(user_name = username).order_by(Cachelist.rating.desc()).paginate(page, per_page=current_app.config['BLUELOG_POST_PER_PAGE'])
#     posts = pagination.items
#     return render_template('personal_recommend.html', pagination=pagination, posts=posts)

@app.route('/test',defaults={'page':1})
@app.route('/test/page/<int:page>')
def Test(page):
    pagination = Filmbaseinfo.query.paginate(page, per_page=current_app.config['BLUELOG_POST_PER_PAGE'])
    print(type(pagination))
    posts = pagination.items
    return render_template('test.html',pagination = pagination, posts = posts)



#
# #
# sql = ''' select film_id,user_name,score from comment; '''
# df = pd.read_sql_query(sql, app.config['SQLALCHEMY_DATABASE_URI'])
# # print(df.head(10))
# df_pivot = df.pivot(index="user_name", columns="film_id", values="score").fillna(0)
# #
# # print(df_pivot.head(10))
# #
# test1 = superSVD(df_pivot)
# test1.sgd()
# # # print(test1.pred(10))
# # pre_df = pd.DataFrame(test1.pred(10))
# # pd.io.sql.to_sql(pre_df, 'rating', con=app.config['SQLALCHEMY_DATABASE_URI'], index=False, if_exists='append')
# # #

# join_test = JoinTest.query.join(Filmbaseinfo,JoinTest.film_id==Filmbaseinfo.film_id)
# print(join_test)
# join_sql = ''''''





if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run()