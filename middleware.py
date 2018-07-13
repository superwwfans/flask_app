#! usr/bin/env python
# coding=utf-8

"""
处理http error 获取当前用户信息

"""
from flask import render_template, g
from flask_wtf.csrf import CSRFError

from libs.blog.user_auth_libs import get_current_user
from extra import app
from blueprint_list import blueprints


for b in blueprints:
    app.register_blueprint(b)


@app.route('/error')
def error_test():
    a = 1/0
    return a


@app.errorhandler(CSRFError)
def csrf_error(reason):
    return render_template('403.html', reason=reason), 403


@app.errorhandler(404)
def page_no_found(error):
    return render_template('404.html')


@app.errorhandler(500)
def server_errors(error):
    return render_template('500.html')


@app.before_request
def before_request():
    g.current_user = get_current_user()