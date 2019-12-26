# coding=utf-8
from PIL import Image

from config.urlConf import urls
from myUrllib.httpUtils import HTTPClient
from verify.localVerifyCode import Verify
import TickerConfig
import os


if TickerConfig.AUTO_CODE_TYPE == 2:
    v = Verify()


def getRandCode(is_auto_code, auto_code_type, result):
    """
    识别验证码
    :return: 坐标
    """
    try:
        if is_auto_code:
            if auto_code_type == 1:
                print(u"打码兔已关闭, 如需使用自动识别，请使用如果平台 auto_code_type == 2")
                return
            elif auto_code_type == 2:
                Result = v.verify(result)
                return codexy(Ofset=Result, is_raw_input=False)
            elif auto_code_type == 3:
                print("您已设置使用云打码，但是服务器资源有限，请尽快改为本地打码" if "CAPTCHALOCAL" not in os.environ else "已设置本地打码服务器")
                http = HTTPClient(0)
                Result = http.send(urls.get("autoVerifyImage"), {"imageFile": result})
                if Result and Result.get("code") is 0:
                    return codexy(Ofset=Result.get("data"), is_raw_input=False)
        else:
            img = Image.open('./tkcode.png')
            img.show()
            return codexy()
    except Exception as e:
        print(e)


def codexy(Ofset=None, is_raw_input=True):
    """
    获取验证码
    :return: str
    """
    if is_raw_input:
        print(u"""
            *****************
            | 1 | 2 | 3 | 4 |
            *****************
            | 5 | 6 | 7 | 8 |
            *****************
            """)
        print(u"验证码分为8个，对应上面数字，例如第一和第二张，输入1, 2  如果开启cdn查询的话，会冲掉提示，直接鼠标点击命令行获取焦点，输入即可，不要输入空格")
        print(u"如果是linux无图形界面，请使用自动打码，is_auto_code: True")
        print(u"如果没有弹出验证码，请手动双击根目录下的tkcode.png文件")
        Ofset = input(u"输入对应的验证码: ")
    if isinstance(Ofset, list):
        select = Ofset
    else:
        Ofset = Ofset.replace("，", ",")
        select = Ofset.split(',')
    post = []
    offsetsX = 0  # 选择的答案的left值,通过浏览器点击8个小图的中点得到的,这样基本没问题
    offsetsY = 0  # 选择的答案的top值
    for ofset in select:
        if ofset == '1':
            offsetsY = 77
            offsetsX = 40
        elif ofset == '2':
            offsetsY = 77
            offsetsX = 112
        elif ofset == '3':
            offsetsY = 77
            offsetsX = 184
        elif ofset == '4':
            offsetsY = 77
            offsetsX = 256
        elif ofset == '5':
            offsetsY = 149
            offsetsX = 40
        elif ofset == '6':
            offsetsY = 149
            offsetsX = 112
        elif ofset == '7':
            offsetsY = 149
            offsetsX = 184
        elif ofset == '8':
            offsetsY = 149
            offsetsX = 256
        else:
            pass
        post.append(offsetsX)
        post.append(offsetsY)
    randCode = str(post).replace(']', '').replace('[', '').replace("'", '').replace(' ', '')
    print(u"验证码识别坐标为{0}".format(randCode))
    return randCode
