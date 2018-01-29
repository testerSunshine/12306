# -*- coding: utf8 -*-
import datetime
import json
import socket
from time import sleep

import requests
import sys
import random

from config import logger

USER_AGENTS = [  
 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",  
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",  
 "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",  
 "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",  
 "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",  
 "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",  
 "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",  
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",  
 "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",  
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",  
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",  
 "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",  
 "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",  
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",  
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",  
 "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",  
] 


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
        add_header = self._set_header()
        agent = random.choice(USER_AGENTS) 
        add_header.update({'User-Agent' : agent}) 

        self._s.headers.update(add_header)

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

    def send(self, url, data=None, is_logger=True, **kwargs):
        """send request to url.If response 200,return response, else return None."""
        allow_redirects = False
        error_data = '{"code": 99999, "message": "重试次数达到上限"}'
        if data:
            method = "post"
            self.setHeaders({"Content-Length": "{0}".format(len(data))})
        else:
            method = "get"
            self.resetHeaders()
        if is_logger:
            logger.log(
                u"url: {0}\n入参: {1}\n请求方式: {2}\n".format(url,data,method,))
        for i in range(3):
            try:
                response = self._s.request(method=method,
                                           timeout=10,
                                           url=url,
                                           data=data,
                                           allow_redirects=allow_redirects,
                                           **kwargs)
                # if response.status_code == 200:
                if response.content:
                    if is_logger:
                        logger.log(
                            u"出参：{0}".format(response.content))
                    return json.loads(response.content) if method == "post" else response.content
                else:
                    print(
                        u"url: {} 返回参数为空".format(url))
                    raise requests.exceptions.ConnectionError()
                # else:
                #     print('retry')
                #     sleep(0.2)
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                pass
            except socket.error:
                pass
            
        return error_data
session = HTTPClient()