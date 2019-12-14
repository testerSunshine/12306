# coding=utf-8
import datetime
import time

from inter.CheckRandCodeAnsyn import checkRandCodeAnsyn
from inter.GetPassengerDTOs import getPassengerDTOs
from inter.GetRandCode import getRandCode
from inter.QueryOrderWaitTime import queryOrderWaitTime


class confirmSingleForQueue:
    def __init__(self, session, ifShowPassCodeTime, is_node_code, token, set_type, ticket_peoples, ticketInfoForPassengerForm,
                 oldPassengerStr, passengerTicketStrList):
        self.session = session
        self.ifShowPassCodeTime = ifShowPassCodeTime
        self.is_node_code = is_node_code
        self.token = token
        self.set_type = set_type
        self.ticket_peoples = ticket_peoples
        self.ticketInfoForPassengerForm = ticketInfoForPassengerForm
        self.passengerTicketStrList = passengerTicketStrList
        self.oldPassengerStr = oldPassengerStr

    def data_par(self):
        """
        模拟提交订单是确认按钮，参数获取方法还是get_ticketInfoForPassengerForm 中获取
        :return:
        """
        if not self.passengerTicketStrList and not self.oldPassengerStr:
            s = getPassengerDTOs(session=self.session, ticket_peoples=self.ticket_peoples, set_type=self.set_type)
            getPassengerDTOsResult = s.getPassengerTicketStrListAndOldPassengerStr()
            if getPassengerDTOsResult.get("status", False):
                self.passengerTicketStrList = getPassengerDTOsResult.get("passengerTicketStrList", "")
                self.oldPassengerStr = getPassengerDTOsResult.get("oldPassengerStr", "")
        data = {
            "passengerTicketStr": self.passengerTicketStrList.rstrip("_{0}".format(self.set_type)),
            "oldPassengerStr": "".join(self.oldPassengerStr),
            "purpose_codes": self.ticketInfoForPassengerForm["purpose_codes"],
            "key_check_isChange": self.ticketInfoForPassengerForm["key_check_isChange"],
            "leftTicketStr": self.ticketInfoForPassengerForm["leftTicketStr"],
            "train_location": self.ticketInfoForPassengerForm["train_location"],
            "seatDetailType": "",  # 开始需要选择座位，但是目前12306不支持自动选择作为，那这个参数为默认
            "roomType": "00",  # 好像是根据一个id来判断选中的，两种 第一种是00，第二种是10，但是我在12306的页面没找到该id，目前写死是00，不知道会出什么错
            "dwAll": "N",
            "whatsSelect": 1,
            "_json_at": "",
            "randCode": "",
            "choose_seats": "",
            "REPEAT_SUBMIT_TOKEN": self.token,
        }
        return data

    def sendConfirmSingleForQueue(self):
        """
        # 模拟查询当前的列车排队人数的方法
        # 返回信息组成的提示字符串
        :return:
        """
        data = self.data_par()
        checkQueueOrderUrl = self.session.urls["checkQueueOrderUrl"]
        try:
            if self.is_node_code:
                print(u"正在使用自动识别验证码功能")
                for i in range(3):
                    randCode = getRandCode(is_auto_code=True, auto_code_type=2)
                    checkcode = checkRandCodeAnsyn(self.session, randCode, self.token)
                    if checkcode == 'TRUE':
                        print(u"验证码通过,正在提交订单")
                        data['randCode'] = randCode
                        break
                    else:
                        print (u"验证码有误, {0}次尝试重试".format(i + 1))
                print(u"验证码超过限定次数3次，放弃此次订票机会!")
            else:
                print(u"不需要验证码")
            time.sleep(self.ifShowPassCodeTime)
            checkQueueOrderResult = self.session.httpClint.send(checkQueueOrderUrl, data)
            if "status" in checkQueueOrderResult and checkQueueOrderResult["status"]:
                c_data = checkQueueOrderResult["data"] if "data" in checkQueueOrderResult else {}
                if 'submitStatus' in c_data and c_data['submitStatus'] is True:
                    qow = queryOrderWaitTime(self.session)
                    qow.sendQueryOrderWaitTime()
                else:
                    if 'errMsg' in c_data and c_data['errMsg']:
                        print(u"提交订单失败，{0}".format(c_data['errMsg']))
                    else:
                        print(c_data)
                        print(u'订票失败!很抱歉,请重试提交预订功能!')
            elif "messages" in checkQueueOrderResult and checkQueueOrderResult["messages"]:
                print(u"提交订单失败,错误信息: " + checkQueueOrderResult["messages"])
            else:
                print(u"提交订单中，请耐心等待：" + checkQueueOrderResult["message"])
        except ValueError:
            print(u"接口 {} 无响应".format(checkQueueOrderUrl))