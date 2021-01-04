# -*- coding=utf-8 -*-
import argparse
import sys


def parser_arguments(argv):
    """
    不应该在这里定义，先放在这里
    :param argv:
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("operate", type=str, help="r: 运行抢票程序, c: 过滤cdn, t: 测试邮箱和server酱，server酱需要打开开关")

    return parser.parse_args(argv)


if __name__ == '__main__':
    args = parser_arguments(sys.argv[1:])
    if args.operate == "r":
        from init import select_ticket_info
        select_ticket_info.select().main()
    elif args.operate == "t":
        from config.emailConf import sendEmail
        from config.serverchanConf import sendServerChan
        sendEmail(u"订票小助手测试一下")
        sendServerChan("订票小助手测试一下")
    elif args.operate == "c":
        from agency.cdn_utils import filterCdn
        filterCdn()

