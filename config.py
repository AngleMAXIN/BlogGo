#/usr/bin/env python3
# -*- coding: utf-8 -*-
#/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))
HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'maxin'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'
    SQLALCHEMY_TRACK_MODIFICATIONS = True



    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """开发时的数据库"""
    DEBUG = True
    DATABASE = 'bloggo_dev_db'
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}?charset=utf8'.format( USERNAME,
                                                                            PASSWORD,
                                                                            HOSTNAME,
                                                                            PORT,
                                                                            DATABASE)

class TestingConfig(Config):
    """测试的数据库"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'test.db')

class ProductionConfig(Config):
    """产品时的数据库"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                             'sqlite:///' + os.path.join(basedir, 'data.db')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
