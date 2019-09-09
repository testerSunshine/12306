# coding=utf-8
from enum import Enum


class ticket(object):
    QUERY_C = u"查询到有余票，尝试提交订单"
    QUERY_IN_BLACK_LIST = u"该车次{} 正在被关小黑屋，跳过此车次"

    SUCCESS_CODE = 000000
    FAIL_CODE = 999999
    AUTO_SUBMIT_ORDER_REQUEST_C = u"提交订单成功"
    AUTO_SUBMIT_ORDER_REQUEST_F = u"提交订单失败，重新刷票中"
    AUTO_SUBMIT_NEED_CODE = u"需要验证码"
    AUTO_SUBMIT_NOT_NEED_CODE = u"不需要验证码"

    TICKET_BLACK_LIST_TIME = 5  # 加入小黑屋的等待时间，默认5 min

    DTO_NOT_FOUND = u"未查找到常用联系人, 请查证后添加!!"
    DTO_NOT_IN_LIST = u"联系人不在列表中，请查证后添加!!"

    QUEUE_TICKET_SHORT = u"当前余票数小于乘车人数，放弃订票"
    QUEUE_TICKET_SUCCESS = u"排队成功, 当前余票还剩余: {0}张"
    QUEUE_JOIN_BLACK = u"排队发现未知错误{0}，将此列车 {1}加入小黑屋"
    QUEUE_WARNING_MSG = u"排队异常，错误信息：{0}, 将此列车 {1}加入小黑屋"

    OUT_NUM = 120  # 排队请求12306的次数
    WAIT_OUT_NUM = u"超出排队时间，自动放弃，正在重新刷票"
    WAIT_ORDER_SUCCESS = u"恭喜您订票成功，订单号为：{0}, 请立即打开浏览器登录12306，访问‘未完成订单’，在30分钟内完成支付!"
    WAIT_AFTER_NATE_SUCCESS = u"候补订单已完成，请立即打开浏览器登录12306，访问‘候补订单’，在30分钟内完成支付!"
    WAIT_ORDER_CONTINUE = u"排队等待时间预计还剩 {0} ms"
    WAIT_ORDER_FAIL = u"排队等待失败，错误消息：{0}"
    WAIT_ORDER_NUM = u"第{0}次排队中,请耐心等待"
    WAIT_ORDER_SUB_FAIL = u"订单提交失败！,正在重新刷票"

    CANCEL_ORDER_SUCCESS = u"排队超时，已为您自动取消订单，订单编号: {0}"
    CANCEL_ORDER_FAIL = u"排队超时，取消订单失败， 订单号{0}"

    REST_TIME = u"12306休息时间，本程序自动停止,明天早上6点将自动运行"
    REST_TIME_PAST = u"休息时间已过，重新开启检票功能"

    LOGIN_SESSION_FAIL = u"用户检查失败：{0}，可能未登录，可能session已经失效, 正在重新登录中"
