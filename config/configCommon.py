# -*- coding: utf-8 -*-

import os
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
