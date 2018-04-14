#/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps

from flask import session, redirect, url_for

from app.models import User, Article, Tag
from ..main import main


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if session.get('logined_id'):

            return func(*args, **kwargs)

        else:

            return redirect(url_for('login'))

    return wrapper

@main.context_processor
def author_list():
    return dict(author_list=User.query.all())


@main.context_processor
def articles_list():
    def get_art():
        return Article.query.all()[:5]
    return dict(articles_list=get_art)


@main.context_processor
def tags_list():
    return dict(tags_list=Tag.query.all())