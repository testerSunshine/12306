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

    print(u"正在同步时间，请耐心等待30秒左右，如果下面有错误发送，可以忽略！！")
    print(u"系统当前时间{}".format(str(datetime.datetime.now())[:22]))
    system = platform.system()
    if system == "Windows":  # windows 同步时间未测试过，参考地址：https://www.jianshu.com/p/92ec15da6cc3
        for host in hosts:
            os.popen('w32tm /register')
            os.popen('net start w32time')
            os.popen('w32tm /config /manualpeerlist:"{}" /syncfromflags:manual /reliable:yes /update'.format(host))
            os.popen('ping -n 3 127.0.0.1 >nul')
            sin = os.popen('w32tm /resync')
            if sin is 0:
                break
    else:  # mac同步地址，如果ntpdate未安装，brew install ntpdate    linux 安装 yum install -y ntpdate
        for host in hosts:
            sin = os.popen('ntpdate {}'.format(host))
            if sin is 0:
                break
    print(u"同步后时间:{}".format(str(datetime.datetime.now())[:22]))


if __name__ == '__main__':
    autoSynchroTime()