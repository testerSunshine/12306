# encoding=utf8
import collections
import json
import os
import re
import sys
import csv
import requests
from config import urlConf

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass

class CDNProxy:
    def __init__(self, host=None):
        self.host = host
        self.urlConf = urlConf.urls
        self.httpClint = requests
        self.city_list = []
        self.timeout = 5

    def _set_header(self):
        """设置header"""
        return {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Requested-With": "xmlHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Referer": "https://kyfw.12306.cn/otn/login/init",
            "Accept": "*/*",
        }

    def get_city_id(self):
        """
        获取所有城市md5参数
        :return:
        """
        try:
            if self.host:
                while True:
                    url = self.urlConf["cdn_host"]["req_url"]
                    data = {"host": self.host, "lintType": "电信,多线,联通,移动"}
                    rep = self.httpClint.post(url, data, headers=self._set_header(), timeout=self.timeout)
                    city_re = re.compile(r"<li id=\"(\S+)\" class=\"PingListCent PingRLlist")
                    self.city_list = re.findall(city_re, rep.content)
                    if self.city_list:
                        print(self.city_list)
                        break
            else:
                pass
        except:
            pass

    def open_cdn_file(self):
        cdn = []
        # cdn_re = re.compile("CONNECT (\S+) HTTP/1.1")
        # path = os.path.join(os.path.dirname(__file__), '../cdn_list')
        # with open(path, "r") as f:
        #     for i in f.readlines():
        #         # print(i.replace("\n", ""))
        #         cdn_list = re.findall(cdn_re, i)
        #         if cdn_list and "kyfw.12306.cn:443" not in cdn_list:
        #             print(cdn_list[0].split(":")[0])
        #             cdn.append(cdn_list[0].split(":")[0])
        #     return cdn
        path = os.path.join(os.path.dirname(__file__), '../cdn_list')
        with open(path, "r") as f:
            for i in f.readlines():
                # print(i.replace("\n", ""))
                if i and "kyfw.12306.cn:443" not in i:
                    cdn.append(i.replace("\n", ""))
            return cdn


if __name__ == '__main__':
    cdn = CDNProxy()
    print(cdn.open_cdn_file())
