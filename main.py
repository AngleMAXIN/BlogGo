# /usr/bin/env python3
# -*- coding: utf-8 -*- 

from flask import Flask, render_template, redirect, request, session, url_for, flash
from exts import db
from decorators import login_required
from models import Article, User, Comment, Tag
from filter_input import TextData, Testlogin
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
        
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password2 != password1:
            flash("前后密码不一致，请重新输入！")
            return redirect(url_for('register'))

        input_dict = {
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': password1
        }

        test = TextData(input_dict)
        if not test.test_name:
            flash("用户名不合法")
            return redirect(url_for('register'))
        elif not test.test_email:
            flash("邮箱不合法")
            return redirect(url_for('register'))
        user = User.query.filter(User.email == input_dict['email']).first()
        if user:
            flash("邮箱已被注册！")
            return redirect(url_for('register'))
        elif not test.test_password:
            flash("密码不合法")
            return redirect(url_for('register'))
        else:
            new_user = User()
            new_user.username = input_dict['username']
            new_user.email = input_dict['email']
            new_user.passtext = input_dict['password']

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        input_dict = {
            'input_text': request.form.get('input_text'),
            'password' : request.form.get('password')
        }
        test = Testlogin(input_dict)
        if not test.test_input_text:

            user = User.query.filter_by(email = input_dict['input_text']).first()
        else:  

            user = User.query.filter_by(username = input_dict['input_text']).first()

        if user and user.verify_password(input_dict['password']):

            session['logined_id'] = user.id
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
    user_id = session.get('logined_id')
    if user_id:
        username = User.query.filter(User.id == user_id).first()
        if username:
            return dict(logined_name=username)
    return dict()


@app.route('/single/<art_id>/')
def single(art_id):
    context = {'article': Article.query.filter(Article.id == art_id).first()}
    return render_template('single.html', **context)


@app.route('/add_comment/', methods=['POST'])
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
        author_id = session.get('logined_id')
        title = request.form.get('title')
        content = request.form.get('content')
        tags_content = request.form.get('tag')
        article = Article(title=title, content=content)
        tags = Tag(content=tags_content)
        article.author = User.query.filter_by(id = author_id).first()
        db.session.add(tags)
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/search_list/',methods=["GET"])
def search_list():

    keyword = request.args.get('keyword')

    if keyword:
        title_result = Article.query.filter(Article.title.like('%'+keyword+'%')).all()
        content_result = Article.query.filter(Article.content.like('%'+keyword+'%')).all()
        result =  title_result.append(content_result)
        print("title_result",title_result)
        context = {
            'articles': title_result
        }
        return render_template('search.html', **context)

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
    app.run(host='0.0.0.1',port='8080')
