#coding=utf-8
from browser.baseEntity import BaseRequest, BaseResponse
import requests
import sys,re
import os

class Response_Web(BaseResponse):
    pass

class Request_Web(BaseRequest):    

    _URL='http://103.46.128.47:47720/'
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': '103.46.128.47:47720',
    'Origin': 'http://103.46.128.47:47720',
    'Referer': 'http://103.46.128.47:47720',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.16 Safari/537.36',
    'Upgrade-Insecure-Requests':'1'
    }

    def __init__(self, baseData):
        self._baseData = baseData        
    
    def getValidateCode(self):
        try:
            f = {
                'pic_file':("filename2.png", self._baseData, "image/png")
            }

            res=requests.post(self._URL,headers= self.headers,files=f)
            print 'res.text',res.text
            tempRes=re.findall(r"<B>(.+?)</B>",res.text)
            
            if  len(tempRes)>0 :
                print tempRes[0].split(" "),tuple(tempRes[0].split(" "))
                return Response_Web(tuple(tempRes[0].split(" ")),0)
            else:
                return Response_Web(tuple(),1)
          
        except Exception as e:
            print e
            return Response_Web(None,1,'360接口处理信息错误')
        

if __name__ == '__main__':
   
    Request_Web(a.read()).getValidateCode()
    # Email()