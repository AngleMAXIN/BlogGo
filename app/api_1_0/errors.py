#/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import api
# from app.extension.decorators import ValidationError
from flask import jsonify


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

# @api.app_errorhandler(403)
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

# @api.app_errorhandler(401)
def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response

# @api.errorhandler(ValidationError)
# def validation_error(e):
#     return bad_request(e.args[0])