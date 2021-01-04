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
        if TickerConfig.EMAIL_CONF["IS_MAIL"]:
            sender = TickerConfig.EMAIL_CONF["email"]
            receiver = TickerConfig.EMAIL_CONF["notice_email_list"]
            subject = '恭喜，您已订票成功'
            username = TickerConfig.EMAIL_CONF["username"]
            password = TickerConfig.EMAIL_CONF["password"]
            host = TickerConfig.EMAIL_CONF["host"]
            s = "{0}".format(msg)

            msg = MIMEText(s, 'plain', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = sender
            msg['To'] = receiver

            try:
                smtp = smtplib.SMTP_SSL(host)
                smtp.connect(host)
            except socket.error:
                smtp = smtplib.SMTP()
                smtp.connect(host)
            smtp.connect(host)
            smtp.login(username, password)
            smtp.sendmail(sender, receiver.split(","), msg.as_string())
            smtp.quit()
            print(u"邮件已通知, 请查收")
    except Exception as e:
        print(u"邮件配置有误{}".format(e))


if __name__ == '__main__':
    sendEmail(1)