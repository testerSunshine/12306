# -*- coding=utf-8 -*-
import os

from config.emailConf import sendEmail
from init import select_ticket_info


def run():
    select_ticket_info.select().main()


def Email():
    sendEmail(u"订票小助手测试一下")


# def sendWeChat():
#     os.system("cd notice & python notice.py")


if __name__ == '__main__':
    run()
    # sendWeChat()
