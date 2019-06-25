import time

import requests
#from config.ticketConf import _get_yaml
from config.urlConf import urls
from myUrllib.httpUtils import HTTPClient


def sendServerChan(msg):
    
        try:
            sendPushBearUrls = urls.get("ServerChan")
            data = {
                "text": "自定义购票成功通知测试版本",
                "desp": msg
            }
            httpClint = HTTPClient(0)
            sendPushBeaRsp = httpClint.send(sendPushBearUrls, data=data)
            if sendPushBeaRsp.get("code") is 0:
                print(u"已下发 serverChan 微信通知, 请查收")
            else:
                print(sendPushBeaRsp)
        except Exception as e:
            print(u"serverChan 配置有误 {}".format(e))
        pass


if __name__ == '__main__':
    sendServerChan(1)