from enum import Enum


class StatusCode(Enum):
    """
    程序返回状态码
    name: 状态名
    value: 状态值
    description: 状态描述
    """
    OK =                          0,   u"正常"
    RetryTimeHasReachedMaxValue = 101, u"重试次数达到上限"
    CdnListEmpty =                102, u"cdn列表为空"
    UnknownError =                999, u"未知错误"

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, description: str = None):
        self._description_ = description

    def __str__(self):
        return str(self.value)

    # description is read-only
    @property
    def description(self):
        return self._description_
