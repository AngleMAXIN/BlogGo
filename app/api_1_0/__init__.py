#/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api/v1.0')

from . import  posts, users