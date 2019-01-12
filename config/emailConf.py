# !/usr/bin/python3.6
# -*- coding:utf-8 –*-


from email.header import Header
from email.mime.text import MIMEText
from config.ticketConf import configMap
import smtplib


def sendEmail(msg):
    """
    邮件通知
    :param str: email content
    :return:
    """
    is_email = configMap["email_conf"]["is_email"]
    if is_email:
        try:
            sender = configMap["email_conf"]["email"]
            receiver = configMap["email_conf"]["notice_email_list"]
            subject = '恭喜，您已订票成功'
            username = configMap["email_conf"]["username"]
            password = configMap["email_conf"]["password"]
            host = configMap["email_conf"]["host"]
            s = "{0}".format(msg)

            msg = MIMEText(s, 'plain', 'utf-8')
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