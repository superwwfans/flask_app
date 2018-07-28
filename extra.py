#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    防止循环导入
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from redis import Redis
import logging
from logging.handlers import RotatingFileHandler
from elasticsearch import Elasticsearch
import flask_whooshalchemyplus

from utils.logs.sslsmpthandler import SSLSMTPHandler
from config import Config

csrf = CSRFProtect()
db = SQLAlchemy()
rd = Redis(decode_responses=True)

basedir = os.path.join(os.path.dirname(__file__))


def set_app_log(app_instance):
    """
    设置应用日志记录配置
    :param app_instance:
    :return:
    """
    if not (app_instance.debug and app_instance.testing):
        # 异常发送邮件提醒
        if app_instance.config['MAIL_SERVER']:
            auth = None
            if app_instance.config['MAIL_USERNAME'] or app_instance.config['MAIL_PASSWORD']:
                auth = (app_instance.config['MAIL_USERNAME'],
                        app_instance.config['MAIL_PASSWORD'])
            mail_handler = SSLSMTPHandler(
                mailhost=(app_instance.config['MAIL_SERVER'], app_instance.config['MAIL_PORT']),
                fromaddr=app_instance.config['MAIL_USERNAME'],
                toaddrs=app_instance.config['ADMINS'],
                subject='记录系统异常--博客',
                credentials=auth)
            mail_handler.setFormatter(logging.Formatter('''
                <style>th { text-align: right}</style><table>
                <tr><th>Message type:</th><td>%(levelname)s</td></tr>
                <tr>    <th>Location:</th><td>%(pathname)s:%(lineno)d</td></tr>
                <tr>      <th>Module:</th><td>%(module)s</td></tr>
                <tr>    <th>Function:</th><td>%(funcName)s</td></tr>
                <tr>        <th>Time:</th><td>%(asctime)s</td></tr>
                </table>
                <h2>Message</h2>
                <pre>%(message)s</pre>'''))
            mail_handler.setLevel(logging.ERROR)
            app_instance.logger.addHandler(mail_handler)

        if app_instance.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app_instance.logger.addHandler(stream_handler)

        else:
            # 异常日志写入blog.log文件
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/blog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app_instance.logger.addHandler(file_handler)

        app_instance.logger.setLevel(logging.INFO)
        app_instance.logger.info('blog startup')


def create_app(config_class):
    """
    生成Flask实例的工厂函数
    加载配置文件, 注册蓝图, 注册插件
    :param config_class: 配置文件类
    :return: 返回应用app
    """
    app_instance = Flask(__name__)

    app_instance.config.from_object(config_class)

    db.init_app(app_instance)
    csrf.init_app(app_instance)

    # app_instance.elasticsearch = Elasticsearch([app_instance.config['ELASTICSEARCH_URL']]) \
    #     if app_instance.config['ELASTICSEARCH_URL'] else None
    flask_whooshalchemyplus.init_app(app_instance)
    set_app_log(app_instance)
    return app_instance

app = create_app(Config)
