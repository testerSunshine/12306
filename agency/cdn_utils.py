# encoding=utf8
import datetime
import os
import requests
from config import urlConf
import threading
from config.urlConf import urls

from myUrllib.httpUtils import HTTPClient

cdn_list = []


class CDNProxy(threading.Thread):
    def __init__(self, cdns):
        super().__init__()
        self.cdns = cdns
        self.urlConf = urlConf.urls
        self.httpClint = requests
        self.city_list = []
        self.timeout = 5

    def run(self):
        for cdn in self.cdns:
            http = HTTPClient(0)
            url = urls["loginInitCdn"]
            http._cdn = cdn.replace("\n", "")
            start_time = datetime.datetime.now()
            rep = http.send(url)
            if rep and "message" not in rep and (datetime.datetime.now() - start_time).microseconds / 1000 < 1000:
                if cdn.replace("\n", "") not in cdn_list:  # 如果有重复的cdn，则放弃加入
                    print(f"加入cdn: {cdn}")
                    cdn_list.append(cdn.replace("\n", ""))


def open_cdn_file(cdnFile):
    cdn = []
    path = os.path.join(os.path.dirname(__file__), f'../{cdnFile}')
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i in f.readlines():
                if i and "kyfw.12306.cn:443" not in i:
                    cdn.append(i.replace("\n", ""))
            return cdn
    except Exception:
        with open(path, "r") as f:
            for i in f.readlines():
                if i and "kyfw.12306.cn:443" not in i:
                    cdn.append(i.replace("\n", ""))
            return cdn


def filterCdn():
    """
    过滤cdn, 过滤逻辑为当前cdn响应值小于1000毫秒
    过滤日志:
        加入cdn: 116.77.75.146
    :return:
    """
    cdns = open_cdn_file("cdn_list")
    cdnss = [cdns[i:i + 50] for i in range(0, len(cdns), 50)]
    cdnThread = []
    for cdn in cdnss:
        t = CDNProxy(cdn)
        cdnThread.append(t)
    for cdn_t in cdnThread:
        cdn_t.start()

    for cdn_j in cdnThread:
        cdn_j.join()

    print(f"当前有效cdn个数为: {len(cdn_list)}")
    if cdn_list:
        f = open(r"../filter_cdn_list", "a+")
        for c in cdn_list:
            f.writelines(f"{c}\n")
        f.close()


if __name__ == '__main__':
    filterCdn()
