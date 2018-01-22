#/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class myrequests:
    def __init__(self,cookies):
        self.s = requests.Session()
        self.cookies = cookies

    def headers(self):
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36',
                 "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                 "X-Requested-With": "xmlHttpRequest",
                 "Referer": "https://kyfw.12306.cn/otn/login/init",
                 "Accept": "application/json, text/javascript, */*; q=0.01",
                 "Origin":"https://kyfw.12306.cn",
                 "Accept-Encoding":"gzip, deflate, br",
                 "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
                 }
        return headers


    def get(self,url):
        result = self.s.get(url,headers=self.headers(),cookies=self.cookies, verify=False)
        return result

    def post(self,url,data):
        result = self.s.post(url, allow_redirects=False,headers=self.headers(),cookies=self.cookies,data=data,verify=False)
        return result


if __name__ == "__main__":
    myrequests.get()
    myrequests.post()