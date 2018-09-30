# coding=utf-8
import datetime
import wrapcache

from config.TicketEnmu import ticket


class checkUser:
    def __init__(self, session):
        self.session = session

    def sendCheckUser(self):
        """
        检查用户登录, 检查间隔为2分钟
        :return:
        """
        CHENK_TIME = 2
        if wrapcache.get("user_time") is None:
            check_user_url = self.session.urls["check_user_url"]
            data = {"_json_att": ""}
            check_user = self.session.httpClint.send(check_user_url, data)
            if check_user.get("data", False):
                check_user_flag = check_user["data"]["flag"]
                if check_user_flag is True:
                    wrapcache.set("user_time", datetime.datetime.now(), timeout=60 * CHENK_TIME)
                else:
                    if check_user['messages']:
                        print (ticket.LOGIN_SESSION_FAIL.format(check_user['messages']))
                        self.session.call_login()
                        wrapcache.set("user_time", datetime.datetime.now(), timeout=60 * CHENK_TIME)
                    else:
                        print (ticket.LOGIN_SESSION_FAIL.format(check_user['messages']))
                        self.session.call_login()
                        wrapcache.set("user_time", datetime.datetime.now(), timeout=60 * CHENK_TIME)