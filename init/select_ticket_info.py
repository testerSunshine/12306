# -*- coding=utf-8 -*-
import datetime
import random
import socket
import sys
import time

import wrapcache

from config import urlConf
from config.TicketEnmu import ticket
from config.ticketConf import _get_yaml
from init.login import GoLogin
from inter.AutoSubmitOrderRequest import autoSubmitOrderRequest
from inter.CheckUser import checkUser
from inter.GetPassengerDTOs import getPassengerDTOs
from inter.LiftTicketInit import liftTicketInit
from inter.Query import query
from inter.SubmitOrderRequest import submitOrderRequest
from myException.PassengerUserException import PassengerUserException
from myException.UserPasswordException import UserPasswordException
from myException.ticketConfigException import ticketConfigException
from myException.ticketIsExitsException import ticketIsExitsException
from myException.ticketNumOutException import ticketNumOutException
from myUrllib.httpUtils import HTTPClient

reload(sys)
sys.setdefaultencoding('utf-8')


class select:
    """
    快速提交车票通道
    """

    def __init__(self):
        self.from_station, self.to_station, self.station_dates, self._station_seat, self.is_more_ticket, \
        self.ticke_peoples, self.select_refresh_interval, self.station_trains, self.ticket_black_list_time, \
        self.order_type = self.get_ticket_info()
        self.is_auto_code = _get_yaml()["is_auto_code"]
        self.auto_code_type = _get_yaml()["auto_code_type"]
        self.is_cdn = _get_yaml()["is_cdn"]
        self.httpClint = HTTPClient()
        self.urls = urlConf.urls
        self.login = GoLogin(self, self.is_auto_code, self.auto_code_type)
        self.cdn_list = []
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
        order_type = ticket_info_config["order_type"]
        print u"*" * 20
        print u"12306刷票小助手，最后更新于2018.2.28，请勿作为商业用途，交流群号：286271084"
        print u"如果有好的margin，请联系作者，表示非常感激\n"
        print u"当前配置：出发站：{0}\n到达站：{1}\n乘车日期：{2}\n坐席：{3}\n是否有票自动提交：{4}\n乘车人：{5}\n" \
              u"刷新间隔：随机(1-4S)\n候选购买车次：{7}\n僵尸票关小黑屋时长：{8}\n 下单接口：{9}\n".format \
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
                order_type,
            )
        print u"*" * 20
        return from_station, to_station, station_dates, set_type, is_more_ticket, ticke_peoples, select_refresh_interval, station_trains, ticket_black_list_time, order_type

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

    def main(self):
        l = liftTicketInit(session=self)
        l.reqLiftTicketInit()
        self.call_login()
        checkUser(self).sendCheckUser()
        from_station, to_station = self.station_table(self.from_station, self.to_station)
        num = 1
        while 1:
            try:
                num += 1
                checkUser(self).sendCheckUser()
                time.sleep(self.select_refresh_interval)
                if time.strftime('%H:%M:%S', time.localtime(time.time())) > "23:00:00" or time.strftime('%H:%M:%S',
                                                                                                        time.localtime(
                                                                                                            time.time())) < "06:00:00":
                    print(ticket.REST_TIME)
                    while 1:
                        time.sleep(1)
                        if "06:00:00" < time.strftime('%H:%M:%S', time.localtime(time.time())) < "23:00:00":
                            print(ticket.REST_TIME_PAST)
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
                          station_dates=self.station_dates, )
                queryResult = q.sendQuery()
                # 查询接口
                if queryResult.get("status", False):
                    train_no = queryResult.get("train_no", "")
                    train_date = queryResult.get("train_date", "")
                    stationTrainCode = queryResult.get("stationTrainCode", "")
                    set_type = queryResult.get("set_type", "")
                    secretStr = queryResult.get("secretStr", "")
                    leftTicket = queryResult.get("leftTicket", "")
                    query_from_station_name = queryResult.get("query_from_station_name", "")
                    query_to_station_name = queryResult.get("query_to_station_name", "")
                    if wrapcache.get(train_no):
                        print(ticket.QUEUE_WARNING_MSG.format(train_no))
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
                        if self.order_type == 1:  # 快读下单
                            a = autoSubmitOrderRequest(session=self,
                                                       secretStr=secretStr,
                                                       train_date=train_date,
                                                       passengerTicketStr=self.passengerTicketStrList,
                                                       oldPassengerStr=self.oldPassengerStr,
                                                       train_no=train_no,
                                                       stationTrainCode=stationTrainCode,
                                                       leftTicket=leftTicket,
                                                       set_type=set_type,
                                                       query_from_station_name=query_from_station_name,
                                                       query_to_station_name=query_to_station_name,
                                                       )
                            a.sendAutoSubmitOrderRequest()
                        elif self.order_type == 2:  # 普通下单
                            sor = submitOrderRequest(self, secretStr, from_station, to_station, train_no, set_type,
                                                     self.passengerTicketStrList, self.oldPassengerStr, train_date,
                                                     self.ticke_peoples)
                            sor.sendSubmitOrderRequest()


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
            except TypeError as e:
                print(u"12306接口无响应，正在重试 {0}".format(e.message))
            except socket.error as e:
                print(e.message)


if __name__ == '__main__':
    pass