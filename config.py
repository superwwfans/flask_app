#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    动态调用配置文件
"""
import os
from kombu import Queue

basedir = os.path.abspath(os.path.dirname(__file__))

HOSTNAME = '127.0.0.1'  # 主机ip
PORT = '3306'  # 端口
DATABASE = 'cms_blog'  # 数据库名
USERNAME = 'huang'  # mysql用户名
PASSWORD = 'HXD112301ww..'  # mysql用户密码
CHARSET = 'charset=utf8'  # 编码
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?{}'.format(USERNAME, PASSWORD, HOSTNAME,
                                                    PORT, DATABASE, CHARSET)


class Config(object):
    """
    应用配置
    """
    SECRET_KEY = os.urandom(24)

    SQLALCHEMY_DATABASE_URI = DB_URI

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = int(465)
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'forever22huang@163.com'
    MAIL_PASSWORD = 'hxd5683ww'
    ADMINS = ['921261233@qq.com']

    ELASTICSEARCH_URL = 'http://localhost:9200'

    POSTS_PER_PAGE = 5

    BROKER_URL = "redis://localhost:6379/0"

    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

    CELERY_TASK_SERIALIZER = "json"

    CELERY_RESULT_SERIALIZER = "json"

    CELERY_TASK_EXPIRES = 60 * 60 * 24

    CELRY_ACCEPT_CONTENT = ["json"]


