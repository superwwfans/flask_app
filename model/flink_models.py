#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 友情链接模型
# ---------------------------------------------------------
from create_app import db


class Flink(db.Model):
    """友情链接表"""
    __tablename__ = 'flinks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(100), nullable=False)
