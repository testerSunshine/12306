# -*- coding=utf-8 -*-
import copy
import json
import random
import re
import time
from collections import OrderedDict
from time import sleep
import TickerConfig
from config.urlConf import urls
from inter.GetPassCodeNewOrderAndLogin import getPassCodeNewOrderAndLogin1
from inter.GetRandCode import getRandCode
from inter.LoginAysnSuggest import loginAysnSuggest
from inter.LoginConf import loginConf
from myException.UserPasswordException import UserPasswordException


class GoLogin:
    def __init__(self, session, is_auto_code, auto_code_type):
        self.session = session
        self.randCode = ""
        self.is_auto_code = is_auto_code
        self.auto_code_type = auto_code_type

    def auth(self):
        """
        :return:
        """
        self.session.httpClint.send(self.session.urls["loginInitCdn1"])
        uamtkStaticUrl = self.session.urls["uamtk-static"]
        uamtkStaticData = {"appid": "otn"}
        return self.session.httpClint.send(uamtkStaticUrl, uamtkStaticData)

    def codeCheck(self):
        """
        验证码校验
        :return:
        """
        # codeCheck = self.session.urls["codeCheck"]
        # codeCheckData = {
        #     "answer": self.randCode,
        #     "rand": "sjrand",
        #     "login_site": "E"
        # }
        # fresult = self.session.httpClint.send(codeCheck, codeCheckData)
        codeCheckUrl = copy.deepcopy(self.session.urls["codeCheck1"])
        codeCheckUrl["req_url"] = codeCheckUrl["req_url"].format(self.randCode, int(time.time() * 1000))
        fresult = self.session.httpClint.send(codeCheckUrl)
        if not isinstance(fresult, str):
            print("登录失败")
            return
        fresult = eval(fresult.split("(")[1].split(")")[0])
        if "result_code" in fresult and fresult["result_code"] == "4":
            print(u"验证码通过,开始登录..")
            return True
        else:
            if "result_message" in fresult:
                print(fresult["result_message"])
            sleep(1)
            self.session.httpClint.del_cookies()

    def baseLogin(self, user, passwd):
        """
        登录过程
        :param user:
        :param passwd:
        :return: 权限校验码
        """
        logurl = self.session.urls["login"]

        loginData = OrderedDict()
        loginData["username"] = user,
        loginData["password"] = passwd,
        loginData["appid"] = "otn",
        loginData["answer"] = self.randCode,

        tresult = self.session.httpClint.send(logurl, loginData)
        if 'result_code' in tresult and tresult["result_code"] == 0:
            print(u"登录成功")
            tk = self.auth()
            if "newapptk" in tk and tk["newapptk"]:
                return tk["newapptk"]
            else:
                return False
        elif 'result_message' in tresult and tresult['result_message']:
            messages = tresult['result_message']
            if messages.find(u"密码输入错误") is not -1:
                raise UserPasswordException("{0}".format(messages))
            else:
                print(u"登录失败: {0}".format(messages))
                print(u"尝试重新登陆")
                return False
        else:
            return False

    def getUserName(self, uamtk):
        """
        登录成功后,显示用户名
        :return:
        """
        if not uamtk:
            return u"权限校验码不能为空"
        else:
            uamauthclientUrl = self.session.urls["uamauthclient"]
            data = {"tk": uamtk}
            uamauthclientResult = self.session.httpClint.send(uamauthclientUrl, data)
            if uamauthclientResult:
                if "result_code" in uamauthclientResult and uamauthclientResult["result_code"] == 0:
                    print(u"欢迎 {} 登录".format(uamauthclientResult["username"]))
                    return True
                else:
                    return False
            else:
                self.session.httpClint.send(uamauthclientUrl, data)
                url = self.session.urls["getUserInfo"]
                self.session.httpClint.send(url)

    def go_login(self):
        """
        登陆
        :param user: 账户名
        :param passwd: 密码
        :return:
        """
        user, passwd = TickerConfig.USER, TickerConfig.PWD
        self.request_device_id()
        if not user or not passwd:
            raise UserPasswordException(u"温馨提示: 用户名或者密码为空，请仔细检查")
        login_num = 0
        while True:
            if loginConf(self.session):
                self.auth()

                result = getPassCodeNewOrderAndLogin1(session=self.session, imgType="login")
                if not result:
                    continue
                self.randCode = getRandCode(self.is_auto_code, self.auto_code_type, result)
                print(self.randCode)
                login_num += 1
                self.auth()
                if self.codeCheck():
                    uamtk = self.baseLogin(user, passwd)
                    if uamtk:
                        self.getUserName(uamtk)
                        break
            else:
                loginAysnSuggest(self.session, username=user, password=passwd)
                login_num += 1
                break

    def request_device_id(self):
        """
        获取加密后的浏览器特征 ID
        :return:
        """
        params = {"algID": self.request_alg_id(), "timestamp": int(time.time() * 1000)}
        params = dict(params, **self._get_hash_code_params())
        response = self.session.httpClint.send(urls.get("getDevicesId"), params=params)
        if response.find('callbackFunction') >= 0:
            result = response[18:-2]
            try:
                result = json.loads(result)
                self.session.httpClint.set_cookies({
                    'RAIL_EXPIRATION': result.get('exp'),
                    'RAIL_DEVICEID': result.get('dfp'),
                })
            except:
                return False

    def request_alg_id(self):
        response = self.session.httpClint.send(urls.get("GetJS"))
        result = re.search(r'algID\\x3d(.*?)\\x26', response)
        try:
            return result.group(1)
        except (IndexError, AttributeError) as e:
            pass
        return ""

    def _get_hash_code_params(self):
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

        d = self._encode_data_str_v2(d)
        d = self._encode_data_str_v2(d)
        d = self._encode_data_str_v2(d)
        data_str = self._encode_string(d)
        params['hashCode'] = data_str
        return params

    def _encode_data_str_v2(self, d):
        b = len(d)
        if b % 2 == 0:
            return d[b // 2: b] + d[0:b // 2]
        else:
            return d[b // 2 + 1:b] + d[b // 2] + d[0:b // 2]

    def _encode_string(self, str):
        import hashlib
        import base64
        result = base64.b64encode(hashlib.sha256(str.encode()).digest()).decode()
        return result.replace('+', '-').replace('/', '_').replace('=', '')