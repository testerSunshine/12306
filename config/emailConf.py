# -*- coding: utf8 -*-
__author__ = 'MR.wen'
from email.header import Header
from email.mime.text import MIMEText
from config.ticketConf import _get_yaml
import smtplib


def sendEmail(msg):
    """
    邮件通知
    :param str: email content
    :return:
    """
    email_conf = _get_yaml()
    is_email = email_conf["email_conf"]["is_email"]
    if is_email:
        try:
            sender = email_conf["email_conf"]["email"]
            receiver = email_conf["email_conf"]["notice_email_list"]
            subject = '恭喜，您已订票成功'
            username = email_conf["email_conf"]["username"]
            password = email_conf["email_conf"]["password"]
            host = email_conf["email_conf"]["host"]
            s = "{0}".format(msg)

            msg = MIMEText(s, 'plain', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = sender
            msg['To'] = receiver

            smtp = smtplib.SMTP_SSL()
            smtp.connect(host)
            smtp.login(username, password)
            smtp.sendmail(sender, receiver.split(","), msg.as_string())
            smtp.quit()
            print(u"邮件已通知, 请查收")
        except Exception as e:
            print(u"邮件配置有误{}".format(e))
    else:
        pass


if __name__ == '__main__':
    sendEmail(1)