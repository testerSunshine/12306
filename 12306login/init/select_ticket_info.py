# -*- coding=utf-8 -*-
import json
import time

import datetime

import re
import urllib

from myUrllib import myurllib2


class select:
    def __init__(self, from_station, to_station):
        self.from_station = from_station
        self.to_station = to_station

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

    def station_table(self):
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
        from_station = station_name[self.from_station]
        to_station = station_name[self.to_station]
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
        name = r"var globalRepeatSubmitToken = '(\S+)'"
        token = re.search(name, initdc_result).group(1)
        return token

    def getPassengerDTOs(self, token):
        """
        获取乘客信息
        :return: 
        """
        get_passengerDTOs = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        get_data = {
            '_json_att': None,
            'REPEAT_SUBMIT_TOKEN': token
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
        from_station, to_station = self.station_table()
        select_url = 'https://kyfw.12306.cn/otn/leftTicket/query?' \
                     'leftTicketDTO.train_date={}&leftTicketDTO.from_station={}' \
                     '&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(self.time(), from_station, to_station)
        check_user_url = 'https://kyfw.12306.cn/otn/login/checkUser'
        submit_station_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        station_ticket = json.loads(myurllib2.get(select_url), encoding='utf-8')
        value = station_ticket['data']
        if value.__len__() is 0:
            print '当前车次查询为空...'
        else:
            for i in value['result']:
                ticket_info = i.split('|')
                for j in range(20, 33):
                    if ticket_info[j] != '' and ticket_info[j] != '无':
                        print '车次: ' + ticket_info[3] + ' 始发车站: ' + value['map']['AOH'] + ' 终点站: ' + \
                              value['map']['CSQ'] + ' ' + self.station_seat(j) + ': ' + ticket_info[j]
                        print '正在尝试提交订票...'
                        data = dict(_json_att=None)
                        check_user = json.loads(myurllib2.Post(check_user_url, data), encoding='utf-8')
                        check_user_flag = check_user['data']['flag']
                        if check_user_flag is True:
                            print '尝试提交订单...'
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
                            submit_data = submitResult['data']
                            if submit_data == 'N':
                                print '出票成功'
                            else:
                                print '出票失败'
                        else:
                            if check_user['massage']:
                                print '用户检查失败：%s' % check_user['massage']
                            else:
                                print '用户检查失败： %s' %check_user
                        return submitResult

    def getPassengerTicketStr(self, str):
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
        return passengerTicketStr[str]

    def checkOrderInfo(self, token):
        """
        检查支付订单，需要提交REPEAT_SUBMIT_TOKEN
        :return: 
        """
        checkOrderInfoUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data = {
            'cancel_flag': 2,
            'bed_level_order_num': 000000000000000000000000000000,

        }

    def main(self):
        token = self.getRepeatSubmitToken()
        self.submitOrderRequest()
        self.getPassengerDTOs(token)
        self.checkOrderInfo(token)

if __name__ == '__main__':
    a = select('上海', '北京')
    a.main()