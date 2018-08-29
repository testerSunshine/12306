# coding=utf-8
import json
import urllib
from collections import OrderedDict

from inter.QueryOrderWaitTime import queryOrderWaitTime


class confirmSingleForQueueAsys:
    """
    订单快读排队
    """
    def __init__(self,
                 session,
                 passengerTicketStr,
                 oldPassengerStr,
                 result,
                 randCode="",
                 ):
        self.session = session
        self.passengerTicketStr = passengerTicketStr
        self.oldPassengerStr = oldPassengerStr
        self.result = result if isinstance(result, str) else str(result)
        self.randCode = randCode

    def data_par(self):
        """
        字段说明
            passengerTicketStr 乘客乘车代码
            oldPassengerStr 乘客编号代码
            randCode 填空
            purpose_codes 学生还是成人
            key_check_isChange autoSubmitOrderRequest返回的result字段做切割即可
            leftTicketStr autoSubmitOrderRequest返回的result字段做切割即可
            train_location autoSubmitOrderRequest返回的result字段做切割即可
            choose_seats
            seatDetailType
            _json_att
        :return:
        """
        results = self.result.split("#")
        key_check_isChange = results[1]
        leftTicketStr = results[2]
        train_location = results[0]
        data = OrderedDict()
        data["passengerTicketStr"] = self.passengerTicketStr
        data["oldPassengerStr"] = self.oldPassengerStr
        data["randCode"] = self.randCode
        data["purpose_codes"] = "ADULT"
        data["key_check_isChange"] = key_check_isChange
        data["leftTicketStr"] = leftTicketStr
        data["train_location"] = train_location
        data["choose_seats"] = ""
        data["seatDetailType"] = ""
        data["_json_att"] = ""
        return data

    def sendConfirmSingleForQueueAsys(self):
        """
        请求订单快读排队接口
        :return:
        """
        urls = self.session.urls["confirmSingleForQueueAsys"]
        data = self.data_par()
        confirmSingleForQueueAsysResult = self.session.httpClint.send(urls, data)
        if confirmSingleForQueueAsysResult.get("status", False) and confirmSingleForQueueAsysResult.get("data", False):
            queueData = confirmSingleForQueueAsysResult.get("data", {})
            if queueData.get("submitStatus", False):
                qwt = queryOrderWaitTime(session=self.session)
                qwt.sendQueryOrderWaitTime()
            else:
                print(queueData.get("errMsg", ""))
