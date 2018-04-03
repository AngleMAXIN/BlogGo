# /usr/bin/env python3
# -*- coding: utf-8 -*- 

from flask import Flask, render_template, redirect, request, session, url_for, flash
from exts import db
from decorators import login_required
from models import Article, User, Comment, Tag
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])
config['development'].init_app(app)
db.init_app(app)


@app.route('/')
def index():
    context = {

        'articles': Article.query.order_by('-create_time').all()
    }

    return render_template('index.html', **context)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print("---------",password1,password2)
        user = User.query.filter(User.email == email).first()
        if user:
            flash("邮箱已被注册！")
            return redirect(url_for('register'))
        else:
            if password2 != password1:
                flash("前后密码不一致，请重新输入！")
                return redirect(url_for('register'))
            else:
                new_user = User(username=username, email=email, password=password1)

                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        input_text = request.form.get('input_text')
        password = request.form.get('password')
        user_name = User.query.filter(User.email == input_text, password == password).first()
        user_email = User.query.filter(User.username == input_text, password == password).first()
        # if user_email or user_name:
        if user_name:
            session['user_name'] = user_name.username
            session.permanent = True
            return redirect(url_for('index'))
        elif user_email:
            session['user_name'] = user_email.username
            session.permanent = True
            return redirect(url_for('index'))
        else:
            flash("输入信息有误，请重新检查输入")
            return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.context_processor
def username_add_global():
    username = session.get('user_name')
    print(username)
    if username:
        return dict(logined_name=username)
    return dict()


@app.route('/single/<art_id>/')
def single(art_id):
    context = {'article': Article.query.filter(Article.id == art_id).first()}
    return render_template('single.html', **context)


@app.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    comment_content = request.form.get('message')
    if comment_content:
        article_id = request.form.get('article_id')
        article = Article.query.filter(Article.id == article_id).first()
        email = request.form.get('email')
        username = request.form.get('name')
        comment = Comment(content=comment_content, articles=article, author=username, email=email)
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
@login_required
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
    author = User.query.filter(User.id == user_id).first()

    return render_template('user.html', articles=author.article)


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
