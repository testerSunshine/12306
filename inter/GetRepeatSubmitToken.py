# coding=utf-8
import json
import re


class getRepeatSubmitToken:
    def __init__(self, session):
        self.session = session

    def sendGetRepeatSubmitToken(self):
        """
        获取提交车票请求token
        :return: token
        """
        initdc_url = self.session.urls["initdc_url"]
        initdc_result = self.session.httpClint.send(initdc_url, )
        token_name = re.compile(r"var globalRepeatSubmitToken = '(\S+)'")
        ticketInfoForPassengerForm_name = re.compile(r'var ticketInfoForPassengerForm=(\{.+\})?')
        order_request_params_name = re.compile(r'var orderRequestDTO=(\{.+\})?')
        token = re.search(token_name, initdc_result).group(1)
        re_tfpf = re.findall(ticketInfoForPassengerForm_name, initdc_result)
        re_orp = re.findall(order_request_params_name, initdc_result)
        if re_tfpf:
            ticketInfoForPassengerForm = json.loads(re_tfpf[0].replace("'", '"'))
        else:
            ticketInfoForPassengerForm = ""
        if re_orp:
            order_request_params = json.loads(re_orp[0].replace("'", '"'))
        else:
            order_request_params = ""
        return {
            "token": token,
            "ticketInfoForPassengerForm": ticketInfoForPassengerForm,
            "order_request_params": order_request_params,
            "session": self.session
        }