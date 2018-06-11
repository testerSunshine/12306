# coding=utf-8
import urllib
from collections import OrderedDict

from config.TicketEnmu import ticket


class autoSubmitOrderRequest:
    """
    快读提交订单通道
    """
    def __init__(self, session,
                 secretStr,
                 train_date,
                 query_from_station_name,
                 query_to_station_name,
                 passengerTicketStr,
                 oldPassengerStr):
        self.secretStr = urllib.unquote(secretStr)
        self.train_date = train_date
        self.query_from_station_name = query_from_station_name
        self.query_to_station_name = query_to_station_name
        self.passengerTicketStr = passengerTicketStr
        self.oldPassengerStr = oldPassengerStr
        self.session = session

    def data_par(self):
        """
        参数结构
        自动提交代码接口-autoSubmitOrderRequest
            - 字段说明
                - secretStr 车票代码
                - train_date 乘车日期
                - tour_flag 乘车类型
                - purpose_codes 学生还是成人
                - query_from_station_name 起始车站
                - query_to_station_name 结束车站
                - cancel_flag 默认2，我也不知道干嘛的
                - bed_level_order_num  000000000000000000000000000000
                - passengerTicketStr   乘客乘车代码
                - oldPassengerStr  乘客编号代码
        :return:
        """
        data = OrderedDict()
        data["secretStr"] = self.secretStr
        data["train_date"] = self.train_date
        data["tour_flag"] = "dc"
        data["purpose_codes"] = "ADULT"
        data["query_from_station_name"] = self.query_from_station_name
        data["query_to_station_name"] = self.query_to_station_name
        data["cancel_flag"] = 2
        data["bed_level_order_num"] = "000000000000000000000000000000"
        data["passengerTicketStr"] = self.passengerTicketStr
        data["oldPassengerStr"] = self.oldPassengerStr
        return data

    def sendAutoSubmitOrderRequest(self):
        """
        请求下单接口
        :return:
        """
        urls = self.session.urls["autoSubmitOrderRequest"]
        data = self.data_par()
        autoSubmitOrderRequestResult = self.session.httpClint.send(urls, data)
        if autoSubmitOrderRequestResult and \
                autoSubmitOrderRequestResult.get("status", False) and\
                autoSubmitOrderRequestResult.get("httpstatus", False) == 200:
            requestResultData = autoSubmitOrderRequestResult.get("data", {})
            if requestResultData:
                result = requestResultData.get("result", "")
                ifShowPassCode = requestResultData.get("ifShowPassCode", "N")
                print(ticket.AUTO_SUBMIT_ORDER_REQUEST_C)
                if ifShowPassCode == "Y":  # 如果需要验证码
                    print(ticket.AUTO_SUBMIT_NEED_CODE)
                    return {
                        "result": result,
                        "ifShowPassCode": ifShowPassCode,
                        "code": ticket.SUCCESS_CODE,
                        "ifShowPassCodeTime": requestResultData.get("requestResultData", 2000) / float(1000),
                        "status": True,
                    }
                else:
                    print(ticket.AUTO_SUBMIT_NOT_NEED_CODE)
                    return {
                        "result": result,
                        "ifShowPassCode": ifShowPassCode,
                        "code": ticket.SUCCESS_CODE,
                        "ifShowPassCodeTime": requestResultData.get("requestResultData", 2000) / float(1000),
                        "status": True,
                    }
        else:
            print(ticket.AUTO_SUBMIT_ORDER_REQUEST_F)
            if autoSubmitOrderRequestResult.get("messages", ""):
                print(autoSubmitOrderRequestResult.get("messages", ""))
                return {
                    "code": ticket.FAIL_CODE,
                    "status": False,
                }
            elif autoSubmitOrderRequestResult.get("validateMessages", ""):
                print(autoSubmitOrderRequestResult.get("validateMessages", ""))
                return {
                    "code": ticket.FAIL_CODE,
                    "status": False,
                }




