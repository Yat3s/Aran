# -*- coding:utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return u'Hello World!/sdasdasdasdasdass松哥是傻逼'

if __name__ == '__main__':
    app.run()
