# -*- coding: utf8 -*-
import TickerConfig
from config.urlConf import urls
from myUrllib.httpUtils import HTTPClient

PUSH_BEAR_API_PATH = "https://pushbear.ftqq.com/sub"


def sendPushBear(msg):
    """
    pushBear微信通知
    :param str: 通知内容 content
    :return:
    """
    if TickerConfig.PUSHBEAR_CONF["is_pushbear"] and TickerConfig.PUSHBEAR_CONF["send_key"].strip() != "":
        try:
            sendPushBearUrls = urls.get("Pushbear")
            data = {
                "sendkey": TickerConfig.PUSHBEAR_CONF["send_key"].strip(),
                "text": "易行购票成功通知",
                "desp": msg
            }
            httpClint = HTTPClient(0)
            sendPushBeaRsp = httpClint.send(sendPushBearUrls, data=data)
            if sendPushBeaRsp.get("code") is 0:
                print(u"已下发 pushbear 微信通知, 请查收")
            else:
                print(sendPushBeaRsp)
        except Exception as e:
            print(u"pushbear 配置有误 {}".format(e))
    else:
        pass


if __name__ == '__main__':
    sendPushBear(1)
