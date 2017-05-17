#!/bin/env python
# -*- coding=utf-8 -*-
import random
import json
import re
from damatuCode.damatuWeb import DamatuApi
from myUrllib import myurllib2

codeimg = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&%s' % random.random()
# 931128603@qq.com
baner = """
##################################
    12306登录脚本,作者Mr RJL
    python版本:2.7,适用于linux
    验证码输入方式:
    输入问题对应的图片序号,1-8;
    多个以','分隔.如:1,2,3
##################################
"""


def cookietp():
    stoidinput("获取Cookie")
    Url = "https://kyfw.12306.cn/otn/login/init"
    myurllib2.get(Url)
    for index, c in enumerate(myurllib2.cookiejar):
        stoidinput(c)


def readImg():
    global randCode
    stoidinput("下载验证码...")
    img_path = '/tmp/tkcode'
    result = myurllib2.get(codeimg)
    try:
        open(img_path, 'wb').write(result)
        randCode = DamatuApi('wenxianping', 'wen1995', img_path).main()
    except OSError as e:
        print e
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
    randurl = 'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn'
    logurl = 'https://kyfw.12306.cn/otn/login/loginAysnSuggest'
    surl = 'https://kyfw.12306.cn/otn/login/userLogin'
    geturl = 'https://kyfw.12306.cn/otn/index/initMy12306'
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
        errorinput("验证码有误,第%s次尝试重试" )
    else:
        stoidinput("验证码通过,开始登录..")
        try:
            tresult = json.loads(myurllib2.Post(logurl, logdata), encoding='utf8')
            if tresult['data'].__len__() == 0:
                errorinput("登录失败: %s" % tresult['messages'][0])
            else:

                stoidinput("登录成功")
                myurllib2.Post(surl, ldata)
                getUserinfo()
        except ValueError as e:
            errorinput(e)


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
    cookietp()
    readImg()
    login('931128603@qq.com', 'QWERTY')


def logout():
    url = 'https://kyfw.12306.cn/otn/login/loginOut'
    result = myurllib2.get(url)
    if result:
        stoidinput("已退出")
    else:
        errorinput("退出失败")


if __name__ == "__main__":
    print baner
    main()
    # logout()