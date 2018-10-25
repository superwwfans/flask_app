#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 关于博客主页显示库文件
# ---------------------------------------------------------
import traceback

from flask import g
from sqlalchemy.exc import SQLAlchemyError

from model.artilce_model import Article, Comment, Category, Tag, Record
from model.flink_models import Flink
from create_app import db
from send_email_task import send_email

model_dict = {
    "Article": Article

}


def get_base_info():
    """
    获取基本信息
    :return:
    """
    hot_articles = Article.query.order_by(Article.read_num.desc())[:5]
    new_comments = Comment.query.order_by(Comment.create_time.desc())[:5]
    friend_links = Flink.query.all()
    categories = Category.query.all()
    tags = Tag.query.all()
    context = {
        "hot_articles": hot_articles,
        "new_comments": new_comments,
        "flinks": friend_links,
        "categories": categories,
        "tags": tags,
    }
    return context


def _get_pagination(class_name, page):
    """
    获取分页
    :param class_name: 模型类
    :param page: 页数
    :return:
    """
    try:
        pagination = class_name.query.order_by(class_name.create_time.desc()).\
                                paginate(page, per_page=10, error_out=False)
        items = pagination.items
        return pagination, items
    except SQLAlchemyError:
        print('分页查询异常', traceback.format_exc())


def article_list_libs(page):
    """
    获取文章分页列表
    :param page:
    :return:
    """
    pagination, articles = _get_pagination(Article, page)
    context = {
        "pagination": pagination,
        "articles": articles,
        "records_count": Article.query.count()
    }
    return context



def get_detail_libs(article_id):
    """
    获取文章详情页
    :param article_id:
    :return:
    """
    if article_id:
        article = Article.query.filter_by(id=article_id).first()
        if article:
            tags = article.tags
            comments = article.comments
            article.read_num += 1
            db.session.add(article)
            db.session.commit()
            context = {
                "post": article,
                "tags": tags,
                "comments": comments,
                       }
            return context
    context = {}
    return context


def add_comment_libs(article_id, comment_content):
    """
    添加评论
    :param article_id:
    :param comment_content:
    :return:
    """
    if article_id and comment_content:
        try:
            comment = Comment()
            comment.user_id = g.current_user.id
            comment.article_id = article_id
            comment.content = comment_content.strip('')
            db.session.add(comment)
            db.session.commit()
            send_email.delay(title='有人评论了你的文章', content=comment.content)
            return {"status": True, "msg": "添加评论成功"}
        except (AttributeError, SQLAlchemyError):
            db.session.rollback()
            print('添加评论异常', traceback.format_exc())
            return {"status": False, "msg": "添加评论失败"}
    return {"status": False, "msg": "缺少文章，或评论内容"}


def get_category_articles_libs(category_name):
    """
    获取分类下文章
    :param category_name:
    :return:
    """
    category = Category.query.filter_by(name=category_name).first()

    if category:
        articles_res = category.articles
        articles = articles_res
    else:
        articles = ''
    return articles


def article_add_like_libs(article_id, ip):
    """
    给文章点赞
    :param article_id:
    :param ip:
    :return:
    """
    if article_id is None:
        return {'status': False, 'msg': '缺少文章ID'}
    if ip is None:
        return {'status': False, 'msg': '缺少ip'}
    article = Article.query.filter(Article.id == article_id).first()

    user_ip = Record.query.filter_by(ip=ip).first()
    if user_ip is None:
        user_ip = Record()
        user_ip.ip = ip
    else:
        user_ip = user_ip
    if user_ip in article.ips:
        return {'status': False, 'msg': '您已经点赞了'}
    article.ips.append(user_ip)
    db.session.add(article)

    try:
        db.session.commit()
        return {'status': True, 'msg': '点赞成功'}
    except:
        db.session.rollback()
        print('点赞异常', traceback.format_exc())
        return {'status': False, 'msg': '点赞异常'}