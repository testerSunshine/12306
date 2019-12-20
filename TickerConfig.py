# -*- coding=utf-8 -*-
# 关于软件使用配置说明，一定要看！！！
# ps: 如果是候补车票，需要通过人证一致性核验的用户及激活的“铁路畅行”会员可以提交候补需求，请您按照操作说明在铁路12306app.上完成人证核验
# 关于候补了之后是否还能继续捡漏的问题在此说明： 软件为全自动候补加捡漏，如果软件候补成功则会停止抢票，发出邮件通知，但是不会影响你继续捡漏，
# 如果这个时候捡漏捡到的话，也是可以付款成功的，也就是说，捡漏+候补，可以最大程度提升抢票成功率

# 刷票模式：1=刷票 2=候补+刷票
TICKET_TYPE = 1

# 出发日期(list) "2018-01-06", "2018-01-07"
STATION_DATES = [
    "2020-01-18"
]

# 填入需要购买的车次(list)，"G1353"
# 修改车次填入规则，注：(以前设置的车次逻辑不变)，如果车次填入为空，那么就是当日乘车所有车次都纳入筛选返回
# 不填车次是整个list为空才算，如果不是为空，依然会判断车次的，这种是错误的写法 [""], 正确的写法 []
STATION_TRAINS = []

# 出发城市，比如深圳北，就填深圳就搜得到
FROM_STATION = "广州南"

# 到达城市 比如深圳北，就填深圳就搜得到
TO_STATION = "隆回"

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
SET_TYPE = ["二等座"]

# 当余票小于乘车人，如果选择优先提交，则删减联系人和余票数一致在提交
# bool
IS_MORE_TICKET = True

# 乘车人(list) 多个乘车人ex:
# "张三",
# "李四"
TICKET_PEOPLES = []

# 12306登录账号
USER = ""
PWD = ""

# 加入小黑屋时间默认为5分钟，此功能为了防止僵尸票导致一直下单不成功错过正常的票
TICKET_BLACK_LIST_TIME = 5

# 自动打码
IS_AUTO_CODE = True

# 设置2本地自动打码，需要配置tensorflow和keras库，3为云打码，由于云打码服务器资源有限(为2h4C的cpu服务器)，请不要恶意请求，不然只能关闭服务器
# ps: 请不要一直依赖云服务器资源，在此向所有提供服务器同学表示感谢
AUTO_CODE_TYPE = 3

# 此处设置云打码服务器地址，如果有自建的服务器，可以自行更改
HOST = "120.77.154.140:8000"
REQ_URL = "/verify/base64/"
HTTP_TYPE = "http"
# HOST="12306.yinaoxiong.cn" #备用服务器稳定性较差
# REQ_URL="/verify/base64/"
# HTTP_TYPE="https"

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
    "IS_MAIL": True,
    "email": "",
    "notice_email_list": "",
    "username": "",
    "password": "",
    "host": "smtp.qq.com",
}

# 是否开启 server酱 微信提醒， 使用前需要前往 http://sc.ftqq.com/3.version 扫码绑定获取 SECRET 并关注获得抢票结果通知的公众号
SERVER_CHAN_CONF = {
    "is_server_chan": False,
    "secret": ""
}

# 是否开启cdn查询，可以更快的检测票票 1为开启，2为关闭
IS_CDN = 1

# 下单接口分为两种，1 模拟网页自动捡漏下单（不稳定），2 模拟车次后面的购票按钮下单（稳如老狗）
ORDER_TYPE = 2

# 下单模式 1 为预售，整点刷新，刷新间隔0.1-0.5S, 然后会校验时间，比如12点的预售，那脚本就会在12.00整检票，刷新订单
#         2 是捡漏，捡漏的刷新间隔时间为0.5-3秒，时间间隔长，不容易封ip
ORDER_MODEL = 1

# 是否开启代理, 0代表关闭， 1表示开始
# 开启此功能的时候请确保代理ip是否可用，在测试放里面经过充分的测试，再开启此功能，不然可能会耽误你购票的宝贵时间
# 使用方法：
# 1、在agency/proxy_list列表下填入代理ip
# 2、测试UnitTest/TestAll/testProxy 测试代理是否可以用
# 3、开启代理ip
IS_PROXY = 0

# 预售放票时间, 如果是捡漏模式，可以忽略此操作
OPEN_TIME = "12:59:57"
# 1=使用selenium获取devicesID
# 2=使用网页端/otn/HttpZF/logdevice获取devicesId，这个接口的算法目前可能有点问题，如果登录一直302的请改为配置1
# 3=自己打开浏览器在headers-Cookies中抓取RAIL_DEVICEID和RAIL_EXPIRATION，这个就不用配置selenium
COOKIE_TYPE = 3
# 如果COOKIE_TYPE=1，则需配置chromeDriver路径,下载地址http://chromedriver.storage.googleapis.com/index.html
# chromedriver配置版本只要和chrome的大版本匹配就行
CHROME_PATH = "/usr/src/app/chromedriver"

# 为了docker37 准备的环境变量，windows环境可以不用管这个参数
CHROME_CHROME_PATH = "/opt/google/chrome/google-chrome"

# 如果COOKIE_TYPE=3, 则需配置RAIL_EXPIRATION、RAIL_DEVICEID的值
RAIL_EXPIRATION = ""
RAIL_DEVICEID = ""
# RAIL_EXPIRATION = "1577034103293"
# RAIL_DEVICEID = "CDno29Erc_Pf3FSXb4dzq-Op64EhWrsi5yUZKVIKR1MAfYo2qFlCeXD8VkexY7_1qg-ClV-fE8j9jgVlPZxRh3wVc2iqLe_5A8sdr62qZx4B22JPF8lFCjpgTKZ5ODW90HJd5tiQsJ1KR9nOqHRxHj1FT5LEIwfw"


# 1=>为一直随机ua,2->只启动的时候随机一次ua
RANDOM_AGENT = 2

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

# 保护12306官网请求频率，设置随机请求时间，原则为5分钟不大于80次
# 最大间隔请求时间
MAX_TIME = 3
# 最小间隔请求时间
MIN_TIME = 1

# 软件版本
RE_VERSION = "1.2.004"
