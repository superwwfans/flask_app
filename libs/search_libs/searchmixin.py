#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 
# ---------------------------------------------------------
from extra import db
from libs.search_libs.search import add_to_index, remove_from_index, query_index


class SearchableMixin:
    """
    """
    @classmethod
    def search(cls, expression):
        """
        搜索
        :param expression: 关键字
        :return:
        """
        ids, total = query_index(cls.__tablename__, expression)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        """
        文章在提交前
        :param session:
        :return:
        """
        session._changes = {
            'add': [obj for obj in session.new if isinstance(obj, cls)],
            'update': [obj for obj in session.dirty if isinstance(obj, cls)],
            'delete': [obj for obj in session.deleted if isinstance(obj, cls)]
        }

    @classmethod
    def after_commit(cls, session):
        """
        :param session:
        :return:
        """
        for obj in session._changes['add']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['update']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['delete']:
            remove_from_index(cls.__tablename, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """
        :return:
        """
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)




