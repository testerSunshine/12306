# -*- coding: utf8 -*-
import socket

__author__ = 'MR.wen'
from email.header import Header
from email.mime.text import MIMEText
from config.ticketConf import _get_yaml
# from ticketConf import _get_yaml
import smtplib
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


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

            try:
                smtp = smtplib.SMTP_SSL()
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
    else:
        pass

def sendmessage(ticketmseeage:str):
    '''
    短信通知，调用阿里云接口
    '''
    message_conf = _get_yaml()
    is_email = message_conf["message_conf"]["is_massage"]
    if is_email:
        accessKeyId = message_conf["message_conf"]["aliyunkeyid"]
        aliyunsecret = message_conf["message_conf"]["aliyunsecret"]
        phonenumbers = message_conf["message_conf"]["phone"]
        trcket = '{"code":"'+ticketmseeage+'"}'
        client = AcsClient(accessKeyId,aliyunsecret, 'cn-hangzhou')
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')
        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('PhoneNumbers', phonenumbers)
        request.add_query_param('SignName', '抢票小助手')
        request.add_query_param('TemplateCode', 'SMS_164266405')
        request.add_query_param('TemplateParam', trcket)
        response = client.do_action(request)
        # python2:  print(response) 
        print(str(response, encoding = 'utf-8'))
        try:
            pass
        except Exception as identifier:
            print(u"短信发送失败{}".format(identifier))

if __name__ == '__main__':
    # sendEmail(1)
    sendmessage("Z50")