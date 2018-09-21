# coding=utf-8
import copy
import datetime
import wrapcache
from config.TicketEnmu import ticket


class query:
    """
    查询接口
    """

    def __init__(self, session, from_station, to_station, from_station_h, to_station_h, _station_seat, station_trains,
                 ticke_peoples_num, station_dates=None,):
        self.session = session
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
                }
        return seat[index]

    def sendQuery(self):
        """
        查询
        :return:
        """
        for station_date in self.station_dates:
            select_url = copy.copy(self.session.urls["select_url"])
            select_url["req_url"] = select_url["req_url"].format(station_date, self.from_station, self.to_station)
            station_ticket = self.session.httpClint.send(select_url)
            value = station_ticket.get("data", "")
            if not value:
                print (u'{0}-{1} 车次坐席查询为空'.format(self.from_station_h, self.to_station_h))
            else:
                result = value.get('result', [])
                if result:
                    for i in value['result']:
                        ticket_info = i.split('|')
                        if ticket_info[11] == "Y" and ticket_info[1].encode("utf8") == "预订":  # 筛选未在开始时间内的车次
                            for j in xrange(len(self._station_seat)):
                                is_ticket_pass = ticket_info[self.station_seat(self._station_seat[j].encode("utf8"))]
                                if is_ticket_pass != '' and is_ticket_pass != '无' and ticket_info[3] in self.station_trains and is_ticket_pass != '*':  # 过滤有效目标车次
                                    secretStr = ticket_info[0]
                                    train_no = ticket_info[2]
                                    query_from_station_name = ticket_info[6]
                                    query_to_station_name = ticket_info[7]
                                    train_location = ticket_info[15]
                                    stationTrainCode = ticket_info[3]
                                    leftTicket = ticket_info[12]
                                    seat = self._station_seat[j].encode("utf8")
                                    try:
                                        ticket_num = int(ticket_info[self.station_seat(self._station_seat[j].encode("utf8"))])
                                    except ValueError:
                                        ticket_num = "有"
                                    print (u'车次: {0} 始发车站: {1} 终点站: {2} {3}: {4}'.format(ticket_info[3],
                                                                                             self.from_station_h,
                                                                                             self.to_station_h,
                                                                                             self._station_seat[j].encode("utf8"),
                                                                                             ticket_num))
                                    if wrapcache.get(train_no):
                                        print(ticket.QUERY_IN_BLACK_LIST.format(train_no))
                                        continue

                                    else:
                                        if ticket_num != "有" and self.ticke_peoples_num > ticket_num:
                                            if self.session.is_more_ticket:
                                                print(u"余票数小于乘车人数，当前余票数: {}, 删减人车人数到: {}".format(ticket_num, ticket_num))
                                                is_more_ticket_num = ticket_num
                                            else:
                                                continue
                                        else:
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
                                            "status": True,
                                        }
                else:
                    print u"车次配置信息有误，或者返回数据异常，请检查 {}".format(station_ticket)
        return {"code": ticket.FAIL_CODE, "status": False}


if __name__ == "__main__":
    q = query()
