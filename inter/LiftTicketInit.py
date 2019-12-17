# coding=utf-8
import re


class liftTicketInit:
    def __init__(self, session):
        self.session = session

    def reqLiftTicketInit(self):
        """
        请求抢票页面
        :return:
        """
        urls = self.session.urls["left_ticket_init"]
        # 获取初始化的结果
        result = self.session.httpClint.send(urls)
        # 用正则表达式查出CLeftTicketUrl的值
        matchObj = re.search('var CLeftTicketUrl = \'(.*)\'', result, re.M|re.I);
        if matchObj:
            # 如果有值，替换queryUrl
            self.session.queryUrl = matchObj.group(1)
        return {
            "status": True
        }
