# -*- coding=utf-8 -*-
import json
import time

import datetime

import re
import urllib

from myUrllib import myurllib2


class select:
    def __init__(self, from_station, to_station):
        self.from_station, self.to_station = self.station_table(from_station, to_station)
        self.order_request_params = {}  # 订单提交时的参数
        self.ticketInfoForPassengerForm = {}  # 初始化当前页面参数
        self.current_seats = {}  # 席别信息
        self.token = ''
        self.set_type = ''

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
                               value['map']['CSQ'] + ' ' + self.station_seat(j) + ': ' + ticket_info[j])
                        print ('正在尝试提交订票...')
                        data = dict(_json_att=None)
                        check_user = json.loads(myurllib2.Post(check_user_url, data), encoding='utf-8')
                        check_user_flag = check_user['data']['flag']
                        if check_user_flag is True:
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

    def checkOrderInfo(self, user_info):
        """
        检查支付订单，需要提交REPEAT_SUBMIT_TOKEN
        passengerTicketStr : 座位编号,0,票类型,乘客名,证件类型,证件号,手机号码,保存常用联系人(Y或N)
        oldPassengersStr: 乘客名,证件类型,证件号,乘客类型
        :return: 
        """
        passengerTicketStr = []
        oldPassengerStr = []
        passengerTicketStr.append(user_info[0]['passenger_id_type_code'])
        passengerTicketStr.append(user_info[0]['passenger_name'])
        passengerTicketStr.append(user_info[0]['passenger_type'])
        passengerTicketStr.append(user_info[0]['passenger_id_no'])
        passengerTicketStr.append(user_info[0]['mobile_no'])
        oldPassengerStr.append(user_info[0]['passenger_name'])
        oldPassengerStr.append(user_info[0]['passenger_type'])
        oldPassengerStr.append(user_info[0]['passenger_id_no'])
        oldPassengerStr.append(user_info[0]['passenger_type'])

        checkOrderInfoUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data = {
            'cancel_flag': 2,
            'bed_level_order_num': 000000000000000000000000000000,
            'passengerTicketStr': self.set_type+',0,'+str(passengerTicketStr)+',N',
            'oldPassengerStr': str(oldPassengerStr)+'_',
            'tour_flag': 'dc',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        checkOrderInfo = json.loads(myurllib2.Post(checkOrderInfoUrl, data))
        print (checkOrderInfo)
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
        getQueueCountUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        data = {
            # 'train_date': 'Sun May 07 2017 00:00:00 GMT+0800',
            'train_date': self.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_date'],
            'train_no': self.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_no'],
            'stationTrainCode':	self.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['station_train_code'],
            'seatType':	self.set_type,
            'fromStationTelecode': self.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['from_station'],
            'toStationTelecode': self.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['to_station'],
            'leftTicket': self.ticketInfoForPassengerForm['leftTicketStr'],
            'purpose_codes': self.ticketInfoForPassengerForm['purpose_codes'],
            'train_location': self.ticketInfoForPassengerForm['train_location'],
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        print(data)
        getQueueCountResult = json.loads(myurllib2.Post(getQueueCountUrl, data))
        print(getQueueCountResult)

    def main(self):
        set_type = self.submitOrderRequest()
        self.getPassengerTicketStr(set_type)
        self.getRepeatSubmitToken()
        user_info = self.getPassengerDTOs()
        self.checkOrderInfo(user_info)
        self.getQueueCount()

if __name__ == '__main__':
    a = select('上海', '北京')
    a.main()