#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about: 
# ---------------------------------------------------------

import smtplib
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from email.mime.text import MIMEText


# Provide a class to allow SSL (Not TLS) connection for mail handlers by overloading the emit() method
class SSLSMTPHandler(SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
        """
        for toaddrs in self.toaddrs:
            try:
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP_SSL(self.mailhost, port)

                message = MIMEText(self.format(record), "html", "utf-8")
                message["Subject"] = self.subject
                message["From"] = self.fromaddr
                message["To"] = toaddrs

                smtp.login(self.username, self.password)
                smtp.sendmail(self.fromaddr, toaddrs, message.as_string())
                smtp.quit()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                self.handleError(record)