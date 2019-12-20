# coding=utf-8
import base64
import threading
import unittest
from collections import OrderedDict

import requests

import TickerConfig
from agency.agency_tools import proxy
from config.emailConf import sendEmail
from config.serverchanConf import sendServerChan
from inter.LiftTicketInit import liftTicketInit


def _set_header_default():
    header_dict = OrderedDict()
    header_dict["Accept"] = "*/*"
    header_dict["Accept-Encoding"] = "gzip, deflate"
    header_dict["X-Requested-With"] = "superagent"

    header_dict[
        "User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    header_dict["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"


class testAll(unittest.TestCase):
    def testProxy(self):
        """
        测试代理是否可用
        :return:
        """
        _proxy = proxy()
        proxie = _proxy.setProxy()
        url = "http://httpbin.org/ip"
        rsp = requests.get(url, proxies=proxie, timeout=5, headers=_set_header_default()).content
        print(u"当前代理ip地址为: {}".format(rsp))

    def testEmail(self):
        """
        实测邮箱是否可用
        :return:
        """
        sendEmail(u"订票小助手测试一下")

    # def testConfig(self):
    #     """
    #     测试config是否配置正确
    #     :return:
    #     """

    def testServerChan(self):
        """
        实测server酱是否可用
        :return:
        """
        sendServerChan(u"server酱 微信通知测试一下")

    def testUserAgent(self):
        """
        测试UserAgent
        :return:
        """
        from fake_useragent import UserAgent
        for i in range(10000):
            ua = UserAgent(verify_ssl=False)
            print(ua.random)

    def testVerfyImage(self):
        """
        测试模型加载识别
        :return:
        """
        from verify.localVerifyCode import Verify
        v = Verify()
        with open('../tkcode.png', 'rb') as f:
            base64Image = base64.b64encode(f.read())
            for i in range(5):
                t = threading.Thread(target=v.verify, args=(base64Image,))
                t.start()

    def testRemoteVerfy(self):
        """
        测试打码是否可用
        :return:
        """
        import requests
        import time
        while True:
            try:
                starttime = time.time()
                rsp = requests.post(url="http://120.77.154.140:8000/verify/base64/",
                                    data={
                                        'imageFile': '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'},
                                    timeout=60,
                                    )
                print(rsp.content)
                print(f"响应时间{time.time()-starttime}m")
            except:
                pass

    def testCdn(self):
        """
        测试cdn筛选
        :return:
        """
        cdn = ["60.9.0.19", "60.9.0.20", "113.16.212.251", "36.250.248.27"]
        from inter.LiftTicketInit import liftTicketInit
        from init.select_ticket_info import select
        from config.getCookie import getDrvicesID

        s = select()
        s.httpClint.cdn = cdn[3]
        getDrvicesID(s)
        liftTicketInit(s).reqLiftTicketInit()


if __name__ == '__main__':
    unittest.main()
