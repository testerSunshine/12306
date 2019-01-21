# coding=utf-8

#-基础请求类
class BaseRequest(object):
    def __init__(self):
        pass

#-基础返回类
class BaseResponse(object):
    def __init__(self, resTuple,code=1, errorMsg=None):
        self.res = resTuple
        self.code = code
        self.errorMsg =errorMsg




