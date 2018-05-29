#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    用户模型类
"""
import pbkdf2
from uuid import uuid4
import hashlib

from extra import db
from model.permission_model import UserToRole


class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50))
    _password = db.Column('password', db.String(200))
    last_login_time = db.Column(db.DateTime)
    login_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime)
    avatar_hash = db.Column(db.String(32))

    articles = db.relationship('Article', backref='users')

    comments = db.relationship('Comment', backref='users')

    roles = db.relationship("Role", secondary=UserToRole.__table__)

    def _hash_password(self, password):
        return pbkdf2.crypt(password, iterations=0x2537)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self._hash_password(password)

    def auth_password(self, other_password):
        if self._password is not None:
            return self.password == pbkdf2.crypt(other_password, self.password)
        else:
            return False

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @classmethod
    def by_emial(cls, email):
        return cls.query.filter_by(email=email).first()
