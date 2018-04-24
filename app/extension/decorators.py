#/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps

from flask import session, redirect, url_for
from app import cache
from app.models import User, Article, Tag
from ..main import main

class ValidationError(ValueError):
    pass

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if session.get('logined_id'):

            return func(*args, **kwargs)

        else:

            return redirect(url_for('main.login'))

    return wrapper

@cache.cached(timeout=7200, key_prefix='author_list')
@main.context_processor
def author_list():
    return dict(author_list=User.query.all())

@cache.cached(timeout=7200, key_prefix='articles_list')
@main.context_processor
def articles_list():
    def get_art():
        return Article.query.all()[:5]
    return dict(articles_list=get_art)

@cache.cached(timeout=7200, key_prefix='tags_list')
@main.context_processor
def tags_list():
    return dict(tags_list=Tag.query.all())