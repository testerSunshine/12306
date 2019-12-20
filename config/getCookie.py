import json
import random
import re
import time
import os
import TickerConfig
from config.urlConf import urls


def getDrvicesID(session):
    """
    :return:
    """
    print("cookie获取中")
    if TickerConfig.COOKIE_TYPE is 1:
        from selenium import webdriver
        cookies = []
        # 解决放镜像里 DevToolsActivePort file doesn't exist的问题
        options = webdriver.ChromeOptions()
        if os.name != 'nt' and TickerConfig.CHROME_CHROME_PATH:
            options = webdriver.ChromeOptions()
            options.binary_location = TickerConfig.CHROME_CHROME_PATH
            options.add_argument(
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=TickerConfig.CHROME_PATH,chrome_options=options)
        driver.get("https://www.12306.cn/index/index.html")
        time.sleep(10)
        for c in driver.get_cookies():
            cookie = dict()
            print()
            if c.get("name") == "RAIL_DEVICEID" or c.get("name") == "RAIL_EXPIRATION":
                cookie[c.get("name")] = c.get("value")
                cookies.append(cookie)
        print(f"获取cookie: {cookies}")
        if cookies:
            session.httpClint.set_cookies(cookies)
            session.cookies = cookies
        print("cookie获取完成")
    elif TickerConfig.COOKIE_TYPE is 2:
        request_device_id(session)
    elif TickerConfig.COOKIE_TYPE is 3:
        # RAIL_DEVICEID,RAIL_EXPIRATION的值打开12306官网可以获取headers-Cookies
        if not TickerConfig.RAIL_DEVICEID or not TickerConfig.RAIL_EXPIRATION:
            print("警告！！: RAIL_DEVICEID,RAIL_EXPIRATION的值为空，请手动打开12306官网可以获取headers-Cookies中的RAIL_DEVICEID,RAIL_EXPIRATION，填入配置文件中")
        cookies = [{
            "RAIL_DEVICEID": TickerConfig.RAIL_DEVICEID,
            "RAIL_EXPIRATION": TickerConfig.RAIL_EXPIRATION,
        }]
        session.httpClint.set_cookies(cookies)
        session.cookies = cookies


def request_device_id(session):
    """
    获取加密后的浏览器特征 ID
    :return:
    """
    params = {"algID": request_alg_id(session), "timestamp": int(time.time() * 1000)}
    params = dict(params, **_get_hash_code_params())
    response = session.httpClint.send(urls.get("getDevicesId"), params=params)
    if response.find('callbackFunction') >= 0:
        result = response[18:-2]
        try:
            result = json.loads(result)
            session.httpClint.set_cookies([{
                'RAIL_EXPIRATION': result.get('exp'),
                'RAIL_DEVICEID': result.get('dfp'),
            }])
            session.cookies = [{
                'RAIL_EXPIRATION': result.get('exp'),
                'RAIL_DEVICEID': result.get('dfp'),
            }]
        except:
            return False


def request_alg_id(session):
    response = session.httpClint.send(urls.get("GetJS"))
    result = re.search(r'algID\\x3d(.*?)\\x26', response)
    try:
        return result.group(1)
    except (IndexError, AttributeError) as e:
        pass
    return ""


def _get_hash_code_params():
    from collections import OrderedDict
    data = {
        'adblock': '0',
        'browserLanguage': 'en-US',
        'cookieEnabled': '1',
        'custID': '133',
        'doNotTrack': 'unknown',
        'flashVersion': '0',
        'javaEnabled': '0',
        'jsFonts': 'c227b88b01f5c513710d4b9f16a5ce52',
        'localCode': '3232236206',
        'mimeTypes': '52d67b2a5aa5e031084733d5006cc664',
        'os': 'MacIntel',
        'platform': 'WEB',
        'plugins': 'd22ca0b81584fbea62237b14bd04c866',
        'scrAvailSize': str(random.randint(500, 1000)) + 'x1920',
        'srcScreenSize': '24xx1080x1920',
        'storeDb': 'i1l1o1s1',
        'timeZone': '-8',
        'touchSupport': '99115dfb07133750ba677d055874de87',
        'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.' + str(
            random.randint(
                5000, 7000)) + '.0 Safari/537.36',
        'webSmartID': 'f4e3b7b14cc647e30a6267028ad54c56',
    }
    data_trans = {
        'browserVersion': 'd435',
        'touchSupport': 'wNLf',
        'systemLanguage': 'e6OK',
        'scrWidth': 'ssI5',
        'openDatabase': 'V8vl',
        'scrAvailSize': 'TeRS',
        'hasLiedResolution': '3neK',
        'hasLiedOs': 'ci5c',
        'timeZone': 'q5aJ',
        'userAgent': '0aew',
        'userLanguage': 'hLzX',
        'jsFonts': 'EOQP',
        'scrAvailHeight': '88tV',
        'browserName': '-UVA',
        'cookieCode': 'VySQ',
        'online': '9vyE',
        'scrAvailWidth': 'E-lJ',
        'flashVersion': 'dzuS',
        'scrDeviceXDPI': '3jCe',
        'srcScreenSize': 'tOHY',
        'storeDb': 'Fvje',
        'doNotTrack': 'VEek',
        'mimeTypes': 'jp76',
        'sessionStorage': 'HVia',
        'cookieEnabled': 'VPIf',
        'os': 'hAqN',
        'hasLiedLanguages': 'j5po',
        'hasLiedBrowser': '2xC5',
        'webSmartID': 'E3gR',
        'appcodeName': 'qT7b',
        'javaEnabled': 'yD16',
        'plugins': 'ks0Q',
        'appMinorVersion': 'qBVW',
        'cpuClass': 'Md7A',
        'indexedDb': '3sw-',
        'adblock': 'FMQw',
        'localCode': 'lEnu',
        'browserLanguage': 'q4f3',
        'scrHeight': '5Jwy',
        'localStorage': 'XM7l',
        'historyList': 'kU5z',
        'scrColorDepth': "qmyu"
    }
    data = OrderedDict(data)
    d = ''
    params = {}
    for key, item in data.items():
        d += key + item
        key = data_trans[key] if key in data_trans else key
        params[key] = item
    d_len = len(d)
    d_f = int(d_len / 3) if d_len % 3 == 0 else int(d_len / 3) + 1
    if d_len >= 3:
        d = d[d_f:2 * d_f] + d[2 * d_f:d_len] + d[0: d_f]
    d_len = len(d)
    d_f = int(d_len / 3) if d_len % 3 == 0 else int(d_len / 3) + 1
    if d_len >= 3:
        d = d[2 * d_f:d_len] + d[0: d_f] + d[1 * d_f: 2 * d_f]

    d = _encode_data_str_v2(d)
    d = _encode_data_str_v2(d)
    d = _encode_data_str_v2(d)
    data_str = _encode_string(d)
    params['hashCode'] = data_str
    return params


def _encode_data_str_v2(d):
    b = len(d)
    if b % 2 == 0:
        return d[b // 2: b] + d[0:b // 2]
    else:
        return d[b // 2 + 1:b] + d[b // 2] + d[0:b // 2]


def _encode_string(str):
    import hashlib
    import base64
    result = base64.b64encode(hashlib.sha256(str.encode()).digest()).decode()
    return result.replace('+', '-').replace('/', '_').replace('=', '')
