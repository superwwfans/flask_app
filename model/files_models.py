#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    文件模型类
"""
import hashlib
from datetime import datetime
from ext import db


def hash_data(datas):
    h = hashlib.sha1()
    h.update(datas)
    return h.hexdigest()


class Files(db.Model):
    """ 文件模型类
    """
    __tablename__ = 'files'
    uuid = db.Column(db.String(100), unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime)
    view_num = db.Column(db.Integer, default=0)
    content_length = db.Column(db.Integer)
    content_type = db.Column(db.String(50))
    yun_url = db.Column(db.String(200))
    _file_hash = db.Column(db.String(50), nullable=False, unique=True)
    _locked = db.Column(db.Boolean, default=False, nullable=False)


    @property
    def file_hash(self):
        return self._file_hash

    @file_hash.setter
    def file_hash(self, datas):
        self._file_hash = hash_data(datas)

    @classmethod
    def file_is_existed(cls, other_dates):
        other_dates_hash = hash_data(other_dates)
        return cls.by_hash(other_dates_hash)

    @classmethod
    def by_hash(cls, other_dates_hash):
        return cls.query.filter_by(_file_hash=other_dates_hash).first()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def by_id(cls, files_id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return cls.query.filter_by(filename=name).first()

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value