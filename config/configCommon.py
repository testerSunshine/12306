# -*- coding: utf-8 -*-
import datetime
import os
import random
import sys
import time

from myException.ticketConfigException import ticketConfigException

rushRefreshMinTimeIntval = 2000
rushRefreshMaxTimeIntval = 3600000
rushRefreshTimeIntval = 100
# 最早运行时间
maxRunTime = 6
# 程序停止时间
maxRunStopTime = 23
# 可售天数
maxDate = 29

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

#
# def fileOpen(path):
#     """
#     文件读取兼容2和3
#     :param path: 文件读取路径
#     :return:
#     """
#     try:
#         with open(path, "r", ) as f:
#             return f
#     except TypeError:
#         with open(path, "r", ) as f:
#             return f



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
    if now.hour >= maxRunStopTime or now.hour < maxRunTime:
        print(u"12306休息时间，本程序自动停止,明天早上六点将自动运行")
        open_time = datetime.datetime(now.year, now.month, now.day, maxRunTime)
        if open_time < now:
            open_time += datetime.timedelta(1)
        time.sleep((open_time - now).seconds + round(random.uniform(1, 10)))
        session.call_login()


def checkDate(station_dates):
    """
    检查日期是否合法
    :param station_dates:
    :return:
    """
    today = datetime.datetime.now()
    maxDay = (today + datetime.timedelta(maxDate)).strftime("%Y-%m-%d")
    for station_date in station_dates[::-1]:
        date = datetime.datetime.strftime(datetime.datetime.strptime(station_date, "%Y-%m-%d"), "%Y-%m-%d")
        if date < today.strftime("%Y-%m-%d") or date > maxDay:
            print(u"警告：当前时间配置有小于当前时间或者大于最大时间: {}, 已自动忽略".format(station_date))
            station_dates.remove(station_date)
            if not station_dates:
                print(u"当前日期设置无符合查询条件的，已被全部删除，请查证后添加!!!")
                raise ticketConfigException(u"当前日期设置无符合查询条件的，已被全部删除，请查证后添加!!!")
        else:
            station_dates[station_dates.index(station_date)] = date
    return station_dates