#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    配置文件
"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    应用配置
    """
    SECRET_KEY = os.urandom(24)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    LOG_TO_STDOUT = False
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "forver22huang@163.com"
    MAIL_PASSWORD = "HXD112301ww"
    ADMINS = ["921261233@qq.com"]

    ELASTICSEARCH_URL = 'http://localhost:9200'

    POSTS_PER_PAGE = 5

    BROKER_URL = "redis://localhost:6379/0"

    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

    CELERY_TASK_SERIALIZER = "json"

    CELERY_RESULT_SERIALIZER = "json"

    CELERY_TASK_EXPIRES = 60 * 60 * 24

    CELRY_ACCEPT_CONTENT = ["json"]

