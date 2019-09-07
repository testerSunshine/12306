# 关于软件使用配置说明，一定要看！！！
# ps: 如果是候补车票，需要通过人证一致性核验的用户及激活的“铁路畅行”会员可以提交候补需求，请您按照操作说明在铁路12306app.上完成人证核验
# 关于候补了之后是否还能继续捡漏的问题在此说明： 软件为全自动候补加捡漏，如果软件候补成功则会停止抢票，发出邮件通知，但是不会影响你继续捡漏，
# 如果这个时候捡漏捡到的话，也是可以付款成功的，也就是说，捡漏+候补，可以最大程度提升抢票成功率

# 刷票模式：1=刷票 2=候补+刷票
TICKET_TYPE = 2

# 候补最晚兑现日期，目前软件为捡漏加自动候补，所以这个值一定要填，并且这个日期一定要填小于最长订票时间(30天)
# 格式为日期+小时+分
# 举例： 比如今天才可以买10.1号的票，比如你那个发车是10.1号上午两点，你兑现时间写到10.1晚上22点？
# t("#fromDate").val() + "#" + t("#dafaultTime").html().replace("时", "") + "#" + t("#dafaultMinutes").html().replace("分", ""),
J_Z_PARAM = "2019-09-28#22#59"

# 出发日期(list) "2018-01-06", "2018-01-07"
# ps: 日期如果是单日，一定要前面补个0，正确做法：2019-01-01， 错误做法：2019-1-1
STATION_DATES = [
    "2019-09-25"
]

# 填入需要购买的车次(list)，"G1353"
STATION_TRAINS = [
    "",
]

# 出发城市，比如深圳北，就填深圳就搜得到
FROM_STATION = ""

# 到达城市 比如深圳北，就填深圳就搜得到
TO_STATION = ""

# 座位(list) 多个座位ex:
# "商务座",
# "一等座",
# "二等座",
# "特等座",
# "软卧",
# "硬卧",
# "硬座",
# "无座",
# "动卧",
SET_TYPE = [
    "",
]

# 当余票小于乘车人，如果选择优先提交，则删减联系人和余票数一致在提交
# bool
IS_MORE_TICKET = True

# 乘车人(list) 多个乘车人ex:
# - "张三"
# - "李四"
TICKET_PEOPLES = [
    "",
]

# 12306登录账号
USER = ""
PWD = ""

# 加入小黑屋时间默认为5分钟，此功能为了防止僵尸票导致一直下单不成功错过正常的票
TICKET_BLACK_LIST_TIME = 5

# 自动打码
IS_AUTO_CODE = True

#  邮箱配置，如果抢票成功，将通过邮件配置通知给您
#  列举163
#  email: "xxx@163.com"
#  notice_email_list: "123@qq.com"
#  username: "xxxxx"
#  password: "xxxxx
#  host: "smtp.163.com"
#  列举qq  ，qq设置比较复杂，需要在邮箱-->账户-->开启smtp服务，取得授权码==邮箱登录密码
#  email: "xxx@qq.com"
#  notice_email_list: "123@qq.com"
#  username: "xxxxx"
#  password: "授权码"
#  host: "smtp.qq.com"
EMAIL_CONF = {
    "IS_MAIL": False,
    "email": "",
    "notice_email_list": "",
    "username": "",
    "password": "",
    "host": "",
}

# 是否开启 pushbear 微信提醒， 使用前需要前往 http://pushbear.ftqq.com 扫码绑定获取 send_key 并关注获得抢票结果通知的公众号
PUSHBEAR_CONF = {
    "is_pushbear": False,
    "send_key": ""
}

# 是否开启cdn查询，可以更快的检测票票 1为开启，2为关闭
IS_CDN = 1

# 下单接口分为两种，1 模拟网页自动捡漏下单（不稳定），2 模拟车次后面的购票按钮下单（稳如老狗）
ORDER_TYPE = 2

# 下单模式 1 为预售，整点刷新，刷新间隔0.1-0.5S, 然后会校验时间，比如12点的预售，那脚本就会在12.00整检票，刷新订单
#         2 是捡漏，捡漏的刷新间隔时间为0.5-3秒，时间间隔长，不容易封ip
ORDER_MODEL = 2

# 是否开启代理, 0代表关闭， 1表示开始
# 开启此功能的时候请确保代理ip是否可用，在测试放里面经过充分的测试，再开启此功能，不然可能会耽误你购票的宝贵时间
# 使用方法：
# 1、在agency/proxy_list列表下填入代理ip
# 2、测试UnitTest/TestAll/testProxy 测试代理是否可以用
# 3、开启代理ip
IS_PROXY = 0

# 预售放票时间, 如果是捡漏模式，可以忽略此操作
OPEN_TIME = "13:00:00"
# 1=使用selenium获取devicesID
# 2=使用网页端/otn/HttpZF/logdevice获取devicesId，这个接口的算法目前可能有点问题，如果登录一直302的请改为配置1
COOKIE_TYPE = 1
# 如果COOKIE_TYPE=1，则需配置chromeDriver路径(注意是填你机器本地chromeDriver的路径，这个地方一定要改),下载地址http://chromedriver.storage.googleapis.com/index.html
# chromedriver配置版本只要和chrome的大版本匹配就行
# 如果是windows,最好在路径加上r, ex: r"/Users/wenxianping/Downloads/chromedriver"
CHROME_PATH = ""

PASSENGER_TICKER_STR = {
    '一等座': 'M',
    '特等座': 'P',
    '二等座': 'O',
    '商务座': 9,
    '硬座': 1,
    '无座': 1,
    '软座': 2,
    '软卧': 4,
    '硬卧': 3,
}

# 软件版本
RE_VERSION = "1.1.106"
