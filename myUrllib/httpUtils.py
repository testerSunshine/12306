# -*- coding: utf8 -*-
import json
import socket
import urllib
from collections import OrderedDict
from time import sleep

import requests

from config import logger


def _set_header_default():
    header_dict = OrderedDict()
    header_dict["Host"] = "kyfw.12306.cn"
    header_dict["Connection"] = "keep-alive"
    header_dict["Accept"] = "application/json, text/javascript, */*; q=0.01"
    header_dict["Origin"] = "https://kyfw.12306.cn"
    header_dict["X-Requested-With"] = "XMLHttpRequest"
    header_dict[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    header_dict["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    header_dict["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"
    header_dict["Accept-Encoding"] = "gzip, deflate, br"
    header_dict["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8"
    return header_dict


def _set_header_j():
    """设置header"""
    return {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Origin": "https://kyfw.12306.cn",
        "Connection": "keep-alive",
    }


def _set_header_x():
    """设置header"""
    return {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Origin": "https://kyfw.12306.cn",
        "Connection": "keep-alive",
    }


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
        self._s.headers.update(_set_header_j())
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

    def setHeaders(self, headers):
        self._s.headers.update(headers)
        return self

    def resetHeaders(self, header_type):
        self._s.headers.clear()
        if header_type == 1:
            self._s.headers.update(_set_header_x())
        else:
            self._s.headers.update(_set_header_j())

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

    # def send_socket(self, urls, data=None, **kwargs):
    #     data = """
    #         POST {0} HTTP/1.1
    #         {0}
    #         """.format(urls["req_url"], self._set_header())
    #     fack = socket.create_connection(urls["Host"], 443)
    #     fack.send()

    def send(self, urls, data=None, **kwargs):
        """send request to url.If response 200,return response, else return None."""
        allow_redirects = False
        is_logger = urls.get("is_logger", False)
        req_url = urls.get("req_url", "")
        re_try = urls.get("re_try", 0)
        s_time = urls.get("s_time", 0)
        contentType = urls.get("Content-Type", 0)
        error_data = {"code": 99999, "message": u"重试次数达到上限"}
        if data:
            method = "post"
            self.setHeaders({"Content-Length": "{0}".format(len(data))})
        else:
            method = "get"
            self.resetHeaders(contentType)
        self.setHeadersReferer(urls["Referer"])
        if is_logger:
            logger.log(
                u"url: {0}\n入参: {1}\n请求方式: {2}\n".format(req_url, data, method, ))
        self.setHeadersHost(urls["Host"])
        if self.cdn:
            url_host = self.cdn
        else:
            url_host = urls["Host"]
        if contentType == 1:
            # 普通from表单
            self.resetHeaders(contentType)
            if method == "post":
                pass
                data = urllib.urlencode(data)
        elif contentType == 0:
            self.resetHeaders(contentType)
        for i in range(re_try):
            try:
                # sleep(urls["s_time"]) if "s_time" in urls else sleep(0.001)
                sleep(s_time)
                requests.packages.urllib3.disable_warnings()
                response = self._s.request(method=method,
                                           timeout=2,
                                           url="https://" + url_host + req_url,
                                           data=data,
                                           allow_redirects=allow_redirects,
                                           verify=False,
                                           **kwargs)
                if response.status_code == 200:
                    if response.content:
                        if is_logger:
                            logger.log(
                                u"出参：{0}".format(response.content))
                        return json.loads(response.content) if urls["is_json"] else response.content
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
