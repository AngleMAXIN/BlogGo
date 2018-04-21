# /usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, jsonify, g, url_for
from . import api
from app import db
from .authentication import auth, forbidden
from ..models import Article


@api.route('/posts/', methods=['POST'])
def new_post():
    print(request.json)
    article = Article.from_json(request.json)
    article.author = g.current_user
    db.session.add(article)
    db.session.commit()
    return jsonify({article.to_json()}) ,201, {'Location': url_for('api.get_post', id=article.id, _external=True)}


@api.route('/posts/')
@auth.login_required
def get_posts():
    # articles = Article.query.all()
    # return jsonify({'posts': [post.to_json() for post in articles]})
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.paginate(
        page, per_page=3, error_out=False)
    articles = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'post': [article.to_json() for article in articles],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/post/<int:id>', methods=['GET'])
@auth.login_required
def get_post(id):
    artilces = Article.query.get_or_404(id)
    return jsonify(artilces.to_json())

@api.route('/posts/<int:id>', methods=['PUT'])
def edit_post(id):
    article = Article.query.get_or_404(id)
    if g.current_user != article.author:
        return forbidden('Insufficient permissions')
    article.content = request.json.get('body', article.content)
    db.session.add(article)
    return jsonify(article.to_json())