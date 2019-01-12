# !/usr/bin/python3.6
# -*- coding:utf-8 –*-

import os
import platform

import ntplib
import datetime


def now():
    return str(datetime.datetime.now())[:22]


def autoSynchroTime():
    """
    同步北京时间，执行时候，请务必用sudo，sudo，sudo 执行，否则会报权限错误，windows打开ide或者cmd请用管理员身份
    :return:
    """
    c = ntplib.NTPClient()

    hosts = ['ntp1.aliyun.com', 'ntp2.aliyun.com', 'ntp3.aliyun.com', 'ntp4.aliyun.com', 'cn.pool.ntp.org']

    print(f"正在同步时间，请耐心等待30秒左右")
    print(f"系统当前时间{now()}")
    system = platform.system()
    if system == "Windows":
        for host in hosts:
            os.system('w32tm /register')
            os.system('net start w32time')
            os.system(f'w32tm /config /manualpeerlist:"{host}" /syncfromflags:manual /reliable:yes /update')
            os.system('ping -n 3 127.0.0.1 >nul')
            sin = os.system('w32tm /resync')
            if sin is 0:
                break
    else:  # mac同步地址，如果ntpdate未安装，brew install ntpdate    linux 安装 yum install -y ntpdate
        for host in hosts:
            sin = os.system('ntpdate {}'.format(host))
            if sin is 0:
                break
    print(f"同步后时间{now()}")


if __name__ == '__main__':
    autoSynchroTime()