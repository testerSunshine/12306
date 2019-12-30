# encoding=utf8
import operator
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from config.urlConf import urls

from myUrllib.httpUtils import HTTPClient

finish_count = 0


def calculate_rtt_blocking(cdn):
    global finish_count
    http = HTTPClient(0)
    url = urls["loginInitCdn"]
    http._cdn = cdn
    rtt_dict = {"rtt": 9999}
    http.send(url, elapsed=rtt_dict)
    rtt = rtt_dict["rtt"]
    finish_count += 1
    # 过滤逻辑为当前cdn响应值小于1000毫秒
    if rtt < 2000:
        print(f"ip:{cdn}，延迟:{rtt}，已测试个数: {finish_count}")
        return {"ip": cdn, "time": rtt}
    else:
        print(f"ip:{cdn}，延迟:N/A，已测试个数: {finish_count}")
        return None


async def calculate_all_rtt_async(cdns, loop, executor):
    done, pending = await asyncio.wait(fs=[loop.run_in_executor(executor, calculate_rtt_blocking, cdn) for cdn in cdns],
                                       return_when=asyncio.ALL_COMPLETED)
    cdn_list = [task.result() for task in done if task.exception() is None and task.result() is not None]
    return cdn_list


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


def sortCdn(cdn_list):
    """
    对cdn进行排序
    :return:
    """
    ips = []
    cs = sorted(cdn_list, key=operator.itemgetter('time'))
    for c in cs:
        print(f"当前ip: {c['ip']}, 延时: {c['time']}")
        ips.append(c["ip"])
    return ips


def filterCdn():
    """
    过滤cdn, 过滤逻辑为当前cdn响应值小于1000毫秒
    过滤日志:
        加入cdn: 116.77.75.146
    :return:
    """
    cdns = open_cdn_file("cdn_list")
    loop = asyncio.get_event_loop()
    cdn_list = loop.run_until_complete(calculate_all_rtt_async(cdns, loop, ThreadPoolExecutor()))
    print(f"当前有效cdn个数为: {len(cdn_list)}")
    if cdn_list:
        ips = sortCdn(cdn_list)
        path = os.path.join(os.path.dirname(__file__), f'../filter_cdn_list')
        f = open(path, "a+")
        f.seek(0)
        f.truncate()
        f.writelines("")
        for ip in ips:
            f.writelines(f"{ip}\n")
        f.close()


if __name__ == '__main__':
    filterCdn()
