#/usr/bin/env python3
# -*- coding: utf-8 -*-
#/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(config['development'])
config['development'].init_app(app)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about/')
def about():
    return render_template('index.html')
@app.route('/contact/')
def contact():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()