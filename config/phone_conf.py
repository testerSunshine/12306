# -*- coding: utf8 -*-
__author__ = 'Song'

import urllib2
from config.ticketConf import _get_yaml
from config.TicketEnmu import ticket

def send_request(url):
    if not url:
        return 'error'
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.151 Safari/534.16')
    try:
        response = urllib2.urlopen(req, timeout=3)
    except Exception as e:
        return e
    result = response.read()
    return result


def sendPhone(order_id):
    """
    短信通知
    :param order_id: 订单号
    :return:
    """
    phone_conf = _get_yaml()
    is_phone = phone_conf['phone_conf']['is_phone']
    if is_phone:
        try:
            SEND_PHONE_MESSAGE_URL = phone_conf["phone_conf"]["SEND_PHONE_MESSAGE_URL"]
            OperID = phone_conf["phone_conf"]["OperID"]
            OperPass = phone_conf['phone_conf']['OperPass']
            phone = phone_conf['phone_conf']['phone']
            message = ticket.WAIT_ORDER_SUCCESS.format(order_id)
            url = SEND_PHONE_MESSAGE_URL % (OperID,OperPass,phone,message)
            url = url.encode('gb2312')
            send_request(urllib2.quote(url, safe="%/:=&?~#+!$,;'@()*[]"))
            print(u"短信已发送, 请查收")
        except Exception as e:
            print(u"短信配置有误{}".format(e))
    else:
        pass


if __name__ == '__main__':
    sendPhone('92kejce')