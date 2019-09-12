# coding=utf-8
import unittest
from collections import OrderedDict

import requests

from agency.agency_tools import proxy
from config.emailConf import sendEmail
from config.serverchanConf import sendServerChan


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


if __name__ == '__main__':
    unittest.main()