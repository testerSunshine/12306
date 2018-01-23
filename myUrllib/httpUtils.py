# -*- coding: utf8 -*-
import datetime
import json
import socket
from time import sleep

import requests


class HTTPClient(object):

    def __init__(self):
        """
        :param method:
        :param headers: Must be a dict. Such as headers={'Content_Type':'text/html'}
        """
        self.initS()

    def initS(self):
        self._s = requests.Session()
        self._s.headers.update(self._set_header())
        return self

    def set_cookies(self, **kwargs):
        """
        设置cookies
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            self._s.cookies.set(k, v)

    def del_cookies(self):
        """
        删除所有的key
        :return:
        """
        self._s.cookies.clear()

    def del_cookies_by_key(self, key):
        """
        删除指定key的session
        :return:
        """
        self._s.cookies.set(key, None)

    def _set_header(self):
        """设置header"""
        return {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Requested-With": "xmlHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Referer": "https://kyfw.12306.cn/otn/login/init",
            "Accept": "*/*",
        }

    def setHeaders(self, headers):
        self._s.headers.update(headers)
        return self

    def resetHeaders(self):
        self._s.headers.clear()
        self._s.headers.update(self._set_header())

    def getHeadersHost(self):
        return self._s.headers["Host"]

    def setHeadersHost(self, host):
        self._s.headers.update({"Host": host})
        return self

    def getHeadersReferer(self):
        return self._s.headers["Referer"]

    def setHeadersReferer(self, referer):
        self._s.headers.update({"Referer": referer})
        return self

    def send(self, url, data=None, **kwargs):
        """send request to url.If response 200,return response, else return None."""
        allow_redirects = False
        error_data = {"code": 99999, "data": ""}
        if data:
            method = "post"
            self.setHeaders({"Content-Length": "{0}".format(len(data))})
        else:
            method = "get"
            self.resetHeaders()
        for i in range(10):
            response = self._s.request(method=method,
                                       timeout=10,
                                       url=url,
                                       data=data,
                                       allow_redirects=allow_redirects,
                                       **kwargs)
            if response.status_code == 200:
                try:
                    if response.content:
                        return json.loads(response.content) if method == "post" else response.content
                    else:
                        return error_data
                except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                    print e.message
                    return error_data
                except socket.error as e:
                    print(e.message)
                    return error_data
            else:
                sleep(0.1)
