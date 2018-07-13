#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 
# ---------------------------------------------------------
"""
    全文搜索接口
"""

from model.artilce_model import Article


def search_libs(content):
    """
    全文搜索
    :param content:用户输入内容
    :return:
    """
    if content:
        articles, total = Article.search(content)
        context = {
            "articles": articles,
        }
        return context
    else:
        context = {
            "articles": '',
        }
        return context