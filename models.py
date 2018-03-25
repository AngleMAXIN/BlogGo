#/usr/bin/env python3
# -*- coding: utf-8 -*-

from main import db
from datetime import datetime


class User(db.Model):

    """用户数据模型"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  #autoincrement=True自动递增
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return '<User %s >' % self.username



class Article(db.Model):

    """文章数据模型"""

    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)    # nullable=False不允许出现空值
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    author = db.relationship('User', backref=db.backref('article'))

    def __repr__(self):
        return '<Article %s >' % self.title


class Comment(db.Model):

    """评论数据模型"""

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #primary_key=True主键
    content = db.Column(db.String(225), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    articles = db.relationship('Article', backref=db.backref('comments', order_by=id.desc())) # desc()降序
    author = db.relationship('User', backref=db.backref('comments'))

    def __repr__(self):
        return '<Comment %d >' % self.id