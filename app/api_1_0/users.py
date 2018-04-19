#/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import api
from ..models import User, Article
from flask import jsonify, request, current_app, url_for

@api.route('/user/<int:id>')
def get_user():
    user = User.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/user/<int:id>/post/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page',1,type=int)
    pagination = user.a