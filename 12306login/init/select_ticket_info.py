# -*- coding=utf-8 -*-
import json
import datetime
import random
import re
import urllib
import sys
import time
from myUrllib import myurllib2
reload(sys)
sys.setdefaultencoding('utf-8')

class select:
    def __init__(self, from_station, to_station):
        self.from_station, self.to_station = self.station_table(from_station, to_station)
        self.order_request_params = {}  # 订单提交时的参数
        self.ticketInfoForPassengerForm = {}  # 初始化当前页面参数
        self.current_seats = {}  # 席别信息
        self.token = ""
        self.set_type = ""
        self.user_info = ""

    def get_order_request_params(self):
        return self.order_request_params

    def get_ticketInfoForPassengerForm(self):
        return self.ticketInfoForPassengerForm

    def get_current_seats(self):
        return self.current_seats

    def get_token(self):
        return self.token

    def get_set_type(self):
        return self.set_type

    def station_seat(self, index):
        """
        获取车票对应坐席
        :param seat_type:
        :return:
        """
        seat = {32: '商务座 ',
                31: '一等座 ',
                30: '二等座 ',
                25: '特等座 ',
                23: '软卧 ',
                28: '硬卧 ',
                29: '硬座 ',
                26: '无座 '
                }
        return seat[index]

    def station_table(self, from_station, to_station):
        """
        读取车站信息
        :param station:
        :return:
        """
        result = open('station_name.txt')
        info = result.read().split('=')[1].strip("'").split('@')
        del info[0]
        station_name = {}
        for i in range(0, len(info)):
            # print info[i]
            n_info = info[i].split('|')
            station_name[n_info[1]] = n_info[2]
        from_station = station_name[from_station]
        to_station = station_name[to_station]
        return from_station, to_station

    def time(self):
        today = datetime.date.today()
        tomorrow = today+datetime.timedelta(1)
        return tomorrow.strftime('%Y-%m-%d')

    def getRepeatSubmitToken(self):
        """
        获取提交车票请求token
        :return: token
        """
        initdc_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        initdc_result = myurllib2.get(initdc_url)
        token_name = re.compile(r"var globalRepeatSubmitToken = '(\S+)'")
        ticketInfoForPassengerForm_name = re.compile(r'var ticketInfoForPassengerForm=(\{.+\})?')
        order_request_params_name = re.compile(r'var orderRequestDTO=(\{.+\})?')
        # if token_name and ticketInfoForPassengerForm_name and order_request_params_name:
        self.token = re.search(token_name, initdc_result).group(1)
        re_tfpf = re.findall(ticketInfoForPassengerForm_name, initdc_result)
        re_orp = re.findall(order_request_params_name, initdc_result)
        if re_tfpf:
            self.ticketInfoForPassengerForm = json.loads(re_tfpf[0].replace("'", '"'))
        else:
            print('车次获取信息为空')
        if re_orp:
            self.order_request_params = json.loads(re_orp[0].replace("'", '"'))
        else:
            print('订单获取信息为空')

    def getPassengerDTOs(self):
        """
        获取乘客信息
        :return: 
        """
        get_passengerDTOs = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        get_data = {
            '_json_att': None,
            'REPEAT_SUBMIT_TOKEN': self.token
        }
        jsonData = json.loads(myurllib2.Post(get_passengerDTOs, get_data))
        if 'data' in jsonData and jsonData['data'] and 'normal_passengers' in jsonData['data'] and jsonData['data'][
            'normal_passengers']:
            return jsonData['data']['normal_passengers']
        else:
            if 'data' in jsonData and 'exMsg' in jsonData['data'] and jsonData['data']['exMsg']:
                print(jsonData['data']['exMsg'])
            elif 'messages' in jsonData and jsonData['messages']:
                print(jsonData['messages'])
            else:
                print("未查找到常用联系人")

    def submitOrderRequest(self):
        """
        提交车次信息
        :return: 车次信息，座位号
        """

        select_url = 'https://kyfw.12306.cn/otn/leftTicket/query?' \
                     'leftTicketDTO.train_date={}&leftTicketDTO.from_station={}' \
                     '&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(self.time(), self.from_station, self.to_station)
        check_user_url = 'https://kyfw.12306.cn/otn/login/checkUser'
        submit_station_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        station_ticket = json.loads(myurllib2.get(select_url), encoding='utf-8')
        value = station_ticket['data']
        if value.__len__() is 0:
            print ('当前车次查询为空...')
        else:
            for i in value['result']:
                ticket_info = i.split('|')
                for j in range(20, 33):
                    if ticket_info[j] != '' and ticket_info[j] != '无':    # 过滤有效目标车次
                        print ('车次: ' + ticket_info[3] + ' 始发车站: ' + value['map']['AOH'] + ' 终点站: ' + \
                               value['map']['CSQ'] + ' ' + self.station_seat(j) + ':' + ticket_info[j])
                        print ('正在尝试提交订票...')
                        data = dict(_json_att=None)
                        check_user = json.loads(myurllib2.Post(check_user_url, data), encoding='utf-8')
                        check_user_flag = check_user['data']['flag']
                        if check_user_flag is True:
                            print ('订票成功!')
                            print ('尝试提交订单...')
                            # 预定的请求参数，注意参数顺序
                            # 注意这里为了防止secretStr被urllib.parse过度编码，在这里进行一次解码
                            # 否则调用HttpTester类的post方法将会将secretStr编码成为无效码,造成提交预定请求失败
                            data = [('secretStr', urllib.unquote(ticket_info[0])),  # 字符串加密
                                    ('train_date', self.time()),  # 出发时间
                                    ('back_train_date', self.time()),  # 返程时间
                                    ('tour_flag', 'dc'),  # 旅途类型
                                    ('purpose_codes', 'ADULT'),  # 成人票还是学生票
                                    ('query_from_station_name', self.from_station),  # 起始车站
                                    ('query_to_station_name', self.to_station),  # 终点车站
                                    ]
                            submitResult = json.loads(myurllib2.Post(submit_station_url, data), encoding='utf-8')
                            if 'data' in submitResult and submitResult['data']:
                                if submitResult['data'] == 'N':
                                    print ('出票成功')
                                    return self.station_seat(j)  # 车次信息，座位号
                                else:
                                    print ('出票失败')
                            elif 'messages' in submitResult and submitResult['messages']:
                                print(submitResult['messages'])
                        else:
                            if check_user['messages']:
                                print ('用户检查失败：%s' % check_user['messages'])
                            else:
                                print ('用户检查失败： %s' % check_user)
                    else:
                        print ('未查询到有效车次，重新查询中')

    def getPassengerTicketStr(self, set_type):
        """
        获取getPassengerTicketStr 提交对应的代号码
        :param str: 坐席
        :return: 
        """
        passengerTicketStr = {
            '一等座': 'M',
            '特等座': 'P',
            '二等座': 'O',
            '商务座': 9,
            '硬座': 1,
            '无座': 1,
            '软卧': 4,
            '硬卧': 3,
        }
        self.set_type = str(passengerTicketStr[set_type.replace(' ', '')])

    def ticket_type(self):
        """订单票的类型，目前只考虑成人票，此方法暂时搁置，做备案"""
        ticket_type = {'adult': "1", 'child': "2", 'student': "3", 'disability': "4"}
        return ticket_type

    def checkOrderInfo(self):
        """
        检查支付订单，需要提交REPEAT_SUBMIT_TOKEN
        passengerTicketStr : 座位编号,0,票类型,乘客名,证件类型,证件号,手机号码,保存常用联系人(Y或N)
        oldPassengersStr: 乘客名,证件类型,证件号,乘客类型
        :return: 
        """
        checkOrderInfoUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data = {
            'cancel_flag': 2,
            'bed_level_order_num': "000000000000000000000000000000",
            'passengerTicketStr': self.set_type+',0,'+self.user_info[0]['passenger_id_type_code']+","+self.user_info[0]["passenger_name"]+","+self.user_info[0]['passenger_type']+","+self.user_info[0]['passenger_id_no']+","+self.user_info[0]['mobile_no']+',N',
            'oldPassengerStr': self.user_info[0]['passenger_name']+","+self.user_info[0]['passenger_type']+","+self.user_info[0]['passenger_id_no']+","+self.user_info[0]['passenger_type']+'_',
            'tour_flag': 'dc',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        checkOrderInfo = json.loads(myurllib2.Post(checkOrderInfoUrl, data, ))
        if 'data' in checkOrderInfo and checkOrderInfo['data']['submitStatus'] is True:
            print ('车票提交通过，正在尝试排队')
        elif 'messages' in checkOrderInfo and checkOrderInfo['messages']:
            print (checkOrderInfo['messages'])

    def getQueueCount(self):
        """
        # 模拟查询当前的列车排队人数的方法
        # 返回信息组成的提示字符串
        :param token:
        :return:
        """
        old_train_date = self.get_ticketInfoForPassengerForm()['queryLeftTicketRequestDTO']['train_date']+"00:00:00"  # 模仿12306格式 Sun May 21 2017 00:00:00 GMT+0800 (中国标准时间)
        m_time = time.mktime(time.strptime(old_train_date, "%Y%m%d%H:%M:%S"))
        l_time = time.localtime(m_time)
        new_train_date = time.strftime("%a %b %d %Y %H:%M:%S", l_time)
        getQueueCountUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        data = {
            'train_date': new_train_date,
            'train_no': self.get_ticketInfoForPassengerForm()['queryLeftTicketRequestDTO']['train_no'],
            'stationTrainCode':	self.get_ticketInfoForPassengerForm()['queryLeftTicketRequestDTO']['station_train_code'],
            'seatType':	self.set_type,
            'fromStationTelecode': self.get_ticketInfoForPassengerForm()['queryLeftTicketRequestDTO']['from_station'],
            'toStationTelecode': self.get_ticketInfoForPassengerForm()['queryLeftTicketRequestDTO']['to_station'],
            'leftTicket': self.get_ticketInfoForPassengerForm()['leftTicketStr'],
            'purpose_codes': self.get_ticketInfoForPassengerForm()['purpose_codes'],
            'train_location': self.get_ticketInfoForPassengerForm()['train_location'],
            'REPEAT_SUBMIT_TOKEN': self.get_token(),
        }
        getQueueCountResult = json.loads(myurllib2.Post(getQueueCountUrl, data))
        if "status" in getQueueCountResult and getQueueCountResult["status"] is True:
            if "countT" in getQueueCountResult["data"]:
                countT = getQueueCountResult["data"]["countT"]
                if int(countT) is 0:
                    print("排队成功, 当前余票还剩余:" + getQueueCountResult["data"]["ticket"]+ "张")
                    print("提交订单中")
                    self.checkQueueOrder()
                else:
                    print("正在排队，当前排队人数:" + str(countT) + "当前余票还剩余:" + getQueueCountResult["data"]["ticket"]+ "张")
            else:
                print("排队发现未知错误")
        elif "messages" in getQueueCountResult and getQueueCountResult["messages"]:
            print("排队异常，错误信息："+getQueueCountResult)
        else:
            print(getQueueCountResult["validateMessages"])

    def checkQueueOrder(self):
        """
        模拟提交订单是确认按钮，参数获取方法还是get_ticketInfoForPassengerForm 中获取
        :return: 
        """
        checkQueueOrderUrl = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
        data = {
            "passengerTicketStr": self.set_type+',0,'+self.user_info[0]['passenger_id_type_code']+","+self.user_info[0]["passenger_name"]+","+self.user_info[0]['passenger_type']+","+self.user_info[0]['passenger_id_no']+","+self.user_info[0]['mobile_no']+',N',
            "oldPassengerStr": self.user_info[0]['passenger_name']+","+self.user_info[0]['passenger_type']+","+self.user_info[0]['passenger_id_no']+","+self.user_info[0]['passenger_type']+'_',
            "purpose_codes": self.get_ticketInfoForPassengerForm()["purpose_codes"],
            "key_check_isChange": self.get_ticketInfoForPassengerForm()["key_check_isChange"],
            "leftTicketStr": self.get_ticketInfoForPassengerForm()["leftTicketStr"],
            "train_location": self.get_ticketInfoForPassengerForm()["train_location"],
            "seatDetailType": "000",   # 开始需要选择座位，但是目前12306不支持自动选择作为，那这个参数为默认
            "roomType": "00",  # 好像是根据一个id来判断选中的，两种 第一种是00，第二种是10，但是我在12306的页面没找到该id，目前写死是00，不知道会出什么错
            "dwAll": "N",
            "REPEAT_SUBMIT_TOKEN": self.get_token(),
        }
        checkQueueOrderResult = json.loads(myurllib2.Post(checkQueueOrderUrl, data))
        if "status" is checkQueueOrderResult and checkQueueOrderResult["status"]:
            c_data = checkQueueOrderResult["data"] if checkQueueOrderResult["data"] in checkQueueOrderResult else {}
            if 'submitStatus' in c_data and c_data['submitStatus']:
                print("出票成功!")
            else:
                if 'errMsg' in c_data and c_data['errMsg']:
                    print("出票失败，" + c_data['errMsg'] + "请重新选择。")
                else:
                    print(c_data)
                    print('订票失败!很抱歉,请重试提交预订功能!')
        elif "messages" in checkQueueOrderResult and checkQueueOrderResult["messages"]:
            print("提交订单失败,错误信息: "+ checkQueueOrderResult["messages"])
        else:
            print("未知错误：" + checkQueueOrderResult["validateMessages"])

    def queryOrderWaitTime(self):
        """
        排队获取订单等待信息,每隔1秒请求一次，最高请求次数为20次！
        :return: 
        """
        queryOrderWaitTimeUrl = "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime"
        data = {
            "random": "149545481029" + str(random.randint(1, 9)),
            "tourFlag": "dc",
            "REPEAT_SUBMIT_TOKEN": self.get_token(),
        }
        num = 1
        while True:
            num += 1
            if num > 20:
                print("订票失败！")
                break
            queryOrderWaitTimeResult = json.loads(myurllib2.Post(queryOrderWaitTimeUrl, data))
            if "orderId" in queryOrderWaitTimeResult and queryOrderWaitTimeResult["data"]["orderId"] != "null":
                print ("恭喜您订票成功，订单号为：" + queryOrderWaitTimeResult["data"]["orderId"] + ", 请立即打开浏览器登录12306，访问‘未完成订单’，在30分钟内完成支付！")
                break
            print("订单提交中,请耐心等待")
            time.sleep(1000)

    def main(self):
        set_type = self.submitOrderRequest()
        self.getPassengerTicketStr(set_type)
        self.getRepeatSubmitToken()
        self.user_info = self.getPassengerDTOs()
        self.checkOrderInfo()
        self.getQueueCount()
        self.queryOrderWaitTime()

if __name__ == '__main__':
    a = select('上海', '北京')
    a.main()