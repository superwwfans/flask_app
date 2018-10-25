#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 权限类
# ---------------------------------------------------------
from create_app import db


class Handler(db.Model):
    """
    视图函数对应权限
    """
    __tablename__ = 'permission_handler'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    p_id = db.Column(db.Integer, db.ForeignKey("permission_permission.id"), unique=True, nullable=False)

    permission = db.relationship("Permission", uselist=False)

    @classmethod
    def by_name(cls, name):
        return cls.query.filter_by(name=name).first()


class Menu(db.Model):
    """
    页面中元素菜单显示对应的权限
    """
    __tablename__ = 'permission_menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    p_id = db.Column(db.Integer, db.ForeignKey("permission_permission.id"),
                     unique=True, nullable=False)

    permission = db.relationship("Permission", uselist=False)

    @classmethod
    def by_name(cls, name):
        return cls.query.filter_by(name=name).first()


class PermissionToRole(db.Model):
    """权限-角色多对多关系表"""
    __tablename__ = 'permission_to_role'
    p_id = db.Column(db.Integer, db.ForeignKey("permission_permission.id"),
                     primary_key=True)
    r_id = db.Column(db.Integer, db.ForeignKey("permission_role.id"),
                     primary_key=True)


class Permission(db.Model):
    """权限表"""
    __tablename__ = 'permission_permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    strcode = db.Column(db.String(50), nullable=False)

    roles = db.relationship("Role", secondary=PermissionToRole.__table__)

    menu = db.relationship("Menu", uselist=False)

    handler = db.relationship("Handler", uselist=False)


class UserToRole(db.Model):
    """用户-角色多对多关系表"""
    __tablename__ = "permission_user_to_role"
    u_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                     primary_key=True)
    r_id = db.Column(db.Integer, db.ForeignKey("permission_role.id"),
                     primary_key=True)


class Role(db.Model):
    """角色表"""
    __tablename__ = 'permission_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    #角色表和用户表多对多查询关系
    users = db.relationship("User", secondary=UserToRole.__table__)

    #角色表和权限表多对多查询关系
    permissions = db.relationship("Permission", secondary=PermissionToRole.__table__)

