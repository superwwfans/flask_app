#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    增加权限,增加角色
"""
from extra import db
from model.user_models import User
from model.permission_model import Role, Permission, Handler, Menu


def permission_manage_libs():
    """
    query all info
    :return:
    """
    roles = Role.query.all()
    permissions = Permission.query.all()
    users = User.query.all()
    menus = Menu.query.all()
    handlers = Handler.query.all()
    return roles, permissions, users, menus, handlers


def permission_add_role(name):
    """
    add role
    :param name:
    :return:
    """
    if name:
        try:
            role = Role()
            role.name = name
            db.session.add(role)
            db.session.commit()
            return {"status": True, "msg": "add role success"}
        except Exception:
            db.session.rollback()
            return {"status": False, "msg": "add role fail"}
    return {"status": False, "msg": "need role name"}


def permission_add_permission(name, per_code):
    """
    add permission
    :param name: permission name class:str
    :param per_code: permission code class:str
    :return:
    """
    if name and per_code:
        try:
            permission = Permission()
            permission.name = name
            permission.strcode = per_code
            db.session.add(permission)
            db.session.commit()
            return {"status": True, "msg": "add permission success"}
        except Exception:
            return {"status": False, "msg": "add permission success"}

    return {"status": False, "msg": "need permission name adn permission code  "}


def permission_user_add_role(userid, roleid):
    user = User.query.filter_by(id=userid).first()
    role = Role.query.filter_by(id=roleid).first()
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()


def permission_role_add_permission(roleid, permissionid):
    permission = Permission.query.filter_by(id=permissionid).first()
    role = Role.query.filter_by(id=roleid).first()
    permission.roles.append(role)
    db.session.add(permission)
    db.session.commit()


def permission_add_menu(name, permissionid):
    permission = Permission.query.filter_by(id=permissionid).first()
    menu = Menu()
    menu.name = name
    menu.permission = permission
    db.session.add(menu)
    db.session.commit()


def permission_add_handler(name, permissionid):
    permission = Permission.query.filter_by(id=permissionid).first()
    handler = Handler()
    handler.name = name
    handler.permission = permission
    db.session.add(handler)
    db.session.commit()
