# -*- coding: utf8 -*-
import json
import socket
from time import sleep

import requests

from config import logger


class HTTPClient(object):

    def __init__(self):
        """
        :param method:
        :param headers: Must be a dict. Such as headers={'Content_Type':'text/html'}
        """
        self.initS()
        self._cdn = None

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

    @property
    def cdn(self):
        return self._cdn

    @cdn.setter
    def cdn(self, cdn):
        self._cdn = cdn

    def send(self, urls, data=None, **kwargs):
        """send request to url.If response 200,return response, else return None."""
        allow_redirects = False
        is_logger = urls["is_logger"]
        error_data = {"code": 99999, "message": u"重试次数达到上限"}
        self.setHeadersReferer(urls["Referer"])
        if data:
            method = "post"
            self.setHeaders({"Content-Length": "{0}".format(len(data))})
        else:
            method = "get"
            self.resetHeaders()
        if is_logger:
            logger.log(
                u"url: {0}\n入参: {1}\n请求方式: {2}\n".format(urls["req_url"],data,method,))
        self.setHeadersHost(urls["Host"])
        if self.cdn:
            url_host = self.cdn
        else:
            url_host = urls["Host"]
        for i in range(urls["re_try"]):
            try:
                requests.packages.urllib3.disable_warnings()
                response = self._s.request(method=method,
                                           timeout=2,
                                           url="https://" + url_host + urls["req_url"],
                                           data=data,
                                           allow_redirects=allow_redirects,
                                           verify=False,
                                           **kwargs)
                if response.status_code == 200:
                    if response.content:
                        if is_logger:
                            logger.log(
                                u"出参：{0}".format(response.content))
                        return json.loads(response.content) if method == "post" else response.content
                    else:
                        logger.log(
                            u"url: {} 返回参数为空".format(urls["req_url"]))
                        return error_data
                else:
                    sleep(urls["re_time"])
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                pass
            except socket.error:
                pass
        return error_data
