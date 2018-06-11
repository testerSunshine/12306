# coding=utf-8


class liftTicketInit:
    def __init__(self, session):
        self.session = session

    def reqLiftTicketInit(self):
        """
        请求抢票页面
        :return:
        """
        urls = self.session.urls["left_ticket_init"]
        self.session.httpClint.send(urls)
        return {
            "status": True
        }