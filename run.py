# -*- coding=utf-8 -*-
from init import login, select_ticket_info, SelectTicketInfoFast


def run():
    # login.main()
    SelectTicketInfoFast.selectFast().main()
    # select_ticket_info.select().main()


if __name__ == '__main__':
    run()