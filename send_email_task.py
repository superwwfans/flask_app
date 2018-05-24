#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 
# ---------------------------------------------------------
from __future__ import absolute_import
import smtplib
from email.mime.text import MIMEText
from celery import Celery
from ext import app

celery_app = Celery(app.import_name)
celery_app.conf.update(app.config)


@celery_app.task
def send_email(title, content, to_email_list=None, from_email=None):
    """
    发送邮件
    :param to_email_list:
    :param from_email:
    :param title:
    :param content:
    :return:
    """

    to_email_list = app.config["ADMINS"]
    for to_email in to_email_list:
        message = MIMEText(content, "html", "utf-8")
        message["Subject"] = "{}-博客评论".format(title)
        message["From"] = app.config["MAIL_USERNAME"]
        message["To"] = to_email
        try:
            s = smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
            s.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            with app.app_context():
                s.send_message(from_email, to_email, message.as_string())
        except Exception as e:

            print(e)

