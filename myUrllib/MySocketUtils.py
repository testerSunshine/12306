# coding=utf-8
import json
import socket
import re
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('183.232.189.31', 80))
# get_str = 'GET {0} HTTP/1.1\r\nConnection: close\r\n' \
#           'Host: %s\r\n' \
#           'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36' \
#           '\r\nAccept: */*\r\n' \
#           '\r\n'
# post_str = "POST {0} HTTP/1.1\r\n" \
#            "Host: kyfw.12306.cn\r\n" \
#            "Connection: close\r\n"\
#            "Origin: https://kyfw.12306.cn\r\n" \
#            "X-Requested-With: XMLHttpRequest\r\n" \
#            "Referer: https://kyfw.12306.cn/otn/leftTicket/init\r\n" \
#            "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8\r\n" \
#            "Content-Type: application/x-www-form-urlencoded; charset=UTF-8\r\n" \
#            "Accept: application/json, text/javascript, */*; q=0.01\r\n" \
#            "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5\r\n" \
#            "Content-Length: 9\r\n"\
#            "Cookie: _passport_session=a459aba69761497eb31de76c27795e999613; _passport_ct=9116b2cb0bf443e1a01d22ac8c1ae449t5007; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerpool_passport=200081930.50215.0000; BIGipServerotn=484704778.64545.0000\r\n\n"\
#            "appid=otn\r\n"
# # s.sendall(get_str.format("https://kyfw.12306.cn/otn/resources/login.html"))
# s.sendall(post_str.format("https://kyfw.12306.cn/passport/web/auth/uamtk"))
from config.urlConf import urls


def default_get_data():
    """
    get请求默认组装字符串
    需要拼接的字符串
    -- url 发送请求的全连接
    :return:
        """
    return 'GET {0} HTTP/1.1\r\nConnection: close\r\n' \
           'Host: kyfw.12306.cn\r\n' \
           "Referer: {1}\r\n" \
           'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36' \
           '\r\nAccept: */*\r\n' \
           "Cookie: {2}\r\n\n"\
           '\r\n'
    # return 'GET {0} HTTP/1.1\r\nConnection: close\r\n' \
    #       'Host: kyfw.12306.cn\r\n' \
    #       'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36' \
    #       '\r\nAccept: */*\r\n' \
    #       '\r\n'


def default_post_data():
    """
    post请求默认组装字符串
    需要拼接的字符串
    -- url 发送请求的全连接
    -- Referer 请求页面来源
    -- Content-Length: body 长度
    -- Cookie 页面请求的身份认证
    -- appid 接口请求报文
    :return:
    """
    return "POST https://kyfw.12306.cn{0} HTTP/1.1\r\n" \
           "Host: kyfw.12306.cn\r\n" \
           "Connection: close\r\n"\
           "Origin: https://kyfw.12306.cn\r\n" \
           "X-Requested-With: XMLHttpRequest\r\n" \
           "Referer: {3}\r\n" \
           "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8\r\n" \
           "Content-Type: application/x-www-form-urlencoded; charset=UTF-8\r\n" \
           "Accept: application/json, text/javascript, */*; q=0.01\r\n" \
           "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5\r\n" \
           "Content-Length: {2}\r\n"\
           "Cookie: {4}\r\n\n"\
           "{1}\r\n"\
           # "\r\n"


class socketUtils:
    def __init__(self, host, port=80):
        self.host = host
        self.port = port
        self.s = self.connect_socket(self.host, self.port)

    def connect_socket(self, host, port):
        """
        连接socket
        :param host:
        :param port:
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host if isinstance(host, str) else str(host),
                   port if isinstance(port, int) else int(port)))
        return s

    def close_s(self):
        self.s.close()

    # def send(self, urls, Cookie=None, data=None):
    #     """
    #     发送请求
    #     :param urls:
    #     :param data:
    #     :param cookie:
    #     :return:
    #     """
    #     url = urls.get("req_url", "")
    #     Referer = urls.get("Referer", "")
    #     if urls.get("req_type", "get") == "post":
    #         Content_Length = len(data)
    #     Cookie = "tk=pnidlCoFy2B7wxO_X_pESbrkZFSq3OtVA_xzXwuba2a0; JSESSIONID=C6144324BFCE36AC5082E543E934E8B3; current_captcha_type=Z; _jc_save_fromDate=2018-08-03; _jc_save_fromStation=%u6DF1%u5733%2CSZQ; _jc_save_toDate=2018-08-03; _jc_save_toStation=%u957F%u6C99%2CCSQ; _jc_save_wfdc_flag=dc; ten_key=b5L6aMWfnzBm8CgQe8pcAKQsmVBS2PYH; BIGipServerpool_passport=166527498.50215.0000; BIGipServerotn=165937674.50210.0000; route=c5c62a339e7744272a54643b3be5bf64; RAIL_DEVICEID=fC-yepiUqNjsBiRvtLBXW4JqQmabCfB9QxI3FifJZK9YDRsImhJLSz4sAQ4HiGF7uQAFdFyISg6jA7KAhtpEldJV9ZMNsn6Dzm_psA5CBDwSNfiORf42w-LIRvkeGvdKFtegZwWGlkA2fVuEWKu-1xAYdCXRnsMD; RAIL_EXPIRATION=1533420302032; _jc_save_detail=true"
    #     if data:
    #         send_value = default_post_data().format(url,
    #                                                 data,
    #                                                 Content_Length,
    #                                                 Referer,
    #                                                 Cookie
    #                                                 )
    #         print("send_value: " + send_value)
    #         self.s.sendall(send_value)
    #     else:
    #         self.s.sendall(default_get_data().format(url,
    #                                                  Referer,
    #                                                  Cookie))
    #     total_data = ""
    #     while 1:
    #         data = self.s.recv(1024)
    #         total_data += data
    #         if not data:
    #             break
    #     self.close_s()
    #     print(total_data)
    #     return self.recv_data(total_data)

    def recv_data(self, r_data):
        cookie = self.get_cookie(r_data)
        status_code = self.get_status_code(r_data)
        r_body = self.get_rep_body(r_data)
        return {
            "cookie": cookie,
            "status_code": status_code,
            "r_body": r_body
        }

    @staticmethod
    def get_cookie(recv_data):
        """
        提取cookie
        :param recv_data:
        :return:
        """
        if not isinstance(recv_data, str):
            recv_data = str(recv_data)
        cookies_re = re.compile(r"Set-Cookie: (\S+);")
        cookies = re.findall(cookies_re, recv_data)
        return "; ".join(cookies)

    @staticmethod
    def get_status_code(recv_data):
        """
        获取状态码
        :return:
        """
        if not isinstance(recv_data, str):
            recv_data = str(recv_data)
        http_code_re = re.compile(r"HTTP/1.1 (\S+) ")
        status_code = re.search(http_code_re, recv_data).group(1)
        return status_code

    @staticmethod
    def get_rep_body(recv_data):
        """
        获取返回值
        :param recv_data:
        :return:
        """
        if not isinstance(recv_data, str):
            recv_data = str(recv_data)
        if recv_data.find("{") != -1 and recv_data.find("}") != -1:
            data = json.loads(recv_data.split("\n")[-1])
            return data
        else:
            print(recv_data)


if __name__ == "__main__":
    so = socketUtils('183.232.189.31', 80)
    train_date = "2018-08-03"
    from_station = "SZQ"
    to_station = "CSQ"
    urls["select_url"]["req_url"] = "https://kyfw.12306.cn" + urls["select_url"]["req_url"].format(train_date, from_station, to_station)
    result = so.send(urls=urls["select_url"])
    print(result)

    so = socketUtils('183.232.189.31', 80)

    data = "secretStr=Vgo534nDZiCH8NCvyEPcGepzJoRCjvYr34gKFv5CW1K1XtM6mtKHoiFPjUYvaVKoe06SMhUUpT%2FK%0AxIEIsBD4zHgJPpVyKiTPx80y6OCWhNgcKjib2LLMXMJfgTgh0RKPISjkDjVFmO9p905O%2FegDeKjp%0A1fhIeqCuYraHjNhI0PjQY39BAY4AHLzW0iGgDq8b%2FtpyOY8Td2XfIWNZJCWzgyPkNXOk0HUguB2G%0AKh2T8nlko6zb5ra%2B%2BA%3D%3D&train_date=2018-08-03&back_train_date=2018-08-03&tour_flag=dc&purpose_codes=ADULT&query_from_station_name=深圳&query_to_station_name=长沙&undefined"
    result1 = so.send(urls=urls["submit_station_url"], data=data)
    print(result1)
    # so = socketUtils('183.232.189.31', 80)
    # result = so.send(url="https://kyfw.12306.cn/passport/web/login", s_data="")
    # print(result)