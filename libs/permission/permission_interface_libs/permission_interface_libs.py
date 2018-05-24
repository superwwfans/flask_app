#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 验证权限库函数
# ---------------------------------------------------------
"""
    权限验证
"""
import functools

from flask import g, abort

from model.permission_model import Menu, Handler


model = {
    "menu": Menu,
    "handler": Handler,

}


def handler_permission(handler_name, model_types):
    """
     验证视图函数(路由)权限
    :param handler_name: 限制视图函数的名称
    :param model_types: Handler类
    :return: 返回一个装饰器
    """
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if PermissionAuth().permission_auth(g.current_user, handler_name, model_types, model):
                return func(*args, **kwargs)
            else:
                abort(404)
        return wrapper

    return decorator


def menu_permission(menu_name, types):
    """
    验证页面元素权限
    :param menu_name:
    :param types:
    :return:
    """
    if PermissionAuth().permission_auth(g.current_user, menu_name, types, model):
        return True
    return False


class PermissionAuth(object):
    def __init__(self):
        self.user_permissions = set()
        self.obj_permission = ''

    def _get_current_user_permission(self, user):
        """
        获取用户拥有的权限,将用户所有权限对应的权限码放入集合
        :param user:
        :return:
        """
        for role in user.roles:
            for permission in role.permissions:
                self.user_permissions.add(permission.strcode)

    def _get_obj_permission(self, name, model):
        """
        根据 Handler类 和 Menu类 查询对应的权限
        :param name:
        :param model:
        :return:
        """
        obj = model.query.filter_by(name=name).first()
        if not obj:
            return
        permission = obj.permission
        self.obj_permission = permission.strcode if permission else False

    def permission_auth(self, user, name, types, model):
        """
        对用户权限验证
        :param user: 登陆用户
        :param name:
        :param types:
        :param model:
        :return:
        """
        if not user:
            return False
        self._get_current_user_permission(user)
        self._get_obj_permission(name, model[types])

        if not self.user_permissions or not self.obj_permission:
            return False
        if self.obj_permission in self.user_permissions:
            return True
        return False


















