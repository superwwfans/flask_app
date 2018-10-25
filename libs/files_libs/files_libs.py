#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
"""
文件上传 保存
"""
from uuid import uuid4
import traceback

from flask import g

from create_app import db, basedir
from model.files_models import Files


def _get_file_info(file_data):
    """
    获取文件信息
    :param file_data: 文件数据
    :return: 文件信息的字典数据格式
    """
    file_content = file_data.read()
    file_ext = file_data.filename.split('.')[-1]
    uuid_name = '{}.{}'.format(str(uuid4()), file_ext)
    file_content_type = file_data.content_type

    file_info = {
        'file_content': file_content,
        "file_ext": file_ext,
        "uuid_name": uuid_name,
        "file_content_type": file_content_type
    }

    return file_info


def _is_file_exist(file_content):
    """
    判断文件是否上传过
    :param file_content:
    :return:
    """
    old_files = Files.file_is_existed(file_content)
    return old_files


def _save_to_database(file_name, content_type, file_content, file_uuid_name):
    """
    文件保存到数据库
    :param file_name:
    :param content_type:
    :param file_content:
    :param file_uuid_name:
    :return:
    """
    try:
        files = Files()
        files.filename = file_name
        files.user_id = g.current_user.id
        files.content_length = len(file_content)
        files.content_type = content_type
        files.file_hash = file_content
        files.uuid = file_uuid_name
        db.session.add(files)
        db.session.commit()

        return {"status": True, "msg": "上传成功"}

    except Exception as e:
        db.session.rollback()
        print('文件保存到数据库错误', traceback.format_exc())
        return {"status": False, "msg": "上传异常"}


def _save_file(file_data):
    """
    保存文件本地服务器
    :param file_data: 文件数据
    :return:
    """
    try:
        file_info = _get_file_info(file_data)
        files_upload_path = 'upload_files/{}'.format(file_info['uuid_name'])

        old_file = _is_file_exist(file_info["file_content"])
        if old_file:
            file_path = 'http://www.pythoncabin.cn/files_look?uuid={}'.format(old_file.uuid)
            return {"status": True, "msg": '上传成功()', "data": file_path}

        with open(files_upload_path, 'wb') as f:
            f.write(file_info['file_content'])

        save_rs = _save_to_database(file_data.filename,
                                    file_info["file_content_type"],
                                    file_info["file_content"],
                                    file_info["uuid_name"],
                                    )

        if save_rs['status']:
            file_path = 'http://www.pythoncabin.cn/files_look?uuid={}'.format(file_info['uuid_name'])
            return {"status": True, "msg": save_rs['msg'], "data": file_path}
        return {"status": False, "msg": save_rs['msg']}

    except Exception as e:
        print("文件保存错误", traceback.format_exc())


def files_upload_libs(file_data):
    """
    文件上传
    :param file_data: 文件列表
    :return:
    """
    if file_data is not None:
        result = _save_file(file_data)
        if result:
            file_path = result['data']
        else:
            file_path = ''
        return file_path
