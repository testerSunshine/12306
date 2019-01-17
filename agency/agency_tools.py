# encoding=utf8
import os
import random
import socket
import time

import requests
from bs4 import BeautifulSoup


class proxy:
    def __init__(self):
        self.proxy_list = []
        self.proxy_filter_list = []

    def get_proxy(self):
        """
        获取未加工代理列表
        :return: 
        """
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = dict()
        header['User-Agent'] = User_Agent

        for i in range(1, 5):
            time.sleep(1)
            url = 'http://www.xicidaili.com/nn/' + str(i)
            res = requests.get(url=url, headers=header).content

            soup = BeautifulSoup(res, "html.parser")
            ips = soup.findAll('tr')

            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
                print(ip_temp)
                self.proxy_list.append(ip_temp)

    def filter_proxy(self):
        """
        将不可用IP剔除
        :return: 
        """
        socket.setdefaulttimeout(1)
        path = os.path.join(os.path.dirname(__file__), './proxy_list')
        f = open(path, "w")
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Connection': 'keep-alive'}
        url = "http://icanhazip.com"
        proxy_num = 0
        for proxy in self.proxy_list:
            proxy_temp = {"https": "https://{}".format(proxy)}
            try:
                req = requests.get(url, proxies=proxy_temp, timeout=2, headers=head).content
                print(req)
                write_proxy = proxy + "\n"
                f.write(write_proxy)
                proxy_num += 1
            except Exception:
                print ("代理链接超时，去除此IP：{0}".format(proxy))
                continue
        print("总共可使用ip量为{}个".format(proxy_num))

    def get_filter_proxy(self):
        """
        读取该可用ip文件
        :return: 可用ip文件list
        """
        path = os.path.join(os.path.dirname(__file__), './proxy_list')
        try:
            with open(path, "r", encoding="utf-8") as f:
                lins = f.readlines()
                for i in lins:
                    p = i.strip("\n")
                    self.proxy_filter_list.append(p)
        except Exception:
            with open(path, "r", ) as f:
                lins = f.readlines()
                for i in lins:
                    p = i.strip("\n")
                    self.proxy_filter_list.append(p)
        return self.proxy_filter_list

    def main(self):
        # self.get_proxy()
        self.filter_proxy()

    def setProxy(self):
        """
        开启此功能的时候请确保代理ip是否可用
        查询的时候设置代理ip,ip设置格式是ip地址+端口，推荐可用的ip代理池：https://github.com/jhao104/proxy_pool
        :return:
        """
        ip = self.get_filter_proxy()
        setIp = ip[random.randint(0, len(ip) - 1)]
        proxie = {
            'http': 'http://{}'.format(setIp),
            'https': 'http://{}'.format(setIp),
        }
        return proxie


if __name__ == "__main__":
    a = proxy()
    print(a.get_filter_proxy())
