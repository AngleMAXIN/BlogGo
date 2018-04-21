# /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import current_app, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import Serializer
from app import db

class ValidationError(ValueError):
    pass


class User(db.Model):
    """用户数据模型"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # autoincrement=True自动递增
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'username': self.username,
            'post': url_for('api.get_user_post', id=self.id, _external=True)

        }
        return json_user


    @property
    def passtext(self):
        """如果有读取行为，则返回错误"""
        raise AttributeError('不可以读取当前密码')

    @passtext.setter
    def passtext(self, password_str):
        """计算密码的散列值，并赋给password字段"""
        self.password = generate_password_hash(password_str)

    def verify_password(self, password_str):
        """检测密码是否正确，正确就返回True"""
        return check_password_hash(self.password, password_str)

    def generate_auth_token(self, expiration):
        """使用编码后的用户id
        字段值生成一个签名令牌，还指定了以秒
        为单位的过期时间"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps('id', 'self.id')

    @property
    def is_anonymous(self):
        return False
    @property
    def confirmed(self):
        return True

    @staticmethod
    def verify_auth_token(token):
        """方法接受的参数是一个令牌，
           如果令牌可用就返回对应的用户"""

        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])


def __repr__(self):
    return '<User %s >' % self.username


class Tag(db.Model):
    """标签数据模型"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Tags %s>' % self.content


class Article(db.Model):
    """文章数据模型"""

    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)  # nullable=False不允许出现空值
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tag = db.relationship('Tag', backref=db.backref('tags'))
    author = db.relationship('User', backref=db.backref('article'))


    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True), #external=True是为了生成完整的 URL
            'body':self.content,
            'create_time': self.create_time,
            'auth_id': self.author_id,
            'tag': self.tag,
            'author': url_for('api.get_user', id=self.author_id, _external=True),
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not hava a body')
        return Article(content=body)

    def __repr__(self):
        return '<Article %s >' % self.title


# db.event.listen(Article.content, 'set', Article.on_body_change)

class Comment(db.Model):
    """评论数据模型"""

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary_key=True主键
    content = db.Column(db.String(225), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    author = db.Column(db.String(225), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    email = db.Column(db.String(100), nullable=False)
    articles = db.relationship('Article', backref=db.backref('comments', order_by=id.desc()))  # desc()降序

    def __repr__(self):
        return '<Comment %d >' % self.id
