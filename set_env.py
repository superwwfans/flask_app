#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 设置环境变量
# ---------------------------------------------------------
import os


if __name__ == '__main__':
    os.environ['FLASK_ADMIN'] = 'pythoncabin@163.com'
    os.environ['USERNAME'] = 'huang'
    os.environ['PASSWORD'] = 'hxd112301ww'
    os.environ['SECRET_KEY'] = str(os.urandom(24))
    os.environ['DATABASE'] = 'cms_blog'
