# encoding=utf8
import collections
import json
import re
import sys
import csv
import requests
from config import urlConf
reload(sys)
sys.setdefaultencoding('utf-8')


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
                        print self.city_list
                        break
            else:
                pass
        except:
            pass

    def open_cdn_file(self):
        f = open("./cdn_list", "a+")
        return f

    def get_cdn_list(self):
        """
        筛选代理
        :return:
        """
        f = self.open_cdn_file()
        url = self.urlConf["cdn_list"]["req_url"]
        num = 1
        f.seek(0)
        f.truncate()
        for guid in self.city_list:
            data = {"guid": guid,
                    "host": "kyfw.12306.cn",
                    "ishost": 0,
                    "encode": "HJXhdRqjh5yCF6G/AZ6EDk9faB1oSk5r",
                    "checktype": 0}
            try:
                cdn_info = self.httpClint.post(url, data, headers=self._set_header(), timeout=self.timeout).content
                print(cdn_info)
                if cdn_info:
                    split_cdn = cdn_info.split("(")[1].rstrip(")").replace("{", "").replace("}", "").split(",")
                    local_dict = collections.OrderedDict()
                    for i in split_cdn:
                        splits = i.split(":")
                        local_dict[splits[0]] = splits[2] if splits[0] == "result" else splits[1]
                    if local_dict and "state" in local_dict and local_dict["state"] == "1":
                        if "responsetime" in local_dict and local_dict["responsetime"].find("毫秒") != -1 and int(filter(str.isdigit, local_dict["responsetime"])) < 100:
                            f.write(json.dumps(local_dict)+"\n")
                            num += 1
            except Exception as e:
                print(e.message)
        print(u"本次cdn获取完成，总个数{0}".format(num))

    def all_cdn(self):
        """获取cdn列表"""
        with open('./cdn_list', 'r') as f:
            cdn = f.readlines()
            return cdn

    def par_csv(self):
        cdn_csv = csv.reader(open("../cdn1.csv", "r"))
        for c in cdn_csv:
            cdn_re = re.compile(r'https://(\S+)/otn/index/init')
            cdn_ip = re.findall(cdn_re, c[0])
            if cdn_ip and c[2] == "200":
                print(cdn_ip[0])


if __name__ == '__main__':
    cdn = CDNProxy()
    cdn.get_city_id()
    # cdn.get_cdn_list()
    cdn.par_csv()
