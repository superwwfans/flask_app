#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    文件上传
"""
from flask import (Blueprint, render_template,
                   g, request, redirect, url_for, jsonify, send_from_directory)

from libs.files_libs.files_libs import files_upload_libs

from libs.permission.permission_interface_libs.permission_interface_libs import handler_permission

files_blueprint = Blueprint('files', __name__, url_prefix='/files')


@files_blueprint.before_request
@handler_permission('before_request', 'handler')
def before_request():
    pass


@files_blueprint.route('/files_upload/', methods=["POST", "GET"])
def files_upload():
    """ 文件上传 """
    if request.method == "POST":
        file_data = request.files.getlist("importfile", None)
        result = files_upload_libs(file_data)
        if result is not None:
            return jsonify({"status": 200, "data": result})
        return jsonify({"status": 400, 'msg': 'error'})


