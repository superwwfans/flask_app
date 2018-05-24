#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    后台应用蓝图
"""
from flask import (Blueprint, render_template,
                   request, redirect, url_for, jsonify)
from libs.blog.user_auth_libs import login_required

from libs.cms.article_libs import (system_info_libs,
                                   add_category_libs,
                                   get_category_libs,
                                   delete_article_libs,
                                   add_article_libs,
                                   get_article_libs,
                                   delete_category_libs,
                                   get_articles_list_libs,
                                   get_comments_list_libs)

from libs.cms.flink_libs import add_flink_libs, get_flinks_list

from libs.permission.permission_interface_libs.permission_interface_libs import handler_permission

cms_blueprint = Blueprint('cms', __name__, url_prefix='/admin')


@cms_blueprint.before_request
@handler_permission('before_request', 'handler')
def before_request():
    pass


@cms_blueprint.context_processor
def system_info():
    context = system_info_libs()
    return context


@cms_blueprint.route('/')
@login_required
def index():
    """ 后台首页
    """
    return render_template('cms/index.html')


@cms_blueprint.route('/article/')
@login_required
def article():
    """ 文章列表
    """
    page = request.args.get('page', 1, type=int)
    context = get_articles_list_libs(page)
    return render_template('cms/article.html', **context)


@cms_blueprint.route('/add_article/', methods=["POST", "GET"])
@login_required
def add_article():
    """ 添加文章
    """
    if request.method == "POST":
        article_id = request.form.get('id', '')
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        describe = request.form.get('describe', '')
        category_id = request.form.get('category', '')
        tags = request.form.get('tags', '')
        file_data = request.files['myfilename']
        result = add_article_libs(article_id, title, content, describe, category_id, tags, file_data)
        if result['status']:
            return redirect(url_for('cms.article'))
        return redirect(url_for('cms.add_article'))
    return render_template('cms/add-article.html')


@cms_blueprint.route('/update_article/', methods=["POST", "GET"])
@login_required
def update_article():
    """ 修改文章
    """
    article_id = request.args.get('id', '')
    article_obj = get_article_libs(article_id)
    return render_template('cms/update-article.html', article=article_obj)


@cms_blueprint.route('/delete_article/', methods=["POST", "GET"])
@login_required
def delete_article():
    """ 删除文章文章
    """
    article_id = request.form.get('id', '')
    result = delete_article_libs(article_id)
    if result['status']:
        return jsonify({'status': 200, "msg": result['msg']})
    return jsonify({'status': 400, "msg": result['msg']})


@cms_blueprint.route('/delete_comment/', methods=["POST", "GET"])
@login_required
def delete_comment():
    """ 删除评论
    """
    pass


@cms_blueprint.route('/comment/')
@login_required
def comment():
    """ 评论列表
    """
    page = request.args.get('page', 1, type=int)
    context = get_comments_list_libs(page=page)
    return render_template('cms/comment.html', **context)


@cms_blueprint.route('/category/', methods=["POST", "GET"])
@login_required
def category():
    """ 分类列表
    """
    return render_template('cms/category.html')


@cms_blueprint.route('/add_category/', methods=["POST", "GET"])
@login_required
def add_category():
    """ 添加分类
    """
    category_id = request.form.get('id', '')

    category_name = request.form.get('name')
    result = add_category_libs(category_id, category_name)
    if result['status']:
        return redirect(url_for('cms.category'))
    return redirect(url_for('cms.category'))


@cms_blueprint.route('/delete_category/', methods=["POST", "GET"])
@login_required
def delete_category():
    """ 删除分类
    """
    category_id = request.form.get('id')
    result = delete_category_libs(category_id)
    if result['status']:
        return jsonify({'status': 200, "msg": result['msg']})
    return jsonify({'status': 400, "msg": result['msg']})


@cms_blueprint.route('/update_category/', methods=["POST", "GET"])
@login_required
def update_category():
    """ 更新分类
    """
    category_id = request.args.get('id', '')
    category_obj = get_category_libs(category_id)
    return render_template('cms/update-category.html', category=category_obj)


@cms_blueprint.route('/friend_link/', methods=["GET", "POST"])
def friend_link_list():
    """ 友情链接 """
    context = get_flinks_list()
    return render_template('cms/flink.html', **context)


@cms_blueprint.route("/add_flink/", methods=["GET", "POST"])
def add_flink():
    """ 增加友情链家 """
    if request.method == "POST":
        name = request.form.get('name', None)
        url = request.form.get("url", None)
        result = add_flink_libs(name, url)
        if result["status"]:
            return redirect(url_for('cms.friend_link_list'))
    return render_template('cms/add-flink.html')
