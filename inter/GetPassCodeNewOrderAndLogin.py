# coding=utf-8
import copy
import random
import time


def getPassCodeNewOrderAndLogin(session, imgType):
    """
    下载验证码
    :param session:
    :param imgType: 下载验证码类型，login=登录验证码，其余为订单验证码
    :return:
    """
    if imgType == "login":
        codeImgUrl = copy.deepcopy(session.urls["getCodeImg"])
        codeImgUrl["req_url"] = codeImgUrl["req_url"].format(random.random())
    else:
        codeImgUrl = copy.deepcopy(session.urls["codeImgByOrder"])
        codeImgUrl["req_url"] = codeImgUrl["req_url"].format(random.random())
    print(u"下载验证码...")
    img_path = './tkcode.png'
    result = session.httpClint.send(codeImgUrl)
    try:
        if isinstance(result, dict):
            print(u"下载验证码失败, 请手动检查是否ip被封，或者重试，请求地址：https://kyfw.12306.cn{}".format(codeImgUrl.get("req_url")))
            return False
        else:
            print(u"下载验证码成功")
            try:
                with open(img_path, 'wb', encoding="utf-8") as img:
                    img.write(result)
            except Exception:
                with open(img_path, 'wb') as img:
                    img.write(result)
            return result
    except OSError:
        print(u"验证码下载失败，可能ip被封，确认请手动请求: {0}".format(codeImgUrl))
