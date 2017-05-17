# -*- coding=utf-8 -*-
from init import login, select_ticket_info


def run():
    login.main()
    select_ticket_info.select('上海', '长沙').main()

run()