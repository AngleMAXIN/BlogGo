#/usr/bin/env python3
# -*- coding: utf-8 -*-
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
        'author': User.query.all(),
        'tags' :  Tag.query.all()
    }

    return render_template('index.html', **context)


@app.route('/single/<art_id>/')
def single(art_id):

    article = Article.query.filter(Article.id == art_id).first()
    return render_template('single.html', article=article)

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


if __name__ == '__main__':
    app.run()