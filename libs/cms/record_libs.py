#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 用户登录记录
# ---------------------------------------------------------
from model.artilce_model import Record
from ext import db
from sqlalchemy.exc import SQLAlchemyError
import traceback
from flask import session, request
from random import randint
from datetime import datetime


model_dict = {
    "Record": Record
}


def save_user_record():
    """ 记录用户登录信息
    """
    try:
        record = Record()
        user_id = session.get('user_id', None)
        if user_id:
            record.user_id = user_id
        else:
            record.users.username = '游客{}'.format(randint(10000, 99999))
        record.ip = request.remote_addr
        record.last_login_time = datetime.now()
        db.session.add(record)
        db.session.commit()
    except SQLAlchemyError:
        print('记录用户登录信息', traceback.format_exc())


def _get_pagination(class_name, page):
    """获取分页
    :param class_name: 模型类
    :param page: 页数
    :return:
    """
    try:
        pagination = class_name.query.order_by(class_name.last_login_time.desc()).\
                                paginate(page, per_page=10, error_out=False)
        items = pagination.items
        return pagination, items
    except SQLAlchemyError:
        print('分页查询异常', traceback.format_exc())


def query_record_libs(page):
    """ 获取文章分页列表
    :param page:
    :return:
    """
    pagination, records = _get_pagination(model_dict['Record'], page)
    context = {
        "pagination": pagination,
        "records": records,
        "records_count": Record.query.count()
    }
    return context


def deleate_record_libs(record_id):
    """删除记录
    :param record_id:
    :return:
    """
    if record_id:
        try:
            record = Record.query.filter_by(id=record_id).first()
            if record:
                db.session.delete(record)
                db.session.commit()
                return {"status": True, "msg": "删除成功!"}
            else:
                return {"status": False, "msg": "查询没有结果"}
        except SQLAlchemyError:
            db.session.rollback()
            print('删除记录异常', traceback.format_exc())
            return {"status": False, "msg": "删除记录异常"}
    return {"status": False, "msg": "没有获取到记录ID"}
