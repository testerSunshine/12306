#!/bin/env python
# -*- coding=utf-8 -*-
import random
import json
import re
import socket
from time import sleep

from config.ticketConf import _get_yaml
from PIL import Image
from damatuCode.damatuWeb import DamatuApi
from damatuCode.ruokuai import RClient
from myException.UserPasswordException import UserPasswordException
from myException.balanceException import balanceException
from myUrllib.httpUtils import session as SESS
from config.urlConf import urls

class GoLogin:
    #def __init__(self,  httpClint, urlConf, is_aotu_code, aotu_code_type):
    def __init__(self, sys_config):
        self.sys_config =  _get_yaml( sys_config)
        self.urlConf = urls
        self.s = SESS 

    def cookietp(self):
        print("正在获取cookie")
        url = self.urlConf["loginInit"]["req_url"]
        self.s.get(url)
        # Url = "https://kyfw.12306.cn/otn/login/init"
        # myurllib2.get(Url)
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
        result = self.s.get(codeimgUrl)
        if "message" in result:
            print("验证码下载失败，正在重试")
        else:
            try:
                open(img_path, 'wb').write(result.content)
                if self.sys_config['is_aotu_code']:
                    if self.sys_config['auto_code_type'] == 1:
                        return DamatuApi(self.sys_config["damatu"]["uesr"], self.sys_config["damatu"]["pwd"], img_path).main()
                    elif self.sys_config['auto_code_type']== 2:
                        rc = RClient(self.sys_config["ruokuai"]["uesr"], self.sys_config["ruokuai"]["pwd"])
                        im = open('./tkcode', 'rb').read()
                        Result = rc.rk_create(im, 6113)
                        if "Result" in Result:
                            return self.codexy(Ofset=",".join(list(Result["Result"])), is_raw_input=False)
                        else:
                            if "Error" in Result and Result["Error"]:
                                print (Result["Error"])
                                return ""
                else:
                    img = Image.open('./tkcode')
                    img.show()
                    return self.codexy()
            except OSError as e:
                print (e)
                return ""

    def codexy(self, Ofset=None, is_raw_input=True):
        """
        获取验证码
        :return: str
        """
        if is_raw_input:
            Ofset = raw_input("请输入验证码: ")
        select = Ofset.split(',')
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
        randCode = str(post).replace(']', '').replace('[', '').replace("'", '').replace(' ', '')
        print("验证码识别坐标为{0}".format(randCode))
        return randCode

    def auth(self):
        """认证"""
        authUrl = self.urlConf["auth"]["req_url"]
        authData = {"appid": "otn"}
        tk = self.s.post(authUrl, authData).json()
        return tk

    def codeCheck(self):
        """
        验证码校验
        :return:
        """
        codeCheck = self.urlConf["codeCheck"]["req_url"]
        codeCheckData = {
            "answer": self.randCode,
            "rand": "sjrand",
            "login_site": "E"
        }
        fresult = self.s.post(codeCheck, codeCheckData).json()
        if "result_code" in fresult and fresult["result_code"] == "4":
            print ("验证码通过,开始登录..")
            return True
        else:
            if "result_message" in fresult:
                print(fresult["result_message"])
            sleep(1)
            self.s.cookies.clear()

    def baseLogin(self, user, passwd):
        """
        登录过程
        :param user:
        :param passwd:
        :return: 权限校验码
        """
        logurl = self.urlConf["login"]["req_url"]
        logData = {
            "username": user,
            "password": passwd,
            "appid": "otn"
        }
        tresult = self.s.post(logurl, logData).json()
        if 'result_code' in tresult and tresult["result_code"] == 0:
            print ("登录成功")
            tk = self.auth()
            if "newapptk" in tk and tk["newapptk"]:
                return tk["newapptk"]
            else:
                return False
        elif 'result_message' in tresult and tresult['result_message']:
            messages = tresult['result_message']
            if messages.find("密码输入错误") is not -1:
                raise UserPasswordException("{0}".format(messages))
            else:
                print ("登录失败: {0}".format(messages))
                print ("尝试重新登陆")
                return False
        else:
            return False

    def getUserName(self, uamtk):
        """
        登录成功后,显示用户名
        :return:
        """
        if not uamtk:
            return "权限校验码不能为空"
        else:
            uamauthclientUrl = self.urlConf["uamauthclient"]["req_url"]
            data = {"tk": uamtk}
            uamauthclientResult = self.s.post(uamauthclientUrl, data).json()
            if uamauthclientResult:
                if "result_code" in uamauthclientResult and uamauthclientResult["result_code"] == 0:
                    print("欢迎 {} 登录".format(uamauthclientResult["username"]))
                    return True
                else:
                    return False
            else:
                self.s.post(uamauthclientUrl, data)
                url = self.urlConf["getUserInfo"]["req_url"]
                self.s.get(url)

    def go_login(self):
        """
        登陆
        :param user: 账户名
        :param passwd: 密码
        :return:
        """
        if self.sys_config['is_aotu_code'] and self.sys_config['auto_code_type'] == 1:
            balance = DamatuApi(self.sys_config["damatu"]["uesr"], self.sys_config["damatu"]["pwd"]).getBalance()
            if int(balance) < 40:
                raise balanceException('余额不足，当前余额为: {}'.format(balance))
        user, passwd = self.sys_config["set"]["12306count"][0]["uesr"], self.sys_config["set"]["12306count"][1]["pwd"]
        if not user or not passwd:
            raise UserPasswordException("温馨提示: 用户名或者密码为空，请仔细检查")
        login_num = 0
        while True:
            print('Login')
            self.cookietp()

            cookies= dict(_jc_save_wfdc_flag="dc", _jc_save_fromStation="%u4E0A%u6D77%u8679%u6865%2CAOH", _jc_save_toStation="%u5170%u5DDE%u897F%2CLAJ", _jc_save_fromDate="2018-02-14", _jc_save_toDate="2018-01-16", RAIL_DEVICEID="EN_3_EGSe2GWGHXJeCkFQ52kHvNCrNlkz9n1GOqqQ1wR0i98WsD8Gj-a3YHZ-XYKeESWgCiJyyucgSwkFOzVHhHqfpidLPcm2vK9n83uzOPuShO3Pl4lCydAtQu4BdFqz-RVmiduNFixrcrN_Ny43135JiEtqLaI")
           
            for k, v in cookies.items():
                self.s.cookies.set(k, v) 
            self.randCode = self.readImg(self.urlConf["getCodeImg"]["req_url"])
            
            login_num += 1
            self.auth()
            if self.codeCheck():
                uamtk = self.baseLogin(user, passwd)
                if uamtk:
                    self.getUserName(uamtk)
                    print ('LoginFinish')
                    break
        print('break')

    def logout(self):
        url = 'https://kyfw.12306.cn/otn/login/loginOut'
        result = myurllib2.get(url)
        if result:
            print ("已退出")
        else:
            print ("退出失败")


# if __name__ == "__main__":
#     # main()
#     # logout()