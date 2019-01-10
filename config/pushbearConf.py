# -*- coding: utf8 -*-
__author__ = 'kongkongyzt'
import requests
from config.ticketConf import _get_yaml

PUSH_BEAR_API_PATH = "https://pushbear.ftqq.com/sub"

def sendPushBear(msg):
    """
    pushBear微信通知
    :param str: 通知内容 content
    :return:
    """
    conf = _get_yaml()
    if conf["pushbear_conf"]["is_pushbear"] and conf["pushbear_conf"]["send_key"].strip() != "":
        try:
            requests.get("{}?sendkey={}&text=来自12306抢票助手的通知&desp={}".format(PUSH_BEAR_API_PATH, conf["pushbear_conf"]["send_key"].strip(), msg))
            print(u"已下发 pushbear 微信通知, 请查收")
        except Exception as e:
            print(u"pushbear 配置有误 {}".format(e))
    else:
        pass


if __name__ == '__main__':
    sendPushBear(1)