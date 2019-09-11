# -*- coding: utf8 -*-
import socket
__author__ = 'MR.wen'
import TickerConfig
from email.header import Header
from email.mime.text import MIMEText
import smtplib


def sendEmail(msg):
    """
    邮件通知
    :param str: email content
    :return:
    """
    try:
        sender = TickerConfig.EMAIL_CONF["email"]
        receiver = TickerConfig.EMAIL_CONF["notice_email_list"]
        isSsl = TickerConfig.EMAIL_CONF["is_ssl"]
        subject = '恭喜，您已订票成功'
        username = TickerConfig.EMAIL_CONF["username"]
        password = TickerConfig.EMAIL_CONF["password"]
        host = TickerConfig.EMAIL_CONF["host"]
        port = TickerConfig.EMAIL_CONF["port"]
        s = "{0}".format(msg)

        msg = MIMEText(s, 'plain', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = sender
        msg['To'] = receiver

        if isSsl:
            smtp = smtplib.SMTP_SSL(host = host, port = port)
        else:
            smtp = smtplib.SMTP(host = host, port = port)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver.split(","), msg.as_string())
        smtp.quit()
        print(u"邮件已通知, 请查收")
    except Exception as e:
        print(u"邮件配置有误{}".format(e))


if __name__ == '__main__':
    sendEmail(1)