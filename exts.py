#/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_sqlalchemy import  SQLAlchemy

import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
