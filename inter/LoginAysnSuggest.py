# coding=utf-8
from config.urlConf import urls


def loginAysnSuggest(session, username, password):
    """
    登录接口
    ps: 不需要验证码
    :return:
    """
    loginAysnSuggestUrls = urls.get("loginAysnSuggest")
    data = {
        "loginUserDTO.user_name": username,
        "userDTO.password":	password
    }
    loginAysnSuggestRsp = session.httpClint.send(urls=loginAysnSuggestUrls, data=data)
    if loginAysnSuggestRsp and loginAysnSuggestRsp.get("httpstatus") is 200 and loginAysnSuggestRsp.get("data", {}).get("loginCheck") == "Y":
        print(u"登录成功")
    else:
        print(u"登录失败, {0} {1}".format("".join(loginAysnSuggestRsp.get("messages")), loginAysnSuggestRsp.get("validateMessages")))
