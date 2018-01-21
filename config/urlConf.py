import random

urls = {
    "auth": {
        "req_url": "https://kyfw.12306.cn/passport/web/auth/uamtk",
        "req_type": "post"
    },
    "login": {
        "req_url": "https://kyfw.12306.cn/passport/web/login",
        "req_type": "post"
    },
    "getCodeImg": {
        "req_url": "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&{0}".format(random.random()),
        "req_type": "get"
    },
    "codeCheck": {
        "req_url": "https://kyfw.12306.cn/passport/captcha/captcha-check",
        "req_type": "post"
    },
    "loginInit": {
        "req_url": "https://kyfw.12306.cn/otn/login/init",
        "req_type": "get"
    },
    "getUserInfo": {
        "req_url": "https://kyfw.12306.cn/otn/index/initMy12306",
        "req_type": "get"
    },
    "userLogin": {
        "req_url": "https://kyfw.12306.cn/otn/login/userLogin",
        "req_type": "get"
    },
    "uamauthclient": {
        "req_url": "https://kyfw.12306.cn/otn/uamauthclient",
        "req_type": "post"
    },
    "initdc_url": {
        "req_url": "https://kyfw.12306.cn/otn/confirmPassenger/initDc",
        "req_type": "get"
    },
    "get_passengerDTOs": {
        "req_url": "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs",
        "req_type": "post"
    },
    "select_url": {
        "req_url": "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={0}&leftTicketDTO.from_station={1}&leftTicketDTO.to_station={2}&purpose_codes=ADULT",
        "req_type": "post"
    },
    "check_user_url": {
        "req_url": "https://kyfw.12306.cn/otn/login/checkUser",
        "req_type": "post"
    },
    "submit_station_url": {
        "req_url": "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest",
        "req_type": "post"
    },
    "checkOrderInfoUrl": {
        "req_url": "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo",
        "req_type": "post"
    },
    "getQueueCountUrl": {
        "req_url": "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount",
        "req_type": "post"
    },
    "checkQueueOrderUrl": {
        "req_url": "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue",
        "req_type": "post"
    },
    "checkRandCodeAnsyn": {
        "req_url": "https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn",
        "req_type": "post"
    },
    "codeImgByOrder": {
        "req_url": "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&%s" % random.random(),
        "req_type": "post"
    },
    "queryOrderWaitTimeUrl": {
        "req_url": "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime",
        "req_type": "post"
    },
    "queryMyOrderNoCompleteUrl": {
        "req_url": "https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete",
        "req_type": "post"
    },
    "initNoCompleteUrl": {
        "req_url": "https://kyfw.12306.cn/otn/queryOrder/initNoComplete",
        "req_type": "post"
    }
}