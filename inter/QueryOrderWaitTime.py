# coding=utf-8
import copy
import time

from config.TicketEnmu import ticket
from config.emailConf import sendEmail
from config.serverchanConf import sendServerChan
from myException.ticketIsExitsException import ticketIsExitsException
from myException.ticketNumOutException import ticketNumOutException


class queryOrderWaitTime:
    """
    排队
    """

    def __init__(self, session):
        self.session = session

    def sendQueryOrderWaitTime(self):
        """
        排队获取订单等待信息,每隔3秒请求一次，最高请求次数为20次！
        :return:
        """
        num = 1
        while True:
            num += 1
            if num > ticket.OUT_NUM:
                print(ticket.WAIT_OUT_NUM)
                order_id = self.queryMyOrderNoComplete()  # 排队失败，自动取消排队订单
                if order_id:
                    self.cancelNoCompleteMyOrder(order_id)
                break
            try:
                queryOrderWaitTimeUrl = copy.deepcopy(self.session.urls["queryOrderWaitTimeUrl"])
                queryOrderWaitTimeUrl["req_url"] = queryOrderWaitTimeUrl["req_url"].format(int(round(time.time() * 1000)))
                queryOrderWaitTimeResult = self.session.httpClint.send(queryOrderWaitTimeUrl)
            except ValueError:
                queryOrderWaitTimeResult = {}
            if queryOrderWaitTimeResult:
                if queryOrderWaitTimeResult.get("status", False):
                    data = queryOrderWaitTimeResult.get("data", False)
                    if data and data.get("orderId", ""):
                        sendEmail(ticket.WAIT_ORDER_SUCCESS.format(
                            data.get("orderId", "")))
                        sendServerChan(ticket.WAIT_ORDER_SUCCESS.format(
                            data.get("orderId", "")))
                        raise ticketIsExitsException(ticket.WAIT_ORDER_SUCCESS.format(
                            data.get("orderId")))
                    elif data.get("msg", False):
                        print(data.get("msg", ""))
                        break
                    elif data.get("waitTime", False):
                        print(ticket.WAIT_ORDER_CONTINUE.format(0 - data.get("waitTime", False)))
                    else:
                        pass
                elif queryOrderWaitTimeResult.get("messages", False):
                    print(ticket.WAIT_ORDER_FAIL.format(queryOrderWaitTimeResult.get("messages", "")))
                else:
                    print(ticket.WAIT_ORDER_NUM.format(num + 1))
            else:
                pass
            time.sleep(2)
        else:
            print(ticketNumOutException(ticket.WAIT_ORDER_SUB_FAIL))

    def queryMyOrderNoComplete(self):
        """
        获取订单列表信息
        :return:
        """
        self.initNoComplete()
        queryMyOrderNoCompleteUrl = self.session.urls["queryMyOrderNoCompleteUrl"]
        data = {"_json_att": ""}
        try:
            queryMyOrderNoCompleteResult = self.session.httpClint.send(queryMyOrderNoCompleteUrl, data)
        except ValueError:
            queryMyOrderNoCompleteResult = {}
        if queryMyOrderNoCompleteResult:
            if queryMyOrderNoCompleteResult.get("data", False) and queryMyOrderNoCompleteResult["data"].get("orderDBList", False):
                return queryMyOrderNoCompleteResult["data"]
            elif queryMyOrderNoCompleteResult.get("data", False) and queryMyOrderNoCompleteResult["data"].get("orderCacheDTO", False):
                if queryMyOrderNoCompleteResult["data"]["orderCacheDTO"].get("message", False):
                    print(queryMyOrderNoCompleteResult["data"]["orderCacheDTO"]["message"]["message"])
                    raise ticketNumOutException(
                        queryMyOrderNoCompleteResult["data"]["orderCacheDTO"]["message"]["message"])
            else:
                if queryMyOrderNoCompleteResult.get("message", False):
                    print(queryMyOrderNoCompleteResult.get("message", False))
                    return False
                else:
                    return False
        else:
            return False

    def initNoComplete(self):
        """
        获取订单前需要进入订单列表页，获取订单列表页session
        :return:
        """
        initNoCompleteUrl = self.session.urls["initNoCompleteUrl"]
        data = {"_json_att": ""}
        self.session.httpClint.send(initNoCompleteUrl, data)

    def cancelNoCompleteMyOrder(self, sequence_no):
        """
        取消订单
        :param sequence_no: 订单编号
        :return:
        """
        cancelNoCompleteMyOrderUrl = self.session.urls["cancelNoCompleteMyOrder"]
        cancelNoCompleteMyOrderData = {
            "sequence_no": sequence_no,
            "cancel_flag": "cancel_order",
            "_json_att": ""
        }
        cancelNoCompleteMyOrderResult = self.session.httpClint.send(cancelNoCompleteMyOrderUrl,
                                                                    cancelNoCompleteMyOrderData)
        if cancelNoCompleteMyOrderResult.get("data", False) and cancelNoCompleteMyOrderResult["data"].get("existError", "N"):
            print(ticket.CANCEL_ORDER_SUCCESS.format(sequence_no))
            time.sleep(2)
            return True
        else:
            print(ticket.CANCEL_ORDER_FAIL.format(sequence_no))
            return False
