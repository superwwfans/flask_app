#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    About Permission module include: add , delete, update
"""

from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify

from libs.permission.permission_interface_libs.permission_interface_libs import handler_permission

from libs.permission.permission_libs import (permission_add_role,
                                             permission_manage_libs,
                                             permission_add_permission,
                                             permission_user_add_role,
                                             permission_role_add_permission,
                                             permission_add_menu,
                                             permission_add_handler

                                             )


permission_blueprint = Blueprint('permission', __name__, url_prefix='/permission')


@permission_blueprint.before_request
@handler_permission('before_request', 'handler')
def before_request():
    pass


@permission_blueprint.route('/manage/', methods=['POST', 'GET'])
def manage():
    """管理台"""
    roles, permissions, users, menus, handlers = permission_manage_libs()
    kw = {
          'roles': roles,
          'permissions': permissions,
          'users': users,
          'menus': menus,
          'handlers': handlers,
    }
    return render_template('cms/permission_list.html', **kw)


@permission_blueprint.route('/add_role/', methods=['POST'])
def add_role():
    """添加角色"""
    name = request.form.get('name', '')
    result = permission_add_role(name)
    if result["status"]:
        return redirect(url_for('permission.manage'))
    return redirect(url_for('permission.manage'))


@permission_blueprint.route('/add_permission/', methods=['POST'])
def add_permission():
    """添加角色"""
    name = request.form.get('name', '')
    per_code = request.form.get('strcode', '')
    result = permission_add_permission(name, per_code)
    if result["status"]:
        return redirect(url_for('permission.manage'))
    return redirect(url_for('permission.manage'))


@permission_blueprint.route('/user_add_role/', methods=['POST'])
def user_add_role():
    """为用户添加角色"""
    userid = request.form.get('userid', '')
    roleid = request.form.get('roleid', '')
    permission_user_add_role(userid, roleid)
    return redirect(url_for('permission.manage'))


@permission_blueprint.route('/role_add_permission/', methods=['POST'])
def role_add_permission():
    """为角色添加权限"""
    permissionid = request.form.get('permissionid', '')
    roleid = request.form.get('roleid', '')
    permission_role_add_permission(roleid, permissionid,)
    return redirect(url_for('permission.manage'))


@permission_blueprint.route('/add_menu/', methods=['POST'])
def add_menu():
    """添加菜单控制"""
    permissionid = request.form.get('permissionid', '')
    name = request.form.get('name', '')
    permission_add_menu(name, permissionid,)
    return redirect(url_for('permission.manage'))


@permission_blueprint.route('/add_handler/', methods=['POST'])
def add_handler():
    """添加handler控制"""
    permissionid = request.form.get('permissionid', '')
    name = request.form.get('name', '')
    permission_add_handler(name, permissionid,)
    return redirect(url_for('permission.manage'))
