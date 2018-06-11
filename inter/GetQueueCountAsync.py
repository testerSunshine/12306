# coding=utf-8
import time
from collections import OrderedDict

from config.TicketEnmu import ticket


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
                 users,):
        self.train_no = train_no
        self.session = session
        self.stationTrainCode = stationTrainCode
        self.fromStationTelecode = fromStationTelecode
        self.toStationTelecode = toStationTelecode
        self.set_type = set_type
        self.leftTicket = leftTicket
        self.users = users

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
        l_time = time.localtime(time.time())
        new_train_date = time.strftime("%b %d %Y %H:%M:%S", l_time)
        data = OrderedDict()
        # data["train_date"] = "Fri " + str(new_train_date) + " GMT+0800 (CST)"
        data["train_date"] = "Fri Jun 21 2018 18:23:54 GMT+0800 (CST)"
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
                    countT = getQueueCountAsyncResult["data"]["countT"]
                    if int(countT) is 0:
                        if int(ticket_split) < self.users:
                            print(ticket.QUEUE_TICKET_SHORT)
                            return {"status": False, "is_black": False}
                        else:
                            print(ticket.QUEUE_TICKET_SUCCESS.format(ticket_split))
                            return {"status": True, "is_black": False}
                    else:
                        return {"status": False, "is_black": True}
                else:
                    print(ticket.QUEUE_JOIN_BLACK.format(getQueueCountAsyncResult, self.train_no))
                    return {"status": False, "is_black": True, "train_no": self.train_no}
            elif "messages" in getQueueCountAsyncResult and getQueueCountAsyncResult["messages"]:
                print(ticket.QUEUE_WARNING_MSG.format(getQueueCountAsyncResult["messages"][0], self.train_no))
                return {"status": False, "is_black": True, "train_no": self.train_no}
            else:
                if "validateMessages" in getQueueCountAsyncResult and getQueueCountAsyncResult["validateMessages"]:
                    print(str(getQueueCountAsyncResult["validateMessages"]))
                    return {"status": False, "is_black": False}
                else:
                    return {"status": False, "is_black": False}
        else:
            return {"status": False, "is_black": False}



