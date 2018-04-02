#/usr/bin/env python3
# -*- coding: utf-8 -*- 

from flask import Flask, render_template, redirect, request,session,url_for
from exts import db
from models import Article, User, Comment, Tag
from config import config



app = Flask(__name__)
app.config.from_object(config['development'])
config['development'].init_app(app)
db.init_app(app)





@app.route('/')
def index():

    context = {

        'articles': Article.query.order_by('-create_time').all(),
        # 'author': User.query.all(),
        'tags' :  Tag.query.all()
    }

    return render_template('index.html', **context)


@app.route('/single/<art_id>/')
def single(art_id):
    context = {
    'article': Article.query.filter(Article.id == art_id).first(),
    'articles': Article.query.order_by('-create_time').all(),
    'author': User.query.all(),
    'tags': Tag.query.all()
    }

   
    return render_template('single.html', **context)

@app.route('/add_comment/', methods=['POST'])
def add_comment():

    comment_content = request.form.get('message')
    if comment_content:
        article_id = request.form.get('article_id')
        article = Article.query.filter(Article.id == article_id).first()
        email = request.form.get('email')
        username = request.form.get('name')
        comment = Comment(content=comment_content,articles=article, author=username,email=email)
        comment.articles = article
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('single', art_id=article_id))
    else:
        return "评论不能为空"
@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/post/', methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
        return render_template('post.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        author_name = request.form.get('username')
        tags_content = request.form.get('tag')
        email = request.form.get('email')
        article = Article(title=title, content=content)
        author = User(username=author_name, email=email)
        tags = Tag(content=tags_content)
        article.author = author
        db.session.add(tags)
        db.session.add(article)
        db.session.add(author)
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/user/<user_id>')
def user(user_id):
    # articles = Article.query.filter(author_id = user_id).all()
    author = User.query.filter(User.id == user_id).first()
    print(author.article)
    return render_template('user.html',articles=author.article)

@app.context_processor
def author_list():
    return dict(author_list=User.query.all())

@app.context_processor
def articles_list():
    def get_art():
        return Article.query.all()[:5]
    return dict(articles_list=get_art)

@app.context_processor
def tags_list():
    return dict(tags_list=Tag.query.all())

if __name__ == '__main__':
    app.run()