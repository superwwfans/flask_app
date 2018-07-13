#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    处理文章, 分类库函数
"""
from datetime import datetime
import traceback

from flask import request, g
from sqlalchemy.exc import SQLAlchemyError

from extra import db
from libs.files_libs.files_libs import files_upload_libs
from model.artilce_model import Article, Category, Comment, Tag, Record
from model.user_models import User


model_dict = {
    "Article": Article,
    "Comment": Comment
}


def system_info_libs():
    """
    获取系统信息
    :return:
    """
    try:
        user_agent = str(request.user_agent)
        context = {
            'current_time': datetime.now(),
            'user_browser': user_agent.split()[-2],
            'user_count': User.query.count(),
            'post_count': Article.query.count(),
            'category_count': Category.query.count(),
            'comment_count': Comment.query.count(),
            'categories': Category.query.all(),
            "records_count": Record.query.count()
        }
        return context

    except SQLAlchemyError:
        print(traceback.format_exc())


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


def get_articles_list_libs(page):
    """
    获取文章分页列表
    :param page:
    :return:
    """
    pagination, articles = _get_pagination(model_dict['Article'], page)
    context = {
        "pagination": pagination,
        "articles": articles
    }
    return context


def get_comments_list_libs(page):
    """
    获取评论分页列表
    :param page:
    :return:
    """
    pagination, comments = _get_pagination(model_dict['Comment'], page)
    context = {
        "pagination": pagination,
        "comments": comments
    }
    return context


def add_article_libs(article_id, title, content, describe, category_id, tags, file_data=None):
    """ 添加文章
    :param article_id:
    :param title:
    :param content:
    :param describe:
    :param category_id:
    :param tags:
    :param file_data:
    :return:
    """
    if not title or not content:
        return {'status': False, 'msg': '标题或者文章内容不能为空'}
    if article_id:
        article = Article.query.filter_by(id=article_id).first()
        num = len(article.tags)
        for i in range(num):
            article.tags.pop()
    else:
        article = Article()
    try:
        article.title = title
        article.content = content
        article.describe = describe

        tag_list = []
        tags_str = tags.split(';')
        for tag_name in tags_str:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag()
                tag.name = tag_name
                tag_list.append(tag)
            else:
                tag_list.append(tag)
        article.tags = tag_list
        article.category_id = category_id
        article.user_id = g.current_user.id
        image_path = files_upload_libs(file_data)
        article.image_path = image_path
        db.session.add(article)
        db.session.commit()
        return {'status': True, 'msg': '文章保存成功'}

    except SQLAlchemyError:
        print('文章保存异常', traceback.format_exc())
        return {'status': False, 'msg': '文章保存异常'}


def get_article_libs(article_id):
    """获取修改文章的
    :param article_id: 文章id
    :return: 返回按id查找到的文章
    """
    try:
        article = Article.query.filter_by(id=article_id).first()
        return article
    except SQLAlchemyError:
        print('查询文章异常', traceback.format_exc())


def add_category_libs(category_id, category_name):
    """ 添加分类
    :param category_id:
    :param category_name:
    :return:
    """
    try:
        if category_id:
            category = Category.query.filter_by(id=category_id).first()
        else:
            category = Category()
        category.name = category_name
        db.session.add(category)
        db.session.commit()
        return {'status': True, 'msg': '添加分类成功!'}

    except SQLAlchemyError:
        db.session.rollback()
        print('添加分类异常', traceback.format_exc())
        return {'status': False, 'msg': '添加分类异常!'}


def get_category_libs(category_id):
    """修改分类获取分类对象
    :param category_id: 分类id
    :return:
    """
    try:
        category = Category.query.filter_by(id=category_id).first()
        return category
    except SQLAlchemyError:
        print('查询分类异常', traceback.format_exc())


def delete_category_libs(category_id):
    """
    删除分类
    :param category_id: 分类id
    :return: 删除按id查找的分类
    """
    try:
        category = Category.query.filter_by(id=category_id).first()
        db.session.delete(category)
        db.session.commit()
        return {'status': True, 'msg': '删除分类成功!'}

    except SQLAlchemyError:
        db.session.rollback()
        print('删除分类异常', traceback.format_exc())
        return {'status': False, 'msg': '删除分类异常!'}


def delete_article_libs(article_id):
    """
    删除文章
    :param article_id:
    :return:
    """
    try:
        article = Article.query.filter_by(id=article_id).first()
        db.session.delete(article)
        db.session.commit()
        return {'status': True, 'msg': '删除文章成功!'}

    except SQLAlchemyError:
        db.session.rollback()
        print('删除分类异常', traceback.format_exc())
        return {'status': False, 'msg': '删除文章异常!'}


def delete_comment_libs(comment_id):
    """
    删除评论
    :param comment_id:
    :return:
    """
    if comment_id:
        try:
            comment = Comment.query.filter_by(id=comment_id).first()
            db.session.delete(comment)
            db.session.commit()
            return {'status': True, 'msg': '删除评论成功!'}
        except:
            db.session.rollback()
            return {'status': False, 'msg': '删除文章失败!'}
    else:
        return {'status': False, 'msg': '删除文章失败!'}


