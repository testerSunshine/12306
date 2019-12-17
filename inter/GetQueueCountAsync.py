import TickerConfig

[]# coding=utf-8
import datetime
import sys
import time
from collections import OrderedDict

import wrapcache

from inter.ConfirmSingleForQueueAsys import confirmSingleForQueueAsys


class getQueueCountAsync:
    """
    排队
    """
    def __init__(self,
                 session,
                 train_no,
                 stationTrainCode,
                 fromStationTelecode,
                 toStationTelecode,
                 leftTicket,
                 set_type,
                 users,
                 station_dates,
                 passengerTicketStr,
                 oldPassengerStr,
                 result,
                 ifShowPassCodeTime):
        self.train_no = train_no
        self.session = session
        self.stationTrainCode = stationTrainCode
        self.fromStationTelecode = fromStationTelecode
        self.toStationTelecode = toStationTelecode
        self.set_type = set_type
        self.leftTicket = leftTicket
        self.users = users
        self.station_dates = station_dates
        self.passengerTicketStr = passengerTicketStr
        self.oldPassengerStr = oldPassengerStr
        self.result = result
        self.ifShowPassCodeTime=ifShowPassCodeTime

    def data_par(self):
        """
         - 字段说明
            - train_date 时间
            - train_no 列车编号,查询代码里面返回
            - stationTrainCode 列车编号
            - seatType 对应坐席
            - fromStationTelecode 起始城市
            - toStationTelecode 到达城市
            - leftTicket 查询代码里面返回
            - purpose_codes 学生还是成人
            - _json_att 没啥卵用，还是带上吧
        :return:
        """
        if sys.version_info.major is 2:
            new_train_date = filter(None, str(time.asctime(time.strptime(self.station_dates, "%Y-%m-%d"))).split(" "))
        else:
            new_train_date = list(filter(None, str(time.asctime(time.strptime(self.station_dates, "%Y-%m-%d"))).split(" ")))
        data = OrderedDict()
        data['train_date'] = "{0} {1} {2} {3} 00:00:00 GMT+0800 (中国标准时间)".format(
            new_train_date[0],
            new_train_date[1],
            new_train_date[2] if len(new_train_date[2]) is 2 else f"0{new_train_date[2]}",
            new_train_date[4],
            time.strftime("%H:%M:%S", time.localtime(time.time()))
        ),
        data["train_no"] = self.train_no
        data["stationTrainCode"] = self.stationTrainCode
        data["seatType"] = self.set_type
        data["fromStationTelecode"] = self.fromStationTelecode
        data["toStationTelecode"] = self.toStationTelecode
        data["leftTicket"] = self.leftTicket
        data["purpose_codes"] = "ADULT"
        data["_json_att"] = ""
        return data

    def conversion_int(self, str):
        return int(str)

    def sendGetQueueCountAsync(self):
        """
        请求排队接口
        :return:
        """
        urls = self.session.urls["getQueueCountAsync"]
        data = self.data_par()
        getQueueCountAsyncResult = self.session.httpClint.send(urls, data)
        if getQueueCountAsyncResult.get("status", False) and getQueueCountAsyncResult.get("data", False):
            if "status" in getQueueCountAsyncResult and getQueueCountAsyncResult["status"] is True:
                if "countT" in getQueueCountAsyncResult["data"]:
                    ticket_data = getQueueCountAsyncResult["data"]["ticket"]
                    ticket_split = sum(map(self.conversion_int, ticket_data.split(","))) if ticket_data.find(
                        ",") != -1 else ticket_data
                    if int(ticket_split) is 0:
                        # 增加余票数为0时，将车次加入小黑屋
                        wrapcache.set(key=self.train_no, value=datetime.datetime.now(),
                                      timeout=TickerConfig.TICKET_BLACK_LIST_TIME * 60)
                        print(f"排队失败，当前余票数为{ticket_split}张")
                        return
                    print(u"排队成功, 当前余票还剩余: {0} 张".format(ticket_split))
                    c = confirmSingleForQueueAsys(session=self.session,
                                                  passengerTicketStr=self.passengerTicketStr,
                                                  oldPassengerStr=self.oldPassengerStr,
                                                  result=self.result,)
                    print(u"验证码提交安全期，等待{}MS".format(self.ifShowPassCodeTime))
                    time.sleep(self.ifShowPassCodeTime)
                    c.sendConfirmSingleForQueueAsys()
                else:
                    print(u"排队发现未知错误{0}，将此列车 {1}加入小黑屋".format(getQueueCountAsyncResult, self.train_no))
                    wrapcache.set(key=self.train_no, value=datetime.datetime.now(),
                                  timeout=TickerConfig.TICKET_BLACK_LIST_TIME * 60)
            elif "messages" in getQueueCountAsyncResult and getQueueCountAsyncResult["messages"]:
                print(u"排队异常，错误信息：{0}, 将此列车 {1}加入小黑屋".format(getQueueCountAsyncResult["messages"][0], self.train_no))
                wrapcache.set(key=self.train_no, value=datetime.datetime.now(),
                              timeout=TickerConfig.TICKET_BLACK_LIST_TIME * 60)
            else:
                if "validateMessages" in getQueueCountAsyncResult and getQueueCountAsyncResult["validateMessages"]:
                    print(str(getQueueCountAsyncResult["validateMessages"]))



