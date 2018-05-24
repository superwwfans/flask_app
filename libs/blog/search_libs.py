#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 
# ---------------------------------------------------------


from model.artilce_model import Article


def search_libs(content):
    """
    :param content:
    :return:
    """
    articles, total = Article.search(content)
    context = {
        "articles": articles,
    }

    return context
