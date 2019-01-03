# coding=utf-8
import os
import platform

import ntplib
import datetime


def autoSynchroTime():
    """
    同步北京时间，执行时候，请务必用sudo，sudo，sudo 执行，否则会报权限错误，windows打开ide或者cmd请用管理员身份
    :return:
    """
    c = ntplib.NTPClient()

    hosts = ['ntp1.aliyun.com', 'ntp2.aliyun.com', 'ntp3.aliyun.com', 'ntp4.aliyun.com', 'cn.pool.ntp.org']

    print(u"正在同步时间，请耐心等待30秒左右")
    print(u"系统当前时间{}".format(str(datetime.datetime.now())[:22]))
    system = platform.system()
    if system == "Windows":  # windows 同步时间未测试过，参考地址：https://www.jianshu.com/p/92ec15da6cc3
        print(u"windeos系统暂时不提供自动对时功能，请手动同步北京时间")
        # for host in hosts:
        #
        #     try:
        #
        #         response = c.request(host)
        #
        #         if response:
        #             break
        #
        #     except Exception as e:
        #         print(u"时区获取异常：{0}".format(e))
        # current_time = response.tx_time
        #
        # _date, _time = str(datetime.datetime.fromtimestamp(current_time))[:22].split(' ')
        # print(u"北京标准时间", _date, _time)
        #
        # a, b, c = _time.split(':')
        #
        # c = float(c) + 0.5
        #
        # _time = "%s:%s:%s" % (a, b, c)
        #
        # os.system('date %s && time %s' % (_date, _time))
    else:  # mac同步地址，如果ntpdate未安装，brew install ntpdate    linux 安装 yum install -y ntpdate
        for host in hosts:
            sin = os.system('ntpdate {}'.format(host))
            if sin is 0:
                break
    print(u"同步后时间:{}".format(str(datetime.datetime.now())[:22]))


if __name__ == '__main__':
    autoSynchroTime()