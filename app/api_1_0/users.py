#/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import api
from ..models import User
from flask import jsonify

@api.route('/user/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/user/<int:id>/posts/')
def get_user_post(id):
    user = User.query.get_or_404(id)
    posts = user.article
    return jsonify({
        'posts': [post.to_json() for post in posts]
    })

