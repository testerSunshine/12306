#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

URL = "http://littlebigluo.qicp.net:47720/"


class fuck12306(object):
    def __init__(self):
        self.file_path = "../getPassCodeNew.jpeg"
        pass

    def fuck(self, file_path):
        """
        :param file_path: 验证码文件
        :return: str 对应图片
        """
        data = {"pic_file": open(file_path, 'rb')}
        resp = requests.post(URL, files=data)
        if resp.status_code == 200:
            return self._parse_result(resp.text)
        else:
            return None

    def _parse_result(self, text):
        soup = BeautifulSoup(text, "lxml")
        return soup.font.b.string
        pass


