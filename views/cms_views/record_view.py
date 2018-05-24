#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    文档说明
"""
from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, jsonify)
from libs.blog.user_auth_libs import login_required
from libs.cms.record_libs import query_record_libs, deleate_record_libs
from libs.permission.permission_interface_libs.permission_interface_libs import handler_permission

cms_record_blueprint = Blueprint('record', __name__, url_prefix='/admin')


@cms_record_blueprint.before_request
@handler_permission('before_request', 'handler')
def before_request():
    pass


@cms_record_blueprint.route('/record/')
@login_required
def record():
    """ 记录列表
    """
    page = request.args.get('page', 1, type=int)
    context = query_record_libs(page)
    return render_template('cms/loginlog.html', **context)


@cms_record_blueprint.route('/delete/', methods=["POST", "GET"])
def deleate_record():
    """ 删除记录
    """
    record_id = request.form.get("id", None)
    result = deleate_record_libs(record_id)
    if result["status"]:
        return jsonify({"status": 200, "msg": result["msg"]})
    return redirect(url_for('record.record'))