# -*- coding: utf-8 -*-
import datetime
import os
import random
import sys
import time

saleMinDelayDay = 0
saleMaxDelayDay = 59
saleStartTime = "06:00:00"
saleStopTime = "23:00:00"
rushRefreshMinTimeIntval = 2000
rushRefreshMaxTimeIntval = 3600000
rushRefreshTimeIntval = 100

RS_SUC = 0
RS_TIMEOUT = 1
RS_JSON_ERROR = 2
RS_OTHER_ERROR = 3

seat_conf = {'商务座': 32,
             '一等座': 31,
             '二等座': 30,
             '特等座': 25,
             '软卧': 23,
             '硬卧': 28,
             '软座': 24,
             '硬座': 29,
             '无座': 26,
             '动卧': 33,
             }
if sys.version_info.major == 2:
    seat_conf_2 = dict([(v, k) for (k, v) in seat_conf.iteritems()])
else:
    seat_conf_2 = dict([(v, k) for (k, v) in seat_conf.items()])


def getNowTimestamp():
    return time.time()


def getMinimumDate():
    return time.localtime(getNowTimestamp() + saleMinDelayDay * 24 * 3600)[:3]


def getMaximumDate():
    return time.localtime(getNowTimestamp() + saleMaxDelayDay * 24 * 3600)[:3]


def getMinimumTime():
    return [int(x) for x in saleStartTime.split(":")]


def getMaximumTime():
    return [int(x) for x in saleStopTime.split(":")]


def decMakeDir(func):
    def handleFunc(*args, **kwargs):
        dirname = func(*args, **kwargs)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        elif not os.path.isdir(dirname):
            pass

        return dirname

    return func


def getWorkDir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@decMakeDir
def getTmpDir():
    return os.path.join(getWorkDir(), "tmp")


@decMakeDir
def getLogDir():
    return os.path.join(getTmpDir(), "log")


@decMakeDir
def getCacheDir():
    return os.path.join(getTmpDir(), "cache")


@decMakeDir
def getVCodeDir():
    return os.path.join(getTmpDir(), "vcode")


def getVCodeImageFile(imageName):
    return os.path.join(getVCodeDir(), imageName + ".jpg")


def getCacheFile(cacheType):
    return os.path.join(getCacheDir(), cacheType + ".cache")


def checkSleepTime(session):
    now = datetime.datetime.now()
    if now.hour >= 23 or now.hour < 6:
        print(u"12306休息时间，本程序自动停止,明天早上六点点将自动运行")
        open_time = datetime.datetime(now.year, now.month, now.day, 6)
        if open_time < now:
            open_time += datetime.timedelta(1)
        time.sleep((open_time - now).seconds + round(random.uniform(1, 10)))
        session.call_login()
