#!/bin/env python
# -*- coding=utf-8 -*-
import random
import json
import re
from time import sleep

from config.ticketConf import _get_yaml
from PIL import Image
from damatuCode.damatuWeb import DamatuApi
from damatuCode.ruokuai import RClient
import requests
from init import gol
import traceback
from http.client import RemoteDisconnected
import time
from myUrllib.httpUtils import HTTPClient


class go_login:
    def __init__(self,  ticket_config=""):
        self.config_data = _get_yaml(ticket_config)
        self.captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&%s' % random.random()
        self.text = ""
        self.user = self.config_data["set"]["12306count"][0]["uesr"]
        self.passwd = self.config_data["set"]["12306count"][1]["pwd"]
        self.aotu_code_type = self.config_data['aotu_code_type']

        self.s = self.create_session()

    def create_session(self):
        s = HTTPClient()
        return s.session

    def get_logincookies(self):
        global login_cookies, randCode
        init_url = "https://kyfw.12306.cn/otn/login/init"
        uamtk_data = {'appid': 'otn'}
        httpZF_url = "https://kyfw.12306.cn/otn/HttpZF/logdevice?algID=i8UYSfDgWt&hashCode=td9I6c9a9k73Jv8Nc2ie0FGZWit-S-0MQJfASXNUQmk&FMQw=0&q4f3=zh-CN&VySQ=FGFKKeD8kVn5VC6vc-6l42-GJzul0oeM&VPIf=1&custID=133&VEek=unknown&dzuS=0&yD16=0&EOQP=c227b88b01f5c513710d4b9f16a5ce52&lEnu=2886927661&jp76=e237f9703f53d448d77c858b634154a5&hAqN=MacIntel&platform=WEB&ks0Q=b9a555dce60346a48de933b3e16ebd6e&TeRS=877x1440&tOHY=24xx900x1440&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew=Mozilla/5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_13_2)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/63.0.3239.132%20Safari/537.36&E3gR=ea438f8fd5bf8a3ac1fe9bd188f2c823&timestamp=1516195328849"
        captcha_check_url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        uamtk_url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        login_url = "https://kyfw.12306.cn/passport/web/login"
        login_userLogin = "https://kyfw.12306.cn/otn/login/userLogin"
        #userLogin = "https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin"
        uamauthclient = "https://kyfw.12306.cn/otn/uamauthclient"

        self.s.get(init_url, verify=False)
        self.s.post(uamtk_url, data=uamtk_data, verify=False)
        content = self.s.get(httpZF_url, verify=False).content
        content = content.decode(encoding='utf-8').split("'")[1]
        d = json.loads(content)

        requests.utils.add_dict_to_cookiejar(
            self.s.cookies, {"RAIL_DEVICEID": d['dfp']})
        #requests.utils.add_dict_to_cookiejar(self.s.cookies, {"RAIL_DEVICEID": 'XHe6FfHQKdYj65DI8SswKR16VuCcV5nT8G62Uyj0uiGpChNOindm0SNWaPvgL2_obrOdD22vuuZf1WmTDAERbW1IRBdpJVAaKYA8Ks9FOVufsrLZ2ccVy3g5XdNQIyXrjmk-psvlj7TSvHrcpUVcvlQd2cn5qEp7'})
        requests.utils.add_dict_to_cookiejar(
            self.s.cookies, {"RAIL_EXPIRATION": d['exp']})
        requests.utils.add_dict_to_cookiejar(
            self.s.cookies, {"_jc_save_fromDate": '2018-01-27'})
        requests.utils.add_dict_to_cookiejar(
            self.s.cookies, {"_jc_save_toStation": '%u5170%u5DDE%u897F%2CLAJ'})
        requests.utils.add_dict_to_cookiejar(
            self.s.cookies, {"_jc_save_toDate": '2018-01-22'})
        requests.utils.add_dict_to_cookiejar(
            self.s.cookies, {"_jc_save_wfdc_flag": 'dc'})
        requests.utils.add_dict_to_cookiejar(
            self.s.cookies, {"_jc_save_fromStation": '%u4E0A%u6D77%u8679%u6865%2CAOH'})
        randCode = self.readImg(self.captcha_url)
        randdata = {"answer": randCode,
                    "login_site": "E",
                    "rand": "sjrand"}
        login_data = {"username": self.user,
                      "password": self.passwd,
                      "appid": "otn"}
        rand_result = self.s.post(
            captcha_check_url, data=randdata, verify=False).json()
        print(rand_result)
        while rand_result['result_code'] is not '4':
            randCode = self.readImg(self.captcha_url)
            randdata = {"answer": randCode,
                        "login_site": "E",
                        "rand": "sjrand"}
            rand_result = self.s.post(
                captcha_check_url, data=randdata, verify=False).json()
            print(rand_result)

        login_result = self.s.post(
            login_url, allow_redirects=False, data=login_data, verify=False)
        login_code = login_result.status_code
        print(login_code)
        # 解决登录接口302重定向问题
        while login_code == 302:

            login_result = self.s.post(
                login_url, allow_redirects=False, data=login_data, verify=False)
            login_code = login_result.status_code
            print('Login redirect...')
            if login_code == 200:
                print('登录成功', login_result.json())
        login_userLogin_data = {'_json_att': ''}
        self.s.post(login_userLogin, data=login_userLogin_data, verify=False)
        uamtk_result = self.s.post(
            uamtk_url, data=uamtk_data, verify=False).json()
        # print(uamtk_result)
        uamauthclient_data = {'tk': uamtk_result['newapptk']}
        uamauthclient_result = self.s.post(
            uamauthclient, data=uamauthclient_data, verify=False).json()
        # print(uamauthclient_result)
        login_cookies = self.s.cookies.get_dict()
        print('Get Login Cookie Finish.')
        return login_cookies

    def get_randcode(self):
        print("下载验证码...")
        img_path = './tkcode'
        r = self.s.get(self.captcha_url,  verify=False)
        result = r.content
        # print(result)
        randCode = ''
        try:
            open(img_path, 'wb').write(result)
            if self.config_data["is_aotu_code"]:
                randCode = DamatuApi(self.config_data["damatu"]["uesr"],
                                     self.config_data["damatu"]["pwd"], img_path).main()

            else:
                img = Image.open('./tkcode')
                img.show()
                randCode = self.codexy()
        except OSError as e:
            traceback.print_exc()
        return randCode
    # def cookietp(self):
    #     global initcookies
    #     self.stoidinput("获取Cookie")
    #     Url = "https://kyfw.12306.cn/otn/login/init"
    #     initcookies1 = myurllib2.myrequests(cookies=None).get(Url).cookies
    #     initcookies1 = initcookies1.get_dict()
    #     #initcookies['current_captcha_type'] = "Z"
    #     print(initcookies1)
    #     uamtk_url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
    #     uamtk_data = {'appid':'otn'}
    #     initcookies2 = myurllib2.myrequests(cookies=initcookies1).post(uamtk_url,data=uamtk_data).cookies
    #     initcookies2 = initcookies2.get_dict()
    #     print(initcookies2)
    #     captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&%s' % random.random()
    #     initcookies3 = myurllib2.myrequests(cookies=None).get(captcha_url).cookies
    #     initcookies3 = initcookies3.get_dict()
    #     initcookies = dict(initcookies3, **initcookies2,**initcookies1)
    #     print(initcookies3)
    #     print(initcookies)
    #     return initcookies
        # for index, c in enumerate(myurllib2.cookiejar):
        #     stoidinput(c)

    def readImg(self, code_url):
        """
        增加手动打码，只是登录接口，完全不用担心提交订单效率
        思路
        1.调用PIL显示图片
        2.图片位置说明，验证码图片中每个图片代表一个下标，依次类推，1，2，3，4，5，6，7，8
        3.控制台输入对应下标，按照英文逗号分开，即可手动完成打码，
        :return:
        """
        print ("下载验证码...")
        codeimgUrl = code_url
        img_path = './tkcode'
        r = self.s.get(codeimgUrl,  verify=False)
        result = r.content
        # if "message" in result:
        #     print("验证码下载失败，正在重试")
        # else:
        try:
            open(img_path, 'wb').write(result)
            if self.aotu_code_type == 1:
                return DamatuApi(self.config_data["damatu"]["uesr"], self.config_data["damatu"]["pwd"], img_path).main()

            elif self.aotu_code_type == 2:
                rc = RClient(
                    self.config_data["ruokuai"]["uesr"], self.config_data["ruokuai"]["pwd"])
                im = open('./tkcode', 'rb').read()
                Result = rc.rk_create(im, 6113)
                if "Result" in Result:
                    return self.codexy(Ofset=",".join(list(Result["Result"])), is_raw_input=False)
                else:
                    if "Error" in Result and Result["Error"]:
                        print(Result["Error"])
                        return ""
            else:
                img = Image.open('./tkcode')
                img.show()
                return self.codexy()
        except OSError as e:
            print (e)
            return ""

    def codexy(self, Ofset = None, is_raw_input=True):
        """
        获取验证码
        :return: str
        """
        if is_raw_input :
            Ofset = input("请输入验证码: ")
        select = Ofset.split(',')
        #global randCode
        post = []
        offsetsX = 0  # 选择的答案的left值,通过浏览器点击8个小图的中点得到的,这样基本没问题
        offsetsY = 0  # 选择的答案的top值
        for ofset in select:
            if ofset == '1':
                offsetsY = 46
                offsetsX = 42
            elif ofset == '2':
                offsetsY = 46
                offsetsX = 105
            elif ofset == '3':
                offsetsY = 45
                offsetsX = 184
            elif ofset == '4':
                offsetsY = 48
                offsetsX = 256
            elif ofset == '5':
                offsetsY = 36
                offsetsX = 117
            elif ofset == '6':
                offsetsY = 112
                offsetsX = 115
            elif ofset == '7':
                offsetsY = 114
                offsetsX = 181
            elif ofset == '8':
                offsetsY = 111
                offsetsX = 252
            else:
                pass
            post.append(offsetsX)
            post.append(offsetsY)
        randCode = str(post).replace(']', '').replace(
            '[', '').replace("'", '').replace(' ', '')

        print("验证码识别坐标为{0}".format(randCode))
        return randCode

    def login(self):
        while True:
            try:
                self.get_logincookies()
                gol._init()
                gol.set_value('s', self.s)
                break
            except (requests.exceptions.ConnectionError, RemoteDisconnected) as e:
                traceback.print_exc()
                sleep_interval = 60 * 5
                print(f'IP可能被封掉，打算睡一觉 {sleep_interval}ms')
                time.sleep(60 * 5)

            except IndexError as e:
                traceback.print_exc()
    #
    # def getUserinfo(self):
    #     """
    #     登录成功后,显示用户名
    #     :return:
    #     """
    #     url = 'https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfo'
    #     data = dict(_json_att=None)
    #     #result = myurllib2.myrequests().post(url, data).decode('utf-8')
    #     result = self.s.post(url,data=data,verify=False).content
    #     userinfo = result
    #     name = r'<input name="userDTO.loginUserDTO.user_name" style="display:none;" type="text" value="(\S+)" />'
    #     try:
    #         self.stoidinput("欢迎 %s 登录" % re.search(name, result).group(1))
    #     except AttributeError:
    #         pass

    def logout(self):
        url = 'https://kyfw.12306.cn/otn/login/loginOut'
        result = self.s.get(url, verify=False).json()
        if result:
            self.stoidinput("已退出")
        else:
            self.errorinput("退出失败")


if __name__ == "__main__":
    go_login.login()
    # logout()
