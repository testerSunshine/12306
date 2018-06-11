# -*- coding=utf-8 -*-
import datetime
import json
import random
import re
import socket
import sys
import threading
import time
import urllib
from collections import OrderedDict

import collections

from agency.cdn_utils import CDNProxy
from config import urlConf
from config.emailConf import sendEmail
from config.ticketConf import _get_yaml
from init import login
from init.login import GoLogin
from inter.AutoSubmitOrderRequest import autoSubmitOrderRequest
from inter.ConfirmSingleForQueueAsys import confirmSingleForQueueAsys
from inter.GetPassengerDTOs import getPassengerDTOs
from inter.GetQueueCountAsync import getQueueCountAsync
from inter.LiftTicketInit import liftTicketInit
from inter.Query import query
from inter.QueryOrderWaitTime import queryOrderWaitTime
from myException.PassengerUserException import PassengerUserException
from myException.UserPasswordException import UserPasswordException
from myException.ticketConfigException import ticketConfigException
from myException.ticketIsExitsException import ticketIsExitsException
from myException.ticketNumOutException import ticketNumOutException
from myUrllib.httpUtils import HTTPClient

reload(sys)
sys.setdefaultencoding('utf-8')


class selectFast:
    """
    快速提交车票通道
    """

    def __init__(self):
        self.from_station, self.to_station, self.station_dates, self._station_seat, self.is_more_ticket, self.ticke_peoples, self.select_refresh_interval, self.station_trains, self.ticket_black_list_time = self.get_ticket_info()
        self.is_aotu_code = _get_yaml()["is_aotu_code"]
        self.aotu_code_type = _get_yaml()["aotu_code_type"]
        self.is_cdn = _get_yaml()["is_cdn"]
        self.httpClint = HTTPClient()
        self.urls = urlConf.urls
        self.login = GoLogin(self.httpClint, self.urls, self.is_aotu_code, self.aotu_code_type)
        self.is_download_img = False
        self.cdn_list = []
        self.is_check_user = dict()
        self.ticket_black_list = dict()
        self.black_train_no = ""
        self.passengerTicketStrList = ""
        self.oldPassengerStr = ""


    def get_ticket_info(self):
        """
        获取配置信息
        :return:
        """
        ticket_info_config = _get_yaml()
        from_station = ticket_info_config["set"]["from_station"].encode("utf8")
        to_station = ticket_info_config["set"]["to_station"].encode("utf8")
        station_dates = ticket_info_config["set"]["station_dates"]
        set_type = ticket_info_config["set"]["set_type"]
        is_more_ticket = ticket_info_config["set"]["is_more_ticket"]
        ticke_peoples = ticket_info_config["set"]["ticke_peoples"]
        select_refresh_interval = ticket_info_config["select_refresh_interval"]
        station_trains = ticket_info_config["set"]["station_trains"]
        ticket_black_list_time = ticket_info_config["ticket_black_list_time"]
        print u"*" * 20
        print u"12306刷票小助手，最后更新于2018.2.28，请勿作为商业用途，交流群号：286271084"
        print u"如果有好的margin，请联系作者，表示非常感激\n"
        print u"当前配置：出发站：{0}\n到达站：{1}\n乘车日期：{2}\n坐席：{3}\n是否有票自动提交：{4}\n乘车人：{5}\n刷新间隔：随机(1-4S)\n候选购买车次：{7}\n僵尸票关小黑屋时长：{8}\n".format \
                (
                from_station,
                to_station,
                station_dates,
                ",".join(set_type),
                is_more_ticket,
                ",".join(ticke_peoples),
                select_refresh_interval,
                ",".join(station_trains),
                ticket_black_list_time,
            )
        print u"*" * 20
        return from_station, to_station, station_dates, set_type, is_more_ticket, ticke_peoples, select_refresh_interval, station_trains, ticket_black_list_time

    def station_table(self, from_station, to_station):
        """
        读取车站信息
        :param station:
        :return:
        """
        result = open('station_name.txt')
        info = result.read().split('=')[1].strip("'").split('@')
        del info[0]
        station_name = {}
        for i in range(0, len(info)):
            n_info = info[i].split('|')
            station_name[n_info[1]] = n_info[2]
        from_station = station_name[from_station.encode("utf8")]
        to_station = station_name[to_station.encode("utf8")]
        return from_station, to_station

    def call_login(self, auth=False):
        """
        登录回调方法
        :return:
        """
        if auth:
            return self.login.auth()
        else:
            self.login.go_login()

    def check_user(self):
        """
        检查用户是否达到订票条件
        :return:
        """
        check_user_url = self.urls["check_user_url"]
        data = {"_json_att": ""}
        check_user = self.httpClint.send(check_user_url, data)
        check_user_flag = check_user['data']['flag']
        if check_user_flag is True:
            self.is_check_user["user_time"] = datetime.datetime.now()
        else:
            if check_user['messages']:
                print (u'用户检查失败：%s，可能未登录，可能session已经失效' % check_user['messages'][0])
                print (u'正在尝试重新登录')
                self.call_login()
                self.is_check_user["user_time"] = datetime.datetime.now()
            else:
                print (u'用户检查失败： %s，可能未登录，可能session已经失效' % check_user)
                print (u'正在尝试重新登录')
                self.call_login()
                self.is_check_user["user_time"] = datetime.datetime.now()

    def main(self):
        l = liftTicketInit(session=self)
        l.reqLiftTicketInit()
        self.call_login()
        self.check_user()
        from_station, to_station = self.station_table(self.from_station, self.to_station)
        passengerTicketStrList, oldPassengerStr, set_type = "", "", ""
        num = 1
        while 1:
            try:
                num += 1
                if "user_time" in self.is_check_user and (
                        datetime.datetime.now() - self.is_check_user["user_time"]).seconds / 60 > 5:
                    # 5分钟检查一次用户是否登录
                    self.check_user()
                time.sleep(self.select_refresh_interval)
                if time.strftime('%H:%M:%S', time.localtime(time.time())) > "23:00:00" or time.strftime('%H:%M:%S',
                                                                                                        time.localtime(
                                                                                                            time.time())) < "06:00:00":
                    print(u"12306休息时间，本程序自动停止,明天早上6点将自动运行")
                    while 1:
                        time.sleep(1)
                        if "06:00:00" < time.strftime('%H:%M:%S', time.localtime(time.time())) < "23:00:00":
                            print(u"休息时间已过，重新开启检票功能")
                            self.call_login()
                            break
                start_time = datetime.datetime.now()

                q = query(session=self,
                          from_station=from_station,
                          to_station=to_station,
                          from_station_h=self.from_station,
                          to_station_h=self.to_station,
                          _station_seat=self._station_seat,
                          station_trains=self.station_trains,
                          station_dates=self.station_dates,
                          black_train_no=self.black_train_no)
                queryResult = q.sendQuery()
                self.black_train_no = ""  # 重置小黑屋名单
                # 查询接口
                if queryResult.get("status", False):
                    secretStr = queryResult.get("secretStr", "")
                    train_no = queryResult.get("train_no", "")
                    stationTrainCode = queryResult.get("stationTrainCode", "")
                    train_date = queryResult.get("train_date", "")
                    query_from_station_name = queryResult.get("query_from_station_name", "")
                    query_to_station_name = queryResult.get("query_to_station_name", "")
                    set_type = queryResult.get("set_type", "")
                    leftTicket = queryResult.get("leftTicket", "")
                    if self.ticket_black_list.has_key(train_no) and (
                            datetime.datetime.now() - self.ticket_black_list[train_no]).seconds / 60 < int(
                            self.ticket_black_list_time):
                        print(u"该车次{} 正在被关小黑屋，跳过此车次".format(train_no))
                    else:
                        # 获取联系人
                        if not self.passengerTicketStrList and not self.oldPassengerStr:
                            s = getPassengerDTOs(session=self, ticket_peoples=self.ticke_peoples, set_type=set_type)
                            getPassengerDTOsResult = s.getPassengerTicketStrListAndOldPassengerStr()
                            if getPassengerDTOsResult.get("status", False):
                                self.passengerTicketStrList = getPassengerDTOsResult.get("passengerTicketStrList", "")
                                self.oldPassengerStr = getPassengerDTOsResult.get("oldPassengerStr", "")
                                set_type = getPassengerDTOsResult.get("set_type", "")
                        # 提交订单
                        a = autoSubmitOrderRequest(session=self,
                                                   secretStr=secretStr,
                                                   train_date=train_date,
                                                   query_from_station_name=self.from_station,
                                                   query_to_station_name=self.to_station,
                                                   passengerTicketStr=self.passengerTicketStrList,
                                                   oldPassengerStr=self.oldPassengerStr
                                                   )
                        submitResult = a.sendAutoSubmitOrderRequest()
                        if submitResult.get("status", False):
                            result = submitResult.get("result", "")
                            # 订单排队
                            time.sleep(submitResult.get("ifShowPassCodeTime", 1))
                            g = getQueueCountAsync(session=self,
                                                   train_no=train_no,
                                                   stationTrainCode=stationTrainCode,
                                                   fromStationTelecode=query_from_station_name,
                                                   toStationTelecode=query_to_station_name,
                                                   leftTicket=leftTicket,
                                                   set_type=set_type,
                                                   users=len(self.ticke_peoples),
                                                   )
                            getQueueCountAsyncResult = g.sendGetQueueCountAsync()
                            time.sleep(submitResult.get("ifShowPassCodeTime", 1))
                            if getQueueCountAsyncResult.get("is_black", False):
                                self.black_train_no = getQueueCountAsyncResult.get("train_no", "")
                            if getQueueCountAsyncResult.get("status", False):
                                # 请求订单快读接口
                                c = confirmSingleForQueueAsys(session=self,
                                                              passengerTicketStr=self.passengerTicketStrList,
                                                              oldPassengerStr=self.oldPassengerStr,
                                                              result=result, )
                                confirmSingleForQueueAsysResult = c.sendConfirmSingleForQueueAsys()
                                # 排队
                                if confirmSingleForQueueAsysResult.get("status", False):
                                    qwt = queryOrderWaitTime(session=self)
                                    qwt.sendQueryOrderWaitTime()
                            else:
                                self.httpClint.del_cookies()

                else:
                    s_time = random.randint(0, 4)
                    time.sleep(s_time)
                    print u"正在第{0}次查询 随机停留时长：{6} 乘车日期: {1} 车次：{2} 查询无票 cdn轮询IP：{4}当前cdn总数：{5} 总耗时：{3}ms".format(num,
                                                                                                                ",".join(
                                                                                                                    self.station_dates),
                                                                                                                ",".join(
                                                                                                                    self.station_trains),
                                                                                                                (
                                                                                                                        datetime.datetime.now() - start_time).microseconds / 1000,
                                                                                                                self.httpClint.cdn,
                                                                                                                len(
                                                                                                                    self.cdn_list),
                                                                                                                s_time)
            except PassengerUserException as e:
                print e.message
                break
            except ticketConfigException as e:
                print e.message
                break
            except ticketIsExitsException as e:
                print e.message
                break
            except ticketNumOutException as e:
                print e.message
                break
            except UserPasswordException as e:
                print e.message
                break
            except ValueError as e:
                if e.message == "No JSON object could be decoded":
                    print(u"12306接口无响应，正在重试")
                else:
                    print(e.message)
            except KeyError as e:
                print(e.message)
            # except TypeError as e:
            #     print(u"12306接口无响应，正在重试 {0}".format(e.message))
            except socket.error as e:
                print(e.message)


if __name__ == '__main__':
    s = selectFast()
    s.main()
    # a = select('上海', '北京')
    # a.main()
