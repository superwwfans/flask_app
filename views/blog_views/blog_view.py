#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    关于博客主页的视图函数
"""
from threading import Lock

from flask import (Blueprint, render_template, send_from_directory,
                   request, redirect, url_for, jsonify, abort)


from libs.blog.blog_libs import article_list_libs, get_detail_libs,\
                                add_comment_libs, get_base_info, get_category_articles_libs, article_add_like_libs

from libs.blog.search_libs import search_libs

blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.context_processor
def context():
    context = get_base_info()
    return context


@blog_blueprint.route('/')
def index():
    """ 博客首页 """
    page = request.args.get('page', None)
    context = article_list_libs(page)
    return render_template('blog/index.html', **context)


@blog_blueprint.route('/article/detail/<article_id>')
def detail(article_id):
    """
    文章详情
    :param article_id: 文章id
    :return:
    """
    article_info_dict = get_detail_libs(article_id)
    if context:
        return render_template('blog/content.html', **article_info_dict)
    else:
        abort(404)


@blog_blueprint.route('/comment/', methods=["POST"])
def add_comment():
    """ 添加评论 """
    article_id = request.form.get('article_id', None)
    comment_content = request.form.get("commentContent", None)
    article_url = url_for('blog.detail', article_id=article_id)
    result = add_comment_libs(article_id, comment_content)
    if result["status"]:
        return redirect(article_url)
    return redirect(article_url)


@blog_blueprint.route('/category/<category_name>', methods=["GET"])
def category(category_name):
    """
    分类列表
    :param category_name:
    :return:
    """
    articles = get_category_articles_libs(category_name)
    if articles:
        return render_template('blog/category_list.html', articles=articles)
    else:
        abort(404)


@blog_blueprint.route('/search/', methods=["POST", "GET"])
def seearch():
    """ 全文搜索 """
    content = request.form.get("content", None)
    search_result_dict = search_libs(content)
    return render_template('blog/search.html', **search_result_dict)


@blog_blueprint.route('/files_look/')
def files_look():
    """ 文件预览 """
    file_uuid = request.args.get('uuid', None)
    file_path = 'upload_files/'
    return send_from_directory(file_path, file_uuid)


@blog_blueprint.route('/add_like/', methods=['POST'])
def add_like():
    """给文章点赞"""
    ip = request.remote_addr
    article_id = request.form.get('article_id', None)
    result = article_add_like_libs(article_id, ip)
    if result['status'] is True:
        return jsonify({'code': 1, 'msg': result['msg']})
    return jsonify({'code': 0, 'msg': result['msg']})


@blog_blueprint.route('/about_me/')
def about_me():
    return render_template('blog/about.html')