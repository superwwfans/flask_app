#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 
# ---------------------------------------------------------

from flask import current_app


def add_to_index(index, model):
    """
    添加索引,模型类中被搜索对象天添加到ES中
    :param index:
    :param model: 模型类
    :return:
    """
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index,
                                    doc_type=index,
                                    id=model.id,
                                    body=payload)


def remove_from_index(index, model):
    """
    删除和修改索引
    :param index:
    :param model:
    :return:
    """
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index,
                                     doc_type=index,
                                     id=model.id)


def query_index(index, query):
    """
    查询
    :param index: es索引
    :param query: 查询关键字
    :return:
    """
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index, doc_type=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}}})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']
