# -*- coding: utf8 -*-
import datetime
import requests


class HTTPClient(object):

    def __init__(self):
        """
        :param method:
        :param headers: Must be a dict. Such as headers={'Content_Type':'text/html'}
        """
        self.session = requests.session()
        self._set_header()

    def _set_header(self):
        """设置header"""
        add_header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Requested-With": "xmlHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36",
            "Referer": "https://kyfw.12306.cn/otn/login/init",
            "Accept": "*/*",
        }
        self.session.headers.update(add_header)

    def get(self, url, proxy=None, **kwargs):
        if proxy:
            proxies = {"http": proxy}
        else:
            proxies = ""
        response = self.session.request(method="GET",
                                        url=url,
                                        proxies=proxies,
                                        **kwargs)
        if response.status_code == 200:
            return response.content
        else:
            print("请求失败。{0}".format(response))

    def post(self, url, data=None, proxy=None, **kwargs):
        if proxy:
            proxies = {"http": proxy}
        else:
            proxies = ""
        response = self.session.request(method="POST",
                                        url=url,
                                        data=data,
                                        proxies=proxies,
                                        **kwargs)
        if response.status_code == 200:
            return response.content
        else:
            print("请求失败。{0}".format(response))