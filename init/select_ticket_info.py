# -*- coding=utf-8 -*-
import datetime
import random
import os
import socket
import sys
import threading
import time

import wrapcache

from agency.cdn_utils import CDNProxy
from config import urlConf, configCommon
from config.AutoSynchroTime import autoSynchroTime
from config.TicketEnmu import ticket
from config.configCommon import seat_conf
from config.configCommon import seat_conf_2
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
from utils.timeUtil import time_to_minutes, minutes_to_time

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass


class select:
    """
    快速提交车票通道
    """

    def __init__(self):
        self.from_station, self.to_station, self.station_dates, self._station_seat, self.is_more_ticket, \
        self.ticke_peoples, self.station_trains, self.ticket_black_list_time, \
        self.order_type, self.is_by_time, self.train_types, self.departure_time, \
        self.arrival_time, self.take_time, self.order_model, self.open_time, self.is_proxy = self.get_ticket_info()
        self.is_auto_code = _get_yaml()["is_auto_code"]
        self.auto_code_type = _get_yaml()["auto_code_type"]
        self.is_cdn = _get_yaml()["is_cdn"]
        self.httpClint = HTTPClient(self.is_proxy)
        self.urls = urlConf.urls
        self.login = GoLogin(self, self.is_auto_code, self.auto_code_type)
        self.cdn_list = []
        self.queryUrl = "leftTicket/queryZ"
        self.passengerTicketStrList = ""
        self.oldPassengerStr = ""
        self.set_type = ""

    def get_ticket_info(self):
        """
        获取配置信息
        :return:
        """
        ticket_info_config = _get_yaml()
        from_station = ticket_info_config["set"]["from_station"]
        to_station = ticket_info_config["set"]["to_station"]
        station_dates = ticket_info_config["set"]["station_dates"]
        set_names = ticket_info_config["set"]["set_type"]
        try:
            set_type = [seat_conf[x.encode("utf-8")] for x in ticket_info_config["set"]["set_type"]]
        except KeyError:
            set_type = [seat_conf[x] for x in ticket_info_config["set"]["set_type"]]
        is_more_ticket = ticket_info_config["set"]["is_more_ticket"]
        ticke_peoples = ticket_info_config["set"]["ticke_peoples"]
        station_trains = ticket_info_config["set"]["station_trains"]
        ticket_black_list_time = ticket_info_config["ticket_black_list_time"]
        order_type = ticket_info_config["order_type"]

        # by time
        is_by_time = ticket_info_config["set"]["is_by_time"]
        train_types = ticket_info_config["set"]["train_types"]
        departure_time = time_to_minutes(ticket_info_config["set"]["departure_time"])
        arrival_time = time_to_minutes(ticket_info_config["set"]["arrival_time"])
        take_time = time_to_minutes(ticket_info_config["set"]["take_time"])

        # 下单模式
        order_model = ticket_info_config["order_model"]
        open_time = ticket_info_config["open_time"]

        # 代理模式
        is_proxy = ticket_info_config["is_proxy"]

        print(u"*" * 50)
        print(u"检查当前python版本为：{}，目前版本只支持2.7.10-2.7.15".format(sys.version.split(" ")[0]))
        print(u"12306刷票小助手，最后更新于2019.01.08，请勿作为商业用途，交流群号：286271084(已满)，"
              u" 2群：649992274(已满)\n"
              u" 3群：632501142(已满)\n"
              u" 4群: 606340519(已满)\n"
              u" 5群: 948526733(未满)\n"
              u" 6群: 444101020(未满)\n"
              u" 7群: 660689659(未满)\n"
              )
        if is_by_time:
            method_notie = u"购票方式：根据时间区间购票\n可接受最早出发时间：{0}\n可接受最晚抵达时间：{1}\n可接受最长旅途时间：{2}\n可接受列车类型：{3}\n" \
                .format(minutes_to_time(departure_time), minutes_to_time(arrival_time), minutes_to_time(take_time),
                        " , ".join(train_types))
        else:
            method_notie = u"购票方式：根据候选车次购买\n候选购买车次：{0}".format(",".join(station_trains))
        print (u"当前配置：\n出发站：{0}\n到达站：{1}\n乘车日期：{2}\n坐席：{3}\n是否有票优先提交：{4}\n乘车人：{5}\n" \
               u"刷新间隔: 随机(1-3S)\n{6}\n僵尸票关小黑屋时长: {7}\n下单接口: {8}\n下单模式: {9}\n预售踩点时间:{10} ".format \
                (
                from_station,
                to_station,
                station_dates,
                ",".join(set_names),
                is_more_ticket,
                ",".join(ticke_peoples),
                method_notie,
                ticket_black_list_time,
                order_type,
                order_model,
                open_time,
            ))
        print (u"*" * 50)
        return from_station, to_station, station_dates, set_type, is_more_ticket, ticke_peoples, station_trains, \
               ticket_black_list_time, order_type, is_by_time, train_types, departure_time, arrival_time, take_time, \
               order_model, open_time, is_proxy

    def station_table(self, from_station, to_station):
        """
        读取车站信息
        :param station:
        :return:
        """
        path = os.path.join(os.path.dirname(__file__), '../station_name.txt')
        result = open(path)
        info = result.read().split('=')[1].strip("'").split('@')
        del info[0]
        station_name = {}
        for i in range(0, len(info)):
            n_info = info[i].split('|')
            station_name[n_info[1]] = n_info[2]
        try:
            from_station = station_name[from_station.encode("utf8")]
            to_station = station_name[to_station.encode("utf8")]
        except KeyError:
            from_station = station_name[from_station]
            to_station = station_name[to_station]
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

    def cdn_req(self, cdn):
        for i in range(len(cdn) - 1):
            http = HTTPClient(0)
            urls = self.urls["loginInitCdn"]
            http._cdn = cdn[i].replace("\n", "")
            start_time = datetime.datetime.now()
            rep = http.send(urls)
            if rep and "message" not in rep and (datetime.datetime.now() - start_time).microseconds / 1000 < 500:
                if cdn[i].replace("\n", "") not in self.cdn_list:  # 如果有重复的cdn，则放弃加入
                    # print(u"加入cdn {0}".format(cdn[i].replace("\n", "")))
                    self.cdn_list.append(cdn[i].replace("\n", ""))
        print(u"所有cdn解析完成...")

    def cdn_certification(self):
        """
        cdn 认证
        :return:
        """
        if self.is_cdn == 1:
            CDN = CDNProxy()
            all_cdn = CDN.open_cdn_file()
            if all_cdn:
                # print(u"由于12306网站策略调整，cdn功能暂时关闭。")
                print(u"开启cdn查询")
                print(u"本次待筛选cdn总数为{}, 筛选时间大约为5-10min".format(len(all_cdn)))
                t = threading.Thread(target=self.cdn_req, args=(all_cdn,))
                t.setDaemon(True)
                # t2 = threading.Thread(target=self.set_cdn, args=())
                t.start()
                # t2.start()
            else:
                raise ticketConfigException(u"cdn列表为空，请先加载cdn")

    def main(self):
        # autoSynchroTime()  # 同步时间
        self.cdn_certification()
        l = liftTicketInit(self)
        l.reqLiftTicketInit()
        self.call_login()
        check_user = checkUser(self)
        t = threading.Thread(target=check_user.sendCheckUser)
        t.setDaemon(True)
        t.start()
        from_station, to_station = self.station_table(self.from_station, self.to_station)
        num = 0
        s = getPassengerDTOs(session=self, ticket_peoples=self.ticke_peoples)
        s.sendGetPassengerDTOs()
        while 1:
            try:
                num += 1
                now = datetime.datetime.now()  # 感谢群里大佬提供整点代码
                configCommon.checkSleepTime(self)   # 晚上到点休眠
                if self.order_model is 1:
                    sleep_time_s = 0.5
                    sleep_time_t = 0.6
                    # 测试了一下有微妙级的误差，应该不影响，测试结果：2019-01-02 22:30:00.004555，预售还是会受到前一次刷新的时间影响，暂时没想到好的解决方案
                    while not now.strftime("%H:%M:%S") == self.open_time:
                        now = datetime.datetime.now()
                        if now.strftime("%H:%M:%S") > self.open_time:
                            break
                        time.sleep(0.0001)
                else:
                    sleep_time_s = 0.5
                    sleep_time_t = 3
                q = query(session=self,
                          from_station=from_station,
                          to_station=to_station,
                          from_station_h=self.from_station,
                          to_station_h=self.to_station,
                          _station_seat=self._station_seat,
                          station_trains=self.station_trains,
                          station_dates=self.station_dates,
                          ticke_peoples_num=len(self.ticke_peoples),
                          )
                queryResult = q.sendQuery()
                # 查询接口
                if queryResult.get("status", False):
                    train_no = queryResult.get("train_no", "")
                    train_date = queryResult.get("train_date", "")
                    stationTrainCode = queryResult.get("stationTrainCode", "")
                    secretStr = queryResult.get("secretStr", "")
                    seat = queryResult.get("seat", "")
                    leftTicket = queryResult.get("leftTicket", "")
                    query_from_station_name = queryResult.get("query_from_station_name", "")
                    query_to_station_name = queryResult.get("query_to_station_name", "")
                    is_more_ticket_num = queryResult.get("is_more_ticket_num", len(self.ticke_peoples))
                    if wrapcache.get(train_no):
                        print(ticket.QUEUE_WARNING_MSG.format(train_no))
                    else:
                        # 获取联系人
                        s = getPassengerDTOs(session=self, ticket_peoples=self.ticke_peoples,
                                             set_type=seat_conf_2[seat],
                                             is_more_ticket_num=is_more_ticket_num)
                        getPassengerDTOsResult = s.getPassengerTicketStrListAndOldPassengerStr()
                        if getPassengerDTOsResult.get("status", False):
                            self.passengerTicketStrList = getPassengerDTOsResult.get("passengerTicketStrList", "")
                            self.oldPassengerStr = getPassengerDTOsResult.get("oldPassengerStr", "")
                            self.set_type = getPassengerDTOsResult.get("set_type", "")
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
                                                       set_type=self.set_type,
                                                       query_from_station_name=query_from_station_name,
                                                       query_to_station_name=query_to_station_name,
                                                       )
                            a.sendAutoSubmitOrderRequest()
                        elif self.order_type == 2:  # 普通下单
                            sor = submitOrderRequest(self, secretStr, from_station, to_station, train_no, self.set_type,
                                                     self.passengerTicketStrList, self.oldPassengerStr, train_date,
                                                     self.ticke_peoples)
                            sor.sendSubmitOrderRequest()
                else:
                    random_time = round(random.uniform(sleep_time_s, sleep_time_t), 2)
                    print(u"正在第{0}次查询 随机停留时长：{6} 乘车日期: {1} 车次：{2} 查询无票 cdn轮询IP：{4}当前cdn总数：{5} 总耗时：{3}ms".format(num,
                                                                                                                ",".join(
                                                                                                                    self.station_dates),
                                                                                                                ",".join(
                                                                                                                    self.station_trains),
                                                                                                                (
                                                                                                                        datetime.datetime.now() - now).microseconds / 1000,
                                                                                                                queryResult.get(
                                                                                                                    "cdn",
                                                                                                                    None),
                                                                                                                len(
                                                                                                                    self.cdn_list),
                                                                                                                random_time))
                    time.sleep(random_time)
            except PassengerUserException as e:
                print(e)
                break
            except ticketConfigException as e:
                print(e)
                break
            except ticketIsExitsException as e:
                print(e)
                break
            except ticketNumOutException as e:
                print(e)
                break
            except UserPasswordException as e:
                print(e)
                break
            except ValueError as e:
                if e == "No JSON object could be decoded":
                    print(u"12306接口无响应，正在重试")
                else:
                    print(e)
            except KeyError as e:
                print(e)
            except TypeError as e:
                print(u"12306接口无响应，正在重试 {0}".format(e))
            except socket.error as e:
                print(e)


if __name__ == '__main__':
    s = select()
    cdn = CDNProxy().open_cdn_file()
    s.cdn_req(cdn)
