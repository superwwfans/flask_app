#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 
# ---------------------------------------------------------
"""
    用户登录验证，注册验证
"""
import re
from functools import wraps
import traceback
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from flask import session, redirect, url_for, g

from create_app import rd as conn
from create_app import db
from utils.captcha.captcha import create_captcha
from model.user_models import User


def login_required(func):
    """ 验证用户是否登录
    登录的继续访问视图, 没有登录重定向到登录页面
    :param func: 被装饰视图函数
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.current_user:
            return func(*args, **kwargs)
        return redirect(url_for('user.login'))
    return wrapper


def get_current_user():
    """ 获取当前登录用户
    :return: 返回用户对象
    """
    try:
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user
        return False
    except SQLAlchemyError:
        print('获取当前用户异常', traceback.format_exc())
        return False


def create_captcha_img(pre_code, code):
    """ 创建图形验证码， 保存到redis中
    :param pre_code: 上一次提交的时间戳
    :param code: 本次提交的时间戳
    :return:
    """
    if pre_code:
        conn.delete('captcha:%s' % pre_code)
    text, img = create_captcha()
    conn.setex('captcha:%s' % code, text.lower(), 60)
    return img


def auth_captcha(captcha_code, code):
    """ 验证图形验证码
    :param captcha_code: 输入的图形验证码
    :param code: 本次提交的时间戳
    :return:
    """
    print('auth_captcha:', captcha_code, conn.get("captcha:%s" % code))
    return False if conn.get("captcha:%s" % code) != captcha_code.lower() else True


def auth_register_libs(email, username, password, password1, verify_code, timestamp):
    """ 注册
    :param email: 邮箱
    :param username: 用户名
    :param password: 密码
    :param password1: 确认密码
    :param verify_code: 图形验证码
    :param timestamp: 本次提交时间戳
    :return:
    """
    regex = re.compile(r'[^\._][\w\._-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$')
    if not (email and regex.match(email)):
        return {"status": False, "msg": "邮箱不能为空或者格式不正确!"}

    if User.by_emial(email):
        return {"status": False, "msg": "邮箱已被注册!"}

    if not 3 < len(username) < 32:
        return {"status": False, "msg": "用户名长度大于3小于32!"}

    if not (len(password1) > 5 and len(password) > 5):
        return {"status": False, "msg": "密码至少6位!"}

    if not (password1 == password):
        return {"status": False, "msg": "两次密码不对应!"}

    if not auth_captcha(verify_code, timestamp):
        return {"status": False, "msg": "验证码不正确!"}

    try:
        user = User()
        user.username = username
        user.password = password
        user.email = email
        user.create_time = datetime.now()
        db.session.add(user)
        db.session.commit()
        return {"status": True, "msg": "注册成功!"}
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return {"status": False, "msg": "内部异常!"}


def auth_login_libs(email, password,  verify_code, timestamp, remember_me):
    """登录验证
    :param email:
    :param password:
    :param verify_code:
    :param timestamp:
    :param remember_me:
    :return:
    """
    regex = re.compile(r'[^\._][\w\._-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$')
    if not (email and regex.match(email)):
        return {"status": False, "msg": "邮箱不能为空或者格式不正确!"}

    user = User.by_emial(email)
    if not user:
        return {"status": False, "msg": "邮箱未注册!"}

    if not user.auth_password(password):
        return {"status": False, "msg": "密码不正确!"}

    if not auth_captcha(verify_code, timestamp):
        return {"status": False, "msg": "验证码不正确!"}
    try:
        user.login_num += 1
        user.last_login_time = datetime.now()
        session['user_id'] = user.id
        if remember_me:
            session.permanent = True
        else:
            session.permanent = False
        db.session.add(user)
        db.session.commit()
        return {"status": True, "msg": "登录成功!"}
    except (AttributeError, SQLAlchemyError) as e:
        db.session.rollback()
        return {"status": False, "msg": "内部异常!"}