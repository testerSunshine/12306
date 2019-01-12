# -*- coding: utf-8 -*-
__author__ = 'fbigun'

import requests
from collections import OrderedDict

from config.ticketConf import _get_yaml


def voiceCall():
    """
    电话语音播报
    :param str: voice content
    :return:
    """
    voiceNotify = _get_yaml()
    is_call= voiceNotify["MBVoiceNotify"]["is_call"]
    if is_call:
        appcode = voiceNotify["MBVoiceNotify"]["appcode"]
        phone = voiceNotify["MBVoiceNotify"]["phone"]
        templateId = voiceNotify["MBVoiceNotify"]["templateId"]

        path = '/mobai_voicenotifysms'
        host = 'http://mbyytz.market.alicloudapi.com'
        payload = OrderedDict([('param','param'), ('phone',phone), ('templateId',templateId)])
        headers = { 'Authorization': 'APPCODE '+appcode }
        try:
            rsp = requests.post(host+path, params=payload, headers=headers)
            rsp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(u"参数错误导致访问出错错误为： {}".format(e))
        except Exception as e:
            print(u"连接语音电话通知的网络不可达错误为： {}".format(e))
        else:
            receipt = rsp.json()
            if receipt['return_code'] == '00000':
                print(u'语音呼叫已成功通知，请查收')
            else:
                print(u'语音呼叫失败，返回的错误码为: {}'.format(receipt['return_code']))

if __name__ == '__main__':
    voiceCall()
