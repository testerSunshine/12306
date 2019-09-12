# coding=utf-8
import copy
import random
import wrapcache
from config import urlConf
from config.TicketEnmu import ticket
from myUrllib.httpUtils import HTTPClient
from config.configCommon import seat_conf_2
import TickerConfig


class query:
    """
    查询接口
    """

    def __init__(self, session, from_station, to_station, from_station_h, to_station_h, _station_seat, station_trains,
                 ticke_peoples_num, station_dates=None, ):
        self.session = session
        self.httpClint = HTTPClient(TickerConfig.IS_PROXY)
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

    def check_is_need_train(self, ticket_info):
        return ticket_info[3] in self.station_trains

    def sendQuery(self):
        """
        查询
        :return:
        """
        if TickerConfig.IS_CDN == 1:
            if self.session.cdn_list:
                self.httpClint.cdn = self.session.cdn_list[random.randint(0, len(self.session.cdn_list) - 1)]
        for station_date in self.station_dates:
            select_url = copy.copy(self.urls["select_url"])
            select_url["req_url"] = select_url["req_url"].format(station_date, self.from_station, self.to_station,
                                                                 self.session.queryUrl)
            station_ticket = self.httpClint.send(select_url)
            value = station_ticket.get("data", "")
            if not value:
                print(u'{0}-{1} 车次坐席查询为空，查询url: https://kyfw.12306.cn{2}, 可以手动查询是否有票'.format(
                    self.from_station_h,
                    self.to_station_h,
                    select_url["req_url"]))
            else:
                result = value.get('result', [])
                if result:
                    for i in value['result']:
                        ticket_info = i.split('|')
                        if self.session.flag:
                            print(f"车次：{ticket_info[3]} 出发站：{self.from_station_h} 到达站：{self.to_station_h} 历时：{ticket_info[10]}"
                                  f" 商务/特等座：{ticket_info[32] or '--'}"
                                  f" 一等座：{ticket_info[31] or '--'}"
                                  f" 二等座：{ticket_info[30] or '--'}"
                                  f" 动卧：{ticket_info[33] or '--'}"
                                  f" 硬卧：{ticket_info[28] or '--'}"
                                  f" 软座：{ticket_info[23] or '--'}"
                                  f" 硬座：{ticket_info[29] or '--'}"
                                  f" 无座：{ticket_info[26] or '--'}"
                                  f" {ticket_info[1] or '--'}")
                        if ticket_info[1] == "预订" and self.check_is_need_train(ticket_info):  # 筛选未在开始时间内的车次
                            for j in self._station_seat:
                                is_ticket_pass = ticket_info[j]
                                if ticket_info[11] == "Y":
                                    if is_ticket_pass != '' and is_ticket_pass != '无' and is_ticket_pass != '*':  # 过滤有效目标车次
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
                                        print(u'车次: {0} 始发车站: {1} 终点站: {2} {3}: {4}'.format(ticket_info[3],
                                                                                            self.from_station_h,
                                                                                            self.to_station_h,
                                                                                            seat_conf_2[j],
                                                                                            ticket_num))
                                        if seat_conf_2[j] == "无座" and ticket_info[3][0] in ["G", "D"]:
                                            seat = 30  # GD开头的无座直接强制改为二等座车次
                                        if wrapcache.get(train_no):
                                            print(ticket.QUERY_IN_BLACK_LIST.format(train_no))
                                            continue
                                        else:
                                            if ticket_num != "有" and self.ticke_peoples_num > ticket_num:
                                                if TickerConfig.IS_MORE_TICKET:
                                                    print(
                                                        u"余票数小于乘车人数，当前余票数: {}, 删减人车人数到: {}".format(ticket_num, ticket_num))
                                                    is_more_ticket_num = ticket_num
                                                else:
                                                    print(u"余票数小于乘车人数，当前设置不提交，放弃此次提交机会")
                                                    continue
                                            else:
                                                print(u"设置乘车人数为: {}".format(self.ticke_peoples_num))
                                                is_more_ticket_num = self.ticke_peoples_num
                                            print(ticket.QUERY_C)
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
                                elif is_ticket_pass == '无' and ticket_info[-2] == "1" and TickerConfig.TICKET_TYPE is 2:
                                    """
                                    is_ticket_pass如果有别的显示，但是可以候补，可以提issues提出来，附上query log，我将添加上
                                    判断车次是否可以候补
                                    目前的候补机制是只要一有候补位置，立马提交候补
                                    """
                                    # 如果最后一位为1，则是可以候补的，不知道这些正确嘛？
                                    nate = list(ticket_info[-1])
                                    if wrapcache.get(f"hb{ticket_info[2]}"):
                                        continue
                                    for set_type in TickerConfig.SET_TYPE:
                                        if TickerConfig.PASSENGER_TICKER_STR[set_type] not in nate:
                                            return {
                                                "secretList": ticket_info[0],
                                                "seat": [set_type],
                                                "train_no": ticket_info[2],
                                                "status": True,
                                            }
                else:
                    print(u"车次配置信息有误，或者返回数据异常，请检查 {}".format(station_ticket))
        self.session.flag = False
        return {"code": ticket.FAIL_CODE, "status": False, "cdn": self.httpClint.cdn, }


if __name__ == "__main__":
    q = query()
