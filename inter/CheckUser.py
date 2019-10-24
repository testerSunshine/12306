# coding=utf-8
import datetime
import random
import time
import wrapcache
from config import configCommon
from config.TicketEnmu import ticket


class checkUser:
    def __init__(self, session):
        self.session = session

    def sendCheckUser(self):
        """
        检查用户登录, 检查间隔为2分钟
        :return:
        """
        CHENK_TIME = 1
        while 1:
            time.sleep(3)  # 防止cpu占用过高
            configCommon.checkSleepTime(self.session)  # 修复晚上查询线程休眠时，检查登录线程为休眠，造成快豆迅速消耗
            if wrapcache.get("user_time") is None:
                check_user_url = self.session.urls["check_user_url"]
                data = {"_json_att": ""}
                check_user = self.session.httpClint.send(check_user_url, data)
                if check_user.get("data", False):
                    check_user_flag = check_user["data"]["flag"]
                    if check_user_flag is True:
                       wrapcache.set("user_time", datetime.datetime.now(), timeout=random.randint(60, 80) * CHENK_TIME)
                    else:
                        if check_user['messages']:
                            print(ticket.LOGIN_SESSION_FAIL.format(check_user['messages']))
                            self.session.call_login()
                            wrapcache.set("user_time", datetime.datetime.now(), timeout=random.randint(60, 80) * CHENK_TIME)
                        else:
                            print(ticket.LOGIN_SESSION_FAIL.format(check_user['messages']))
                            self.session.call_login()
                            wrapcache.set("user_time", datetime.datetime.now(), timeout=random.randint(60, 80) * CHENK_TIME)
