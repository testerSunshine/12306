# -*- coding=utf-8 -*-
import http.client
import ssl
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import sys
from http.cookiejar import LWPCookieJar
# import imp
#
# imp.reload(sys)
# sys.setdefaultencoding('UTF8')
cookiejar = LWPCookieJar()
cookiesuppor = urllib.request.HTTPCookieProcessor(cookiejar)
opener = urllib.request.build_opener(cookiesuppor, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)
ssl._create_default_https_context = ssl._create_unverified_context


def get(url):
    try:
        request = urllib.request.Request(url=url)
        request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=utf-8")
        request.add_header('X-Requested-With', 'xmlHttpRequest')
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
        request.add_header('Referer', 'https://kyfw.12306.cn/otn/login/init')
        request.add_header('Accept', '*/*')
        result = urllib.request.urlopen(request).read()
        assert isinstance(result, object)
        return result
    except http.client.error as e:
        print(e)
        pass
    except urllib.error.URLError as e:
        print(e)
        pass
    except urllib.request.HTTPBasicAuthHandler as xxx_todo_changeme:
        urllib.error.HTTPError = xxx_todo_changeme
        pass


def Post(url, data):
    try:
        request = urllib.request.Request(url=url, data=urllib.parse.urlencode(data).encode(encoding='UTF8'))
        # req.add_header('User-Agent', 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0')
        # request = urllib2Post.Request(ajax_url, urllib.urlencode(dc))
        request.add_header("Content-Type", "application/x-www-form-urlencoded;application/json;charset=utf-8")
        request.add_header('X-Requested-With', 'xmlHttpRequest')
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
        request.add_header('Referer', 'https://kyfw.12306.cn/otn/login/init')
        request.add_header('Accept', '*/*')
        # request.add_header('Accept-Encoding', 'gzip, deflate')
        for i in range(3):
            result = urllib.request.urlopen(request).read()
            if result:
                return result
            else:
                print(("返回结果为空，正在第{0}重试".format(i)))
    except http.client.error as e:
        return e
    except urllib.error.URLError as e:
        return e
    except urllib.request.HTTPBasicAuthHandler as xxx_todo_changeme1:
        urllib.error.HTTPError = xxx_todo_changeme1
        return ('error')