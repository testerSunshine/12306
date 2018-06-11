# coding=utf-8
import copy
import datetime
import random
import time

from config.TicketEnmu import ticket


class query:
    """
    查询接口
    """

    def __init__(self, session, from_station, to_station, from_station_h, to_station_h, _station_seat, station_trains,
                 black_train_no, station_dates=None, ):
        self.session = session
        self.from_station = from_station
        self.to_station = to_station
        self.from_station_h = from_station_h
        self.to_station_h = to_station_h
        self.station_trains = station_trains
        self._station_seat = _station_seat if isinstance(_station_seat, list) else list(_station_seat)
        self.station_dates = station_dates if isinstance(station_dates, list) else list(station_dates)
        self.ticket_black_list = dict()
        self.black_train_no = black_train_no

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
        if self.black_train_no:
            self.ticket_black_list[self.black_train_no] = datetime.datetime.now()
        for station_date in self.station_dates:
            select_url = copy.copy(self.session.urls["select_url"])
            select_url["req_url"] = select_url["req_url"].format(
                station_date, self.from_station, self.to_station)
            station_ticket = self.session.httpClint.send(select_url)
            value = station_ticket.get("data", "")
            if not value:
                print (u'{0}-{1} 车次坐席查询为空'.format(self.from_station, self.to_station))
            else:
                result = value.get('result', [])
                if result:
                    for i in value['result']:
                        ticket_info = i.split('|')
                        if ticket_info[11] == "Y" and ticket_info[1].encode("utf8") == "预订":  # 筛选未在开始时间内的车次
                            for j in xrange(len(self._station_seat)):
                                is_ticket_pass = ticket_info[self.station_seat(self._station_seat[j].encode("utf8"))]
                                if is_ticket_pass != '' and is_ticket_pass != '无' and ticket_info[
                                    3] in self.station_trains and is_ticket_pass != '*':  # 过滤有效目标车次
                                    secretStr = ticket_info[0]
                                    train_no = ticket_info[2]
                                    query_from_station_name = ticket_info[6]
                                    query_to_station_name = ticket_info[7]
                                    train_location = ticket_info[15]
                                    stationTrainCode = ticket_info[3]
                                    train_date = station_date
                                    leftTicket = ticket_info[12]
                                    set_type = self._station_seat[j]
                                    print (u'车次: {0} 始发车站: {1} 终点站: {2} {3}: {4}'.format(train_no,
                                                                                         self.from_station_h,
                                                                                         self.to_station_h,
                                                                                         self._station_seat[j].encode(
                                                                                             "utf8"),
                                                                                         ticket_info[self.station_seat(
                                                                                             self._station_seat[
                                                                                                 j].encode("utf8"))]
                                                                                         ))
                                    if "train_no" in self.ticket_black_list and (
                                            datetime.datetime.now() - self.ticket_black_list[
                                        train_no]).seconds / 60 < int(ticket.TICKET_BLACK_LIST_TIME):
                                        print(ticket.QUERY_IN_BLACK_LIST.format(train_no))
                                        break
                                    else:
                                        print (ticket.QUERY_C)
                                        # self.buy_ticket_time = datetime.datetime.now()
                                        return {
                                            "secretStr": secretStr,
                                            "train_no": train_no,
                                            "stationTrainCode": stationTrainCode,
                                            "train_date": train_date,
                                            "query_from_station_name": query_from_station_name,
                                            "query_to_station_name": query_to_station_name,
                                            # "buy_ticket_time": self.buy_ticket_time,
                                            "set_type": set_type,
                                            "leftTicket": leftTicket,
                                            "train_location": train_location,
                                            "code": ticket.SUCCESS_CODE,
                                            "status": True,
                                        }
                                else:
                                    pass
                        else:
                            pass
                else:
                    print u"车次配置信息有误，或者返回数据异常，请检查 {}".format(station_ticket)
        return {"code": ticket.FAIL_CODE, "status": False}


if __name__ == "__main__":
    q = query()
