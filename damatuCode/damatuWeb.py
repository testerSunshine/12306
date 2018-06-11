# -*- coding=utf-8 -*-

import hashlib
import json
import base64
import requests

from myException.balanceException import balanceException


def md5str(str):  # md5加密字符串
    m = hashlib.md5(str.encode(encoding="utf-8"))
    return m.hexdigest()


def md5(byte):  # md5加密byte
    return hashlib.md5(byte).hexdigest()


class DamatuApi():
    ID = '40838'
    KEY = 'ca9507e17e8d5ddf7c57cd18d8d33010'
    HOST = 'http://api.dama2.com:7766/app/'

    def __init__(self, username, password, file_path=None):
        self.username = username
        self.password = password
        self.file_path = file_path

    def getSign(self, param=b''):
        return (md5(bytes(self.KEY) + bytes(self.username) + param))[:8]

    def getPwd(self):
        return md5str(self.KEY + md5str(md5str(self.username) + md5str(self.password)))

    def post(self, path, params={}):
        data = params
        url = self.HOST + path
        response = requests.post(url, data)
        return response.content

    # 查询余额 return 是正数为余额 如果为负数 则为错误码
    def getBalance(self):
        data = {'appID': self.ID,
                'user': self.username,
                'pwd': self.getPwd(),
                'sign': self.getSign()
                }
        res = self.post('d2Balance', data)
        res = str(res)
        jres = json.loads(res)
        if jres['ret'] == 0:
            return jres['balance']
        else:
            return jres['ret']

    # 上传验证码 参数filePath 验证码图片路径 如d:/1.jpg type是类型，查看http://wiki.dama2.com/index.php?n=ApiDoc.Pricedesc  return 是答案为成功 如果为负数 则为错误码
    def decode(self, type):
        f = open(self.file_path, 'rb')
        fdata = f.read()
        filedata = base64.b64encode(fdata)
        f.close()
        data = {'appID': self.ID,
                'user': self.username,
                'pwd': self.getPwd(),
                'type': type,
                'fileDataBase64': filedata,
                'sign': self.getSign(fdata)
                }
        res = self.post('d2File', data)
        res = str(res)
        jres = json.loads(res)
        if jres['ret'] == 0:
            # 注意这个json里面有ret，id，result，cookie，根据自己的需要获取
            return jres['result']
        else:
            return jres['ret']

    # url地址打码 参数 url地址  type是类型(类型查看http://wiki.dama2.com/index.php?n=ApiDoc.Pricedesc) return 是答案为成功 如果为负数 则为错误码
    def decodeUrl(self, url, type):
        data = {'appID': self.ID,
                'user': self.username,
                'pwd': self.getPwd(),
                'type': type,
                'url': url,
                'sign': self.getSign(url.encode(encoding="utf-8"))
                }
        res = self.post('d2Url', data)
        res = str(res,)
        jres = json.loads(res)
        if jres['ret'] == 0:
            # 注意这个json里面有ret，id，result，cookie，根据自己的需要获取
            return (jres['result'])
        else:
            return jres['ret']

    # 报错 参数id(string类型)由上传打码函数的结果获得 return 0为成功 其他见错误码
    def reportError(self, id):
        data = {'appID': self.ID,
                'user': self.username,
                'pwd': self.getPwd(),
                'id': id,
                'sign': self.getSign(id.encode(encoding="utf-8"))
                }
        res = self.post('d2ReportError', data)
        res = str(res)
        jres = json.loads(res)
        return jres['ret']

    def main(self):
        result = self.decode(287)
        img_code = result.replace('|', ',') if not isinstance(result, int) else ""
        print("验证码识别坐标为{0}".format(img_code))
        return img_code

# # 调用类型实例：
# # 1.实例化类型 参数是打码兔用户账号和密码
# dmt = DamatuApi("wenxianping", "wen1995")
# # 2.调用方法：
# print(dmt.getBalance())  # 查询余额
# print(dmt.decode('tkcode', 287))  # 上传打码
# # print(dmt.decodeUrl('https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.7586344633015405', 310))  # 上传打码
# # print(dmt.reportError('894657096')) # 上报错误
