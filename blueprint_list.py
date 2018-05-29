#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    导入项目中所有蓝图,组成列表
"""
from views.blog_views.user_auth_views import user_auth_blueprint
from views.cms_views.cms_view import cms_blueprint
from views.blog_views.blog_view import blog_blueprint
from views.files_views.file_views import files_blueprint
from views.cms_views.record_view import cms_record_blueprint
from views.cms_views.permission_view import permission_blueprint

blueprints = [cms_blueprint,
              user_auth_blueprint,
              blog_blueprint,
              files_blueprint,
              cms_record_blueprint,
              permission_blueprint
              ]
