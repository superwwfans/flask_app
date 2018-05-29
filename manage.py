#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
    开发管理文件
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from middleware import app
from extra import db    

from model.user_models import User
from model.artilce_model import Article, Tag, Category, Comment
from model.files_models import Files
from model.flink_models import Flink


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.option('-n', '--name', dest='name', help='', default='root')
@manager.option('-p', '--password', dest='password', help='', default='222')
def superuser(name, password):
    admin = User()
    admin.username = name
    admin.password = password
    db.session.add(admin)
    db.session.commit()
    print('超级用户创建成功!!!')

if __name__ == '__main__':
    print(app.url_map)

    manager.run()
