# coding=utf-8
import copy
import threading
import time

import random

import wrapcache
from config import urlConf
from config.TicketEnmu import ticket
from myUrllib.httpUtils import HTTPClient
from config.configCommon import seat_conf_2
from utils.timeUtil import time_to_minutes


class query:
    """
    查询接口
    """

    def __init__(self, session, from_station, to_station, from_station_h, to_station_h, _station_seat, station_trains,
                 ticke_peoples_num, station_dates=None, ):
        self.session = session
        self.httpClint = HTTPClient(session.is_proxy)
        self.urls = urlConf.urls
        self.from_station = from_station
        self.to_station = to_station
        self.from_station_h = from_station_h
        self.to_station_h = to_station_h
        self.station_trains = station_trains
        self._station_seat = _station_seat if isinstance(_station_seat, list) else list(_station_seat)
        self.station_dates = station_dates if isinstance(station_dates, list) else list(station_dates)
        self.ticket_black_list = dict()
        self.ticke_peoples_num = ticke_peoples_num
        # by time
        self.is_by_time = session.is_by_time
        self.train_types = session.train_types
        self.departure_time = session.departure_time
        self.arrival_time = session.arrival_time
        self.take_time = session.take_time

    @classmethod
    def station_seat(self, index):
        """
        获取车票对应坐席
        :return:
        """
        seat = {'商务座': 32,
                '一等座': 31,
                '二等座': 30,
                '特等座': 25,
                '软卧': 23,
                '硬卧': 28,
                '硬座': 29,
                '无座': 26,
                '动卧': 33,
                }
        return seat[index]

    def check_time_interval(self, ticket_info):
        return self.departure_time <= time_to_minutes(ticket_info[8]) and \
               time_to_minutes(ticket_info[9]) <= self.arrival_time and \
               time_to_minutes(ticket_info[10]) <= self.take_time

    def check_train_types(self, train):
        train_type = train[0]
        if train_type != "G" and train_type != "D": train_type = "O"
        if train_type in self.train_types:
            return True
        else:
            return False

    def check_is_need_train(self, ticket_info):
        if self.is_by_time:
            return self.check_train_types(ticket_info[3]) and self.check_time_interval(ticket_info)
        else:
            return ticket_info[3] in self.station_trains

    def sendQuery(self):
        """
        查询
        :return:
        """
        if self.session.is_cdn == 1:
            if self.session.cdn_list:
                self.httpClint.cdn = self.session.cdn_list[random.randint(0, len(self.session.cdn_list) - 1)]
        for station_date in self.station_dates:
            select_url = copy.copy(self.urls["select_url"])
            select_url["req_url"] = select_url["req_url"].format(station_date, self.from_station, self.to_station,
                                                                 self.session.queryUrl)
            station_ticket = self.httpClint.send(select_url)
            if station_ticket.get("c_url", ""):
                print(u"设置当前查询url为: {}".format(station_ticket.get("c_url", "")))
                self.session.queryUrl = station_ticket.get("c_url", "")  # 重设查询接口
                continue
            value = station_ticket.get("data", "")
            if not value:
                print(u'{0}-{1} 车次坐席查询为空,ip网络异常，查询url: https://kyfw.12306.cn{2}, 可以手动查询是否有票'.format(self.from_station_h,
                                                                                               self.to_station_h,
                                                                                               select_url["req_url"]))
            else:
                result = value.get('result', [])
                if result:
                    for i in value['result']:
                        ticket_info = i.split('|')
                        if ticket_info[11] == "Y" and ticket_info[1] == "预订":  # 筛选未在开始时间内的车次
                            for j in self._station_seat:
                                is_ticket_pass = ticket_info[j]
                                if is_ticket_pass != '' and is_ticket_pass != '无' and is_ticket_pass != '*' and self.check_is_need_train(
                                        ticket_info):  # 过滤有效目标车次
                                    secretStr = ticket_info[0]
                                    train_no = ticket_info[2]
                                    query_from_station_name = ticket_info[6]
                                    query_to_station_name = ticket_info[7]
                                    train_location = ticket_info[15]
                                    stationTrainCode = ticket_info[3]
                                    leftTicket = ticket_info[12]
                                    start_time = ticket_info[8]
                                    arrival_time = ticket_info[9]
                                    distance_time = ticket_info[10]
                                    print(start_time, arrival_time, distance_time)
                                    seat = j
                                    try:
                                        ticket_num = int(ticket_info[j])
                                    except ValueError:
                                        ticket_num = "有"
                                    print (u'车次: {0} 始发车站: {1} 终点站: {2} {3}: {4}'.format(ticket_info[3],
                                                                                         self.from_station_h,
                                                                                         self.to_station_h,
                                                                                         seat_conf_2[j],
                                                                                         ticket_num))
                                    if wrapcache.get(train_no):
                                        print(ticket.QUERY_IN_BLACK_LIST.format(train_no))
                                        continue
                                    else:
                                        if ticket_num != "有" and self.ticke_peoples_num > ticket_num:
                                            if self.session.is_more_ticket:
                                                print(
                                                    u"余票数小于乘车人数，当前余票数: {}, 删减人车人数到: {}".format(ticket_num, ticket_num))
                                                is_more_ticket_num = ticket_num
                                            else:
                                                print(u"余票数小于乘车人数，当前设置不提交，放弃此次提交机会")
                                                continue
                                        else:
                                            print(u"设置乘车人数为: {}".format(self.ticke_peoples_num))
                                            is_more_ticket_num = self.ticke_peoples_num
                                        print (ticket.QUERY_C)
                                        return {
                                            "secretStr": secretStr,
                                            "train_no": train_no,
                                            "stationTrainCode": stationTrainCode,
                                            "train_date": station_date,
                                            "query_from_station_name": query_from_station_name,
                                            "query_to_station_name": query_to_station_name,
                                            "seat": seat,
                                            "leftTicket": leftTicket,
                                            "train_location": train_location,
                                            "code": ticket.SUCCESS_CODE,
                                            "is_more_ticket_num": is_more_ticket_num,
                                            "cdn": self.httpClint.cdn,
                                            "status": True,
                                        }
                else:
                    print(u"车次配置信息有误，或者返回数据异常，请检查 {}".format(station_ticket))
        return {"code": ticket.FAIL_CODE, "status": False, "cdn": self.httpClint.cdn,}


if __name__ == "__main__":
    q = query()
