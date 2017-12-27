#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__, static_folder='templates', static_url_path='')


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/')
def home():
    return render_template('home.html')

#
# @app.route('/about')
# def about():
#     return render_template('about.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
