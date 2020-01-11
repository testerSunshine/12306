#coding: utf-8

import os
import time
import logging

from config import configCommon

logger = None
loggerHandler = None
dateStr = '' #默认拥有日期后缀
suffix = '' #除了日期外的后缀

def setSuffix(s):
	global suffix
	suffix = s

def getTodayDateStr():
	return time.strftime("%Y-%m-%d", time.localtime(configCommon.getNowTimestamp()))

def setDateStr(s):
	global dateStr
	dateStr = s

def isAnotherDay(s):
	global dateStr
	return dateStr != s

def getLogFile():
	global dateStr, suffix
	rtn = os.path.join(configCommon.getLogDir(), dateStr)
	if suffix:
		rtn += "_" + suffix
	return rtn + ".log"

def log(msg, func = "info"):
	global logger
	if not logger:
		logger = logging.getLogger()
		logger.setLevel(logging.INFO)

	todayStr = getTodayDateStr()
	if isAnotherDay(todayStr):
		setDateStr(todayStr)
		logger.removeHandler(loggerHandler)
		
		fh = logging.FileHandler(getLogFile())
		fm = logging.Formatter(u'[%(asctime)s][%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)')
		fh.setFormatter(fm)

		logger.addHandler(fh)

	levels = {
		"debug": logger.debug,
		"info": logger.info,
		"warning": logger.warning,
		"error": logger.error,
		"critical": logger.critical
	}

	levels[func](msg)