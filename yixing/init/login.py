#!/bin/env python
# -*- coding=utf-8 -*-
import random
import json
import re
from time import sleep
from yixing.config.ticketConf import _get_yaml


from yixing.damatuCode.damatuWeb import DamatuApi
from yixing.myUrllib import myurllib2

codeimg = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&%s' % random.random()


def cookietp():
    stoidinput("获取Cookie")
    Url = "https://kyfw.12306.cn/otn/login/init"
    myurllib2.get(Url)
    # for index, c in enumerate(myurllib2.cookiejar):
    #     stoidinput(c)


def readImg():
    global randCode
    stoidinput("下载验证码...")
    img_path = './tkcode'
    result = myurllib2.get(codeimg)
    try:
        open(img_path, 'wb').write(result)
        randCode = DamatuApi(_get_yaml()["damatu"]["uesr"], _get_yaml()["damatu"]["pwd"], img_path).main()
    except OSError as e:
        print (e)
        pass


def stoidinput(text):
    """
    正常信息输出
    :param text:
    :return:
    """
    print "\033[34m[*]\033[0m %s " % text


def errorinput(text):
    """
    错误信息输出
    :param text:
    :return:
    """
    print "\033[32m[!]\033[0m %s " % text
    return False


# def codexy():
#     """
#     获取验证码
#     :return: str
#     """
#
#     Ofset = raw_input("[*] 请输入验证码: ")
#     select = Ofset.split(',')
#     global randCode
#     post = []
#     offsetsX = 0  # 选择的答案的left值,通过浏览器点击8个小图的中点得到的,这样基本没问题
#     offsetsY = 0  # 选择的答案的top值
#     for ofset in select:
#         if ofset == '1':
#             offsetsY = 46
#             offsetsX = 42
#         elif ofset == '2':
#             offsetsY = 46
#             offsetsX = 105
#         elif ofset == '3':
#             offsetsY = 45
#             offsetsX = 184
#         elif ofset == '4':
#             offsetsY = 48
#             offsetsX = 256
#         elif ofset == '5':
#             offsetsY = 36
#             offsetsX = 117
#         elif ofset == '6':
#             offsetsY = 112
#             offsetsX = 115
#         elif ofset == '7':
#             offsetsY = 114
#             offsetsX = 181
#         elif ofset == '8':
#             offsetsY = 111
#             offsetsX = 252
#         else:
#             pass
#         post.append(offsetsX)
#         post.append(offsetsY)
#     randCode = str(post).replace(']', '').replace('[', '').replace("'", '').replace(' ', '')


def login(user, passwd):
    """
    登陆
    :param user: 账户名
    :param passwd: 密码
    :return: 
    """
    login_num = 0
    while True:
        cookietp()
        readImg()
        login_num += 1
        randurl = 'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn'
        logurl = 'https://kyfw.12306.cn/otn/login/loginAysnSuggest'
        surl = 'https://kyfw.12306.cn/otn/login/userLogin'
        randdata = {
            "randCode": randCode,
            "rand": "sjrand"
        }
        logdata = {
            "loginUserDTO.user_name": user,
            "userDTO.password": passwd,
            "randCode": randCode
        }
        ldata = {
            "_json_att": None
        }
        fresult = json.loads(myurllib2.Post(randurl, randdata), encoding='utf8')
        checkcode = fresult['data']['msg']
        if checkcode == 'FALSE':
            errorinput("验证码有误,第{}次尝试重试".format(login_num))
        else:
            stoidinput("验证码通过,开始登录..")
            sleep(1)
            try:
                tresult = json.loads(myurllib2.Post(logurl, logdata), encoding='utf8')
                if 'data' not in tresult:
                    errorinput("登录失败: %s" % tresult['messages'][0])
                # elif "messages" in tresult and tresult["messages"][0].find("密码输入错误") is not -1:
                #     errorinput("登陆失败：{}".format(tresult["messages"][0]))
                #     break
                elif 'messages' in tresult and tresult['messages']:
                    messages = tresult['messages'][0]
                    if messages.find("密码输入错误") is not -1:
                        errorinput("登陆失败：{}".format(tresult["messages"][0]))
                        break
                    else:
                        errorinput("登录失败: %s" % tresult['messages'][0])
                        stoidinput("尝试重新登陆")
                else:
                    stoidinput("登录成功")
                    myurllib2.Post(surl, ldata)
                    getUserinfo()
                    break
            except ValueError as e:
                errorinput(e)
        sleep(1)


def getUserinfo():
    """
    登录成功后,显示用户名
    :return:
    """
    url = 'https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfo'
    data = dict(_json_att=None)
    result = myurllib2.Post(url, data)
    userinfo = result
    name = r'<input name="userDTO.loginUserDTO.user_name" style="display:none;" type="text" value="(\S+)" />'
    try:
        stoidinput("欢迎 %s 登录" % re.search(name, result).group(1))
    except AttributeError:
        pass


def main():
    login(_get_yaml()["12306count"]["uesr"], _get_yaml()["12306count"]["pwd"])


def logout():
    url = 'https://kyfw.12306.cn/otn/login/loginOut'
    result = myurllib2.get(url)
    if result:
        stoidinput("已退出")
    else:
        errorinput("退出失败")


if __name__ == "__main__":
    main()
    # logout()