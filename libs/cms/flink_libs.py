#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 关于友情链接的增删查改
# ---------------------------------------------------------
"""
    处理友情链接库函数
"""
from sqlalchemy.exc import SQLAlchemyError

from globals import db
from model.flink_models import Flink


def add_flink_libs(name, url):
    """添加友情链接
    :param name:
    :param url:
    :return:
    """
    flink = Flink()
    try:
        flink.name = name
        flink.url = url
        db.session.add(flink)
        db.session.commit()
        result = {"status": True, "msg": "添加友情链接成功"}
    except (SQLAlchemyError, AttributeError):
        result = {"status": False, "msg": "添加友情链接异常"}

    return result


def get_flinks_list():
    """
    获取友情链接
    :return:
    """
    friend_links = Flink.query.all()
    flink_count = Flink.query.count()
    context = {
        "flinks": friend_links,
        "flink_count": flink_count
    }
    return context