#encoding=utf8
import socket
import urllib
import urllib2
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
        header = {}
        header['User-Agent'] = User_Agent

        for i in range(1, 5):
            url = 'http://www.xicidaili.com/nn/'+str(i)
            req = urllib2.Request(url, headers=header)
            res = urllib2.urlopen(req).read()

            soup = BeautifulSoup(res, "html.parser")
            ips = soup.findAll('tr')

            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
                self.proxy_list.append(ip_temp)

    def filter_proxy(self):
        """
        将不可用IP剔除
        :return: 
        """
        socket.setdefaulttimeout(1)
        f = open("./proxy_list", "w")
        url = "http://ip.chinaz.com/getip.aspx"
        proxy_num = 0
        for proxy in self.proxy_list:
            proxy_temp = {"http://": proxy}
            try:
                urllib.urlopen(url, proxies=proxy_temp).read()
                write_proxy = proxy+"\n"
                f.write(write_proxy)
                proxy_num += 1
            except Exception, e:
                print ("代理链接超时，去除此IP：{0}".format(proxy))
                print e
                continue
        print("总共可使用ip量为{}个".format(proxy_num))

    def get_filter_proxy(self):
        """
        读取该可用ip文件
        :return: 可用ip文件list
        """
        f = open("./proxy_list", "r")
        lins = f.readlines()
        for i in lins:
            p = i.strip("\n")
            self.proxy_filter_list.append(p)
        return self.proxy_filter_list

    def main(self):
        self.get_proxy()
        self.filter_proxy()


if __name__ == "__main__":
    a = proxy()
    a.get_filter_proxy()