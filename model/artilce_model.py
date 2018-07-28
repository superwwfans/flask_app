#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    关于文章的模型类
"""
from uuid import uuid4
from datetime import datetime

from jieba.analyse.analyzer import ChineseAnalyzer

from extra import db
from libs.search_libs.searchmixin import SearchableMixin


class UserLikeArticle(db.Model):
    """点赞表"""
    __tablename__ = 'article_user_like'

    ip_id = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article_article.id'), nullable=False, primary_key=True)


class Comment(db.Model):
    """一级评论表"""
    __tablename__ = 'article_comment'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    # 与文章表建立外键关系
    article_id = db.Column(db.Integer, db.ForeignKey('article_article.id', ondelete="CASCADE"))
    # 与用户表建立外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class ArticleToTag(db.Model):
    """标签与文章关系表"""
    __tablename__ = 'article_to_tag'
    article_id = db.Column(db.Integer, db.ForeignKey('article_article.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('article_tag.id'), primary_key=True)


class Article(SearchableMixin, db.Model):
    """文章表"""
    __tablename__ = 'article_article'
    __searchable__ = ['title', 'content']
    __analyzer__ = ChineseAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    title = db.Column(db.String(50))
    describe = db.Column(db.Text)
    read_num = db.Column(db.Integer, default=0)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)

    image_path = db.Column(db.String(100),)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # 与分类建立外键关系
    category_id = db.Column(db.Integer, db.ForeignKey('article_category.id'))

    # 建立orm查询关系,文章表与评论表的一对多关系
    comments = db.relationship('Comment', backref='article', passive_deletes=True, order_by=-Comment.create_time)

    # 建立orm查询关系,标签表与文章表的多对多关系
    tags = db.relationship('Tag', secondary=ArticleToTag.__table__)

    ips = db.relationship('Record', secondary=UserLikeArticle.__table__)

# db.event.listen(db.session, 'before_commit', Article.before_commit)
# db.event.listen(db.session, 'after_commit', Article.after_commit)


class Category(db.Model):
    """分类表"""
    __tablename__ = 'article_category'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True,  default=lambda: str(uuid4()))
    name = db.Column(db.String(50), unique=True, )
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)

    # 建立orm查询关系,分类表与文章表的一对多关系
    articles = db.relationship('Article', backref='category')


class Tag(db.Model):
    """标签表"""
    __tablename__ = 'article_tag'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True,  default=lambda: str(uuid4()))
    name = db.Column(db.String(50), unique=True, )
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)

    # 建立orm查询关系,标签表与文章表的多对多关系
    articles = db.relationship('Article', secondary=ArticleToTag.__table__)


class Record(db.Model):
    """记录表"""
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(20), nullable=False, unique=True)

    ips = db.relationship('Article', secondary=UserLikeArticle.__table__)