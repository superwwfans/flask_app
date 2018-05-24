#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 用户登录和注册
# ---------------------------------------------------------

from flask import (Blueprint, render_template,
                   redirect, request, url_for,
                   session, jsonify)

from libs.blog.user_auth_libs import (create_captcha_img,
                                      auth_register_libs,
                                      auth_login_libs)


user_auth_blueprint = Blueprint('user', __name__, url_prefix='/user/auth')


@user_auth_blueprint.route('/login/', methods=['POST', "GET"])
def login():
    """
    登录
    :return:
    """
    if request.method == "POST":
        email = request.form.get("email", None)
        password = request.form.get("password", None)
        verify_code = request.form.get("verify", None)
        timestamp = request.form.get("timestamp", None)
        remember_me = request.form.get("remember_me", None)
        result = auth_login_libs(email, password, verify_code, timestamp, remember_me)
        if result["status"]:
            return jsonify({'status': 200, "msg": result["msg"]})
        return jsonify({'status': 400, "msg": result["msg"]})
    return render_template('blog/login.html')


@user_auth_blueprint.route('/login_out/', methods=['POST', "GET"])
def login_out():
    """
    退出登录
    :return:
    """
    session.pop('user_id')
    return redirect(url_for('user.login'))


@user_auth_blueprint.route('/register/', methods=['POST', "GET"])
def register():
    """
    注册
    :return:
    """
    if request.method == "POST":
        email = request.form.get("email", None)
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        password1 = request.form.get("password1", None)
        verify_code = request.form.get("verify", None)
        timestamp = request.form.get("timestamp", None)
        result = auth_register_libs(email, username, password, password1, verify_code, timestamp)
        if result["status"]:
            return jsonify({'status': 200, "msg": result["msg"]})
        return jsonify({'status': 400, "msg": result["msg"]})
    return render_template('blog/register.html')


@user_auth_blueprint.route('/captcha/', methods=['POST', 'GET'])
def captcha():
    """图形验证码,给页面的img标签"""
    pre_code = request.args.get('pre_code', '')
    code = request.args.get('code', '')
    img = create_captcha_img(pre_code, code)
    return img
