#/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flaskext.markdown import Markdown
from flask_cache import Cache
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
cache = Cache()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    cache.init_app(app)
    Markdown(app)
    from .main import main as main_bluprint
    app.register_blueprint(main_bluprint)
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint)

    return app