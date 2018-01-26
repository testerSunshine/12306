#!/bin/env python
# -*- coding=utf-8 -*-
import random
import json
import re
from time import sleep

from config.ticketConf import _get_yaml
from PIL import Image
from damatuCode.damatuWeb import DamatuApi
import requests
from init import gol
import traceback
from http.client import RemoteDisconnected
import time
from myUrllib.httpUtils  import HTTPClient


class go_login:
    def __init__(self, ticket_config=""):
        self.captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&%s' % random.random()
        self.ticket_config = ticket_config
        self.text = ""
        self.user = _get_yaml(ticket_config)["set"]["12306count"][0]["uesr"]
        self.passwd = _get_yaml(ticket_config)["set"]["12306count"][1]["pwd"]

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
        
        self.s.get(init_url ,verify=False)
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
        randCode = self.get_randcode()
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
            randCode = self.get_randcode()
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
                print('登录成功' , login_result.json())
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
        self.stoidinput("下载验证码...")
        img_path = './tkcode'
        r = self.s.get(self.captcha_url,  verify=False)
        result = r.content
        # print(result)
        randCode = ''
        try:
            open(img_path, 'wb').write(result)
            if _get_yaml(self.ticket_config)["is_aotu_code"]:
                randCode = DamatuApi(_get_yaml(self.ticket_config)["damatu"]["uesr"],
                                     _get_yaml(self.ticket_config)["damatu"]["pwd"], img_path).main()

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

    # def readImg(self):
    #     """
    #     增加手动打码，只是登录接口，完全不用担心提交订单效率
    #     思路
    #     1.调用PIL显示图片
    #     2.图片位置说明，验证码图片中每个图片代表一个下标，依次类推，1，2，3，4，5，6，7，8
    #     3.控制台输入对应下标，按照英文逗号分开，即可手动完成打码，
    #     :return:
    #     """
    #
    #     #global randCode
    #     self.stoidinput("下载验证码...")
    #     img_path = './tkcode'
    #     r = s.get(self.captcha_url, verify=False)
    #     captcha_cookie = r.cookies.get_dict()
    #     result = r.content
    #     #print(result)
    #     try:
    #         open(img_path, 'wb').write(result)
    #         if _get_yaml(self.ticket_config)["is_aotu_code"]:
    #             #print(_get_yaml(self.ticket_config)["damatu"]["uesr"])
    #             randCode = DamatuApi(_get_yaml(self.ticket_config)["damatu"]["uesr"], _get_yaml(self.ticket_config)["damatu"]["pwd"], img_path).main()
    #         else:
    #             img = Image.open('./tkcode')
    #             img.show()
    #             self.codexy()
    #     except OSError as e:
    #         print (e)
    #         pass
    #     return randCode

    def stoidinput(self, text):
        """
        正常信息输出
        :param text:
        :return:
        """
        print("\033[34m[*]\033[0m %s " % text)

    def errorinput(self, text):
        """
        错误信息输出
        :param text:
        :return:
        """
        print("\033[32m[!]\033[0m %s " % text)
        return False

    def codexy(self):
        """
        获取验证码
        :return: str
        """
        global randCode
        Ofset = input("[*] 请输入验证码: ")
        select = Ofset.split(',')
        #global randCode
        post = []
        offsetsX = 0  # 选择的答案的left值,通过浏览器点击8个小图的中点得到的,这样基本没问题
        offsetsY = 0  # 选择的答案的top值
        for ofset in select:
            if ofset == '1':
                offsetsY = 41
                offsetsX = 39
            elif ofset == '2':
                offsetsY = 44
                offsetsX = 110
            elif ofset == '3':
                offsetsY = 49
                offsetsX = 184
            elif ofset == '4':
                offsetsY = 45
                offsetsX = 253
            elif ofset == '5':
                offsetsY = 116
                offsetsX = 39
            elif ofset == '6':
                offsetsY = 113
                offsetsX = 110
            elif ofset == '7':
                offsetsY = 120
                offsetsX = 184
            elif ofset == '8':
                offsetsY = 121
                offsetsX = 257
            else:
                pass
            post.append(offsetsX)
            post.append(offsetsY)
        randCode = str(post).replace(']', '').replace(
            '[', '').replace("'", '').replace(' ', '')
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
                time.sleep(60 *5)

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
