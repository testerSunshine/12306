# -*- coding=utf-8 -*-
import json
import datetime
import random
import re
import socket
import threading
import urllib.request
import urllib.parse
import urllib.error
import sys
import time
from collections import OrderedDict
from init import login
from myUrllib.httpUtils import session as SESS

from config.emailConf import email
from config.ticketConf import _get_yaml
from damatuCode.damatuWeb import DamatuApi
from myException.PassengerUserException import PassengerUserException
from myException.ticketConfigException import ticketConfigException
from myException.ticketIsExitsException import ticketIsExitsException
from myException.ticketNumOutException import ticketNumOutException
from json import JSONDecodeError 
import codecs
import traceback
from init import login

class select:

    retry_limit = 5
    env_retry_limit = 0

    def __init__(self, ticket_config):
        self.from_station, self.to_station, self.station_dates, self._station_seat, self.is_more_ticket, self.ticke_peoples, self.select_refresh_interval, self.station_trains, self.expect_refresh_interval, self.ticket_black_list_time = self.get_ticket_info(
            ticket_config)
        self.order_request_params = {}  # 订单提交时的参数
        self.ticketInfoForPassengerForm = {}  # 初始化当前页面参数
        self.current_seats = {}  # 席别信息
        self.token = ""
        self.set_type = ""
        self.user_info = ""
        self.secretStr = ""
        self.ticket_black_list = dict()
        self.is_check_user = dict()
        self.ticket_config = ticket_config
        self.login =login.GoLogin(self.ticket_config).go_login()
        self.s = SESS

    def get_ticket_info(self, ticket_config):
        """
        获取配置信息
        :return:
        """
        ticket_info_config = _get_yaml(ticket_config)
        from_station = ticket_info_config["set"]["from_station"]
        to_station = ticket_info_config["set"]["to_station"]
        station_dates = ticket_info_config["set"]["station_dates"]
        set_type = ticket_info_config["set"]["set_type"]
        is_more_ticket = ticket_info_config["set"]["is_more_ticket"]
        ticke_peoples = ticket_info_config["set"]["ticke_peoples"]
        select_refresh_interval = ticket_info_config["select_refresh_interval"]
        station_trains = ticket_info_config["set"]["station_trains"]
        expect_refresh_interval = ticket_info_config["expect_refresh_interval"]
        ticket_black_list_time = ticket_info_config["ticket_black_list_time"]
        print("*" * 20)
        print("当前配置：出发站：{0}\n到达站：{1}\n乘车日期：{2}\n坐席：{3}\n是否有票自动提交：{4}\n乘车人：{5}\n刷新间隔：{6}\n候选购买车次：{7}\n未开始刷票间隔时间：{8}\n僵尸票关小黑屋时长：{9}\n".format
              (
                  from_station,
                  to_station,
                  station_dates,
                  ",".join(set_type),
                  is_more_ticket,
                  ",".join(
                      ticke_peoples),
                  select_refresh_interval,
                  ",".join(
                      station_trains),
                  expect_refresh_interval,
                  ticket_black_list_time,
              ))
        print("*" * 20)
        return from_station, to_station, station_dates, set_type, is_more_ticket, ticke_peoples, select_refresh_interval, station_trains, expect_refresh_interval, ticket_black_list_time

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

    def conversion_int(self, str):
        return int(str)

    def station_seat(self, index):
        """
        获取车票对应坐席
        :param seat_type:
        :return:
        """
        seat = {'商务座': 32,
                '一等座': 31,
                '二等座': 30,
                '特等座': 25,
                '软卧': 23,
                '硬卧': 28,
                '硬座': 29,
                '无座': 26,
                }
        return seat[index]

    def station_table(self, from_station, to_station):
        """
        读取车站信息
        :param station:
        :return:
        """
        result = codecs.open('station_name.txt', encoding='utf-8')
        info = result.read().split('=')[1].strip("'").split('@')
        del info[0]
        station_name = {}
        for i in range(0, len(info)):
            n_info = info[i].split('|')
            station_name[n_info[1]] = n_info[2]
        from_station = station_name[from_station]
        to_station = station_name[to_station]
        return from_station, to_station

    def time(self):
        """
        获取日期
        :return:
        """
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(1)
        return tomorrow.strftime('%Y-%m-%d')

    def getRepeatSubmitToken(self):
        """
        获取提交车票请求token
        :return: token
        """
        initdc_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        initdc_result = self.s.get(
            initdc_url, verify=False).content.decode(encoding='utf-8')
        token_name = re.compile(r"var globalRepeatSubmitToken = '(\S+)'")
        ticketInfoForPassengerForm_name = re.compile(
            r'var ticketInfoForPassengerForm=(\{.+\})?')
        order_request_params_name = re.compile(
            r'var orderRequestDTO=(\{.+\})?')
        # if token_name and ticketInfoForPassengerForm_name and order_request_params_name:
        self.token = re.search(token_name, initdc_result).group(1)
        re_tfpf = re.findall(ticketInfoForPassengerForm_name, initdc_result)
        re_orp = re.findall(order_request_params_name, initdc_result)
        if re_tfpf:
            self.ticketInfoForPassengerForm = json.loads(
                re_tfpf[0].replace("'", '"'))
        else:
            pass
        if re_orp:
            self.order_request_params = json.loads(re_orp[0].replace("'", '"'))
        else:
            pass

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
        jsonData = self.s.post(
            get_passengerDTOs, data=get_data, verify=False).json()

        if 'data' in jsonData and jsonData['data'] and 'normal_passengers' in jsonData['data'] and jsonData['data'][
                'normal_passengers']:
            # return jsonData['data']['normal_passengers']
            normal_passengers = jsonData['data']['normal_passengers']
            _normal_passenger = [normal_passengers[i] for i in range(len(
                normal_passengers))if normal_passengers[i]["passenger_name"] in self.ticke_peoples]
            # 如果配置乘车人没有在账号，则默认返回第一个用户
            return _normal_passenger if _normal_passenger else normal_passengers[0]
        else:
            if 'data' in jsonData and 'exMsg' in jsonData['data'] and jsonData['data']['exMsg']:
                print(jsonData['data']['exMsg'])
            elif 'messages' in jsonData and jsonData['messages']:
                print(jsonData['messages'][0])
            else:
                print("未查找到常用联系人")
                raise PassengerUserException("未查找到常用联系人,请先添加联系人在试试")

    def submitOrderRequestFunc(self, from_station, to_station, station_date):
        _status_code = 0
        try:
            select_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={0}&leftTicketDTO.from_station={1}&leftTicketDTO.to_station={2}&purpose_codes=ADULT'.format(
                station_date, from_station, to_station)
            while _status_code is not 200:
                station_ticket = self.s.get(
                    select_url, allow_redirects=False, verify=False)
                _status_code = station_ticket.status_code

            return station_ticket.json()
        except KeyboardInterrupt:
            traceback.print_exc()
        except:
            return {}

    def submitOrderRequestImplement(self, from_station, to_station,):
        """
        提交车次信息
        车次对应字典
        {32: '商务座 ',
            31: '一等座 ',
            30: '二等座 ',
            25: '特等座 ',
            23: '软卧 ',
            28: '硬卧 ',
            29: '硬座 ',
            26: '无座 '
        } 参照station_seat()方法
        :return:
        """

        station_ticket = {}
        broken_data_num = 0
        for station_date in self.station_dates:
            if station_date >= datetime.datetime.now().date().isoformat() and station_date < (datetime.datetime.now() + datetime.timedelta(days=30)).date().isoformat():
                sub_result = self.submitOrderRequestFunc(
                    from_station, to_station, station_date=station_date)
                if 'data' not in sub_result:
                    print(f'查询日期 {station_date}  {self.from_station}-{self.to_station} 车次, 返回结果不正确... {broken_data_num}')
                    broken_data_num += 1
                else:
                    station_ticket[station_date] = sub_result['data']

        if broken_data_num == len(self.station_dates):
            self.env_retry_limit += 1
        else:
            self.env_retry_limit += 0

        if not station_ticket:
            print(f"车次配置信息有误，或者返回数据异常，请检查 {station_ticket}")
        if self.env_retry_limit >= self.retry_limit:
            _sleep_interval = 60 * 60 * 1
            print(f'连续请求{self.env_retry_limit}次， 数据返回结果不正确， 睡一觉{_sleep_interval} ...')
            time.sleep(_sleep_interval)

        have_trains = 0
        for _station_ticket in station_ticket:

            if 'result' not in station_ticket[_station_ticket]:
                print(f'查询日期 {_station_ticket}  {self.from_station}-{self.to_station} 车次, 坐席查询为空...')
            else:
                for i in station_ticket[_station_ticket]['result']:
                    ticket_info = i.split('|')
                    train_no = ticket_info[3]
                    # print(ticket_info[3], ticket_info[11] ,  ticket_info[1] ,self.ticket_black_list.__contains__(train_no) )

                    if ticket_info[3] in self.station_trains:
                        have_trains += 1
                        if self.ticket_black_list.__contains__(train_no) and (datetime.datetime.now() - self.ticket_black_list[train_no]).seconds < int(self.ticket_black_list_time):
                            print(f"{_station_ticket} 该车次{train_no} 正在被关小黑屋，跳过此车次")
                            # self.ticket_black_list[train_no] = datetime.datetime.now()
                        elif ticket_info[11] == "Y" and ticket_info[1] == "预订":  # 筛选未在开始时间内的车次
                            for j in range(len(self._station_seat)):
                                is_ticket_pass = ticket_info[self.station_seat(
                                    self._station_seat[j])]
                                # print self._station_seat[j]
                                # 过滤有效目标车次
                                if is_ticket_pass != '' and is_ticket_pass != '无' and is_ticket_pass != '*':
                                    # tiket_station_values = [k for k in station_value['map'].values()]
                                    self.secretStr = ticket_info[0]
                                    print (f'车次:  {train_no} 发车日期{_station_ticket}   始发车站: {self.from_station}  终点站: {self.to_station}  {self._station_seat[j]} {ticket_info[self.station_seat(self._station_seat[j])]} ')

                                    print ('正在尝试提交订票...', end=' ')
                                    # self.submitOrderRequestFunc(from_station, to_station, self.time())
                                    self.submit_station()
                                    self.getPassengerTicketStr(
                                        self._station_seat[j])
                                    self.getRepeatSubmitToken()
                                    if not self.user_info:  # 修改每次都调用用户接口导致用户接口不能用
                                        print('检查联系人', end=' ')
                                        self.user_info = self.getPassengerDTOs()
                                    if self.checkOrderInfo(train_no, self._station_seat[j]):
                                        break
                                else:
                                    pass
                        else:
                            pass

                time.sleep(self.expect_refresh_interval)
                # else:
                #     print("车次配置信息有误，或者返回数据异常，请检查 {}".format(station_ticket))
        if not have_trains:
            print(f'此次查询结果中没有 {self.station_trains}  {self.from_station}-{self.to_station} 请确认配置项...')
            self.env_retry_limit += 1

    def check_user(self):
        """
        检查用户是否达到订票条件
        :return:
        """
        # check_user_url = 'https://kyfw.12306.cn/otn/login/checkUser'
        # data = dict(_json_att=None)
        uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        # data = dict(_json_att=None)
        data = {"appid": "otn","t" : time.time()}
        # self.s.post(uamtk_url, data=uamtk_data, verify=False)
        check_user = self.login.s.post(uamtk_url, data=data, verify=False)
        print(check_user.text[:300])
        print(self.s.post(uamtk_url, data=data, verify=False).text)
        check_user = check_user.json()
        # check_user_flag = check_user['data']['flag']
        if check_user['result_code'] != 0:
                # self.login.logout()
            # if check_user['messages']:
                print ('用户检查失败：%s，可能未登录，可能session已经失效' %
                       check_user['result_message'])
                print ('正在尝试重新登录')
                self.call_login()
                self.is_check_user["user_time"] = datetime.datetime.now()
            # else:
            #     print ('用户检查失败： %s，可能未登录，可能session已经失效' % check_user)
            #     print ('正在尝试重新登录')
            #     self.call_login()
            #     self.is_check_user["user_time"] = datetime.datetime.now()

    def submit_station(self):
        """
        提交车次
        预定的请求参数，注意参数顺序
        注意这里为了防止secretStr被urllib.parse过度编码，在这里进行一次解码
        否则调用HttpTester类的post方法将会将secretStr编码成为无效码,造成提交预定请求失败
        :param self:
        :param secretStr: 提交车次加密
        :return:
        """

        submit_station_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = [('secretStr', urllib.parse.unquote(self.secretStr)),  # 字符串加密
                ('train_date', self.time()),  # 出发时间
                ('back_train_date', self.time()),  # 返程时间
                ('tour_flag', 'dc'),  # 旅途类型
                ('purpose_codes', 'ADULT'),  # 成人票还是学生票
                ('query_from_station_name', self.from_station),  # 起始车站
                ('query_to_station_name', self.to_station),  # 终点车站
                ]

        submitResult = self.s.post(
            submit_station_url, allow_redirects=False, data=data, verify=False)
        _max_try = 0
        while submitResult.status_code is not 200 and _max_try < 20:
            _max_try += 1
            print(f'submigResult.status_code {submitResult.status_code}' )
            submitResult = self.s.post(
                submit_station_url, allow_redirects=False, data=data, verify=False)
        submitResult = submitResult.json()
        print(submitResult)
        if 'data' in submitResult and submitResult['data']:
            if submitResult['data'] == 'N':
                print ('出票成功', end=' ')
            else:
                print ('出票失败', end=' ')
        elif 'messages' in submitResult and submitResult['messages']:
            msg = submitResult['messages'][0]
            print(msg)
            if '未完成订单' in  msg :
                mail_content = f'也许您有未完成订单，请立即打开浏览器登录12306，访问‘未完成订单’，在30分钟内完成支付！{msg} \n 12306 Account  { _get_yaml(self.ticket_config)["set"]["12306count"] } '
                email(mail_content, self.ticket_config).sendEmail()
            elif '未登陆' in msg:
                self.call_login()
                raise lostLoginInfomationException()
            raise ticketIsExitsException(submitResult['messages'][0])

    def getPassengerTicketStr(self, set_type):
        """
        获取getPassengerTicketStr 提交对应的代号码
        :param str: 坐席
        :return: 
        """

        # passengerTicketStr = {
        #     "商务座": "SWZ",
        #     "特等座": "TZ",
        #     "一等座": "ZY",
        #     "二等座": "ZE",
        #     "高级软卧": "GR",
        #     "软卧": "RW",
        #     "硬卧": "YW",
        #     "动卧": "SRRB",
        #     "高级动卧": "YYRW",
        #     "软座": "RZ",
        #     "硬座": "YZ",
        #     "无座": "WZ"}

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
        ticket_type = {'adult': "1", 'child': "2",
                       'student': "3", 'disability': "4"}
        return ticket_type

    def getPassengerTicketStrListAndOldPassengerStr(self):
        """
        获取提交车次人内容格式
        passengerTicketStr	O,0,1,文贤平,1,43052419950223XXXX,15618715583,N_O,0,1,梁敏,1,43052719920118XXXX,,N
        oldPassengerStr	文贤平,1,43052719920118XXXX,1_梁敏,1,43052719920118XXXX,1_
        :return:
        """
        passengerTicketStrList = []
        oldPassengerStr = []
        if not self.user_info:
            raise PassengerUserException("联系人不在列表中，请查证后添加")
        if len(self.user_info) is 1:
            passengerTicketStrList.append(
                '0,' + self.user_info[0]['passenger_type'] + "," + self.user_info[0][
                    "passenger_name"] + "," +
                self.user_info[0]['passenger_id_type_code'] + "," + self.user_info[0]['passenger_id_no'] + "," +
                self.user_info[0]['mobile_no'] + ',N')
            oldPassengerStr.append(
                self.user_info[0]['passenger_name'] + "," + self.user_info[0]['passenger_id_type_code'] + "," +
                self.user_info[0]['passenger_id_no'] + "," + self.user_info[0]['passenger_type'] + '_')
        else:
            for i in range(len(self.user_info)):
                passengerTicketStrList.append(
                    '0,' + self.user_info[i]['passenger_type'] + "," + self.user_info[i][
                        "passenger_name"] + "," + self.user_info[i]['passenger_id_type_code'] + "," + self.user_info[i][
                        'passenger_id_no'] + "," + self.user_info[i]['mobile_no'] + ',N_' + self.set_type)
                oldPassengerStr.append(
                    self.user_info[i]['passenger_name'] + "," + self.user_info[i]['passenger_id_type_code'] + "," +
                    self.user_info[i]['passenger_id_no'] + "," + self.user_info[i]['passenger_type'] + '_')
        return passengerTicketStrList, oldPassengerStr

    def checkOrderInfo(self, train_no, set_type):
        """
        检查支付订单，需要提交REPEAT_SUBMIT_TOKEN
        passengerTicketStr : 座位编号,0,票类型,乘客名,证件类型,证件号,手机号码,保存常用联系人(Y或N)
        oldPassengersStr: 乘客名,证件类型,证件号,乘客类型
        :return: 
        """
        passengerTicketStrList, oldPassengerStr = self.getPassengerTicketStrListAndOldPassengerStr()
        # print('*'* 20 )
        # print(passengerTicketStrList)
        # print(oldPassengerStr)
        # print('*'* 20 )
        checkOrderInfoUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data = OrderedDict()
        data['cancel_flag'] = 2
        data['bed_level_order_num'] = "000000000000000000000000000000"
        data['passengerTicketStr'] = self.set_type + "," + \
            ",".join(passengerTicketStrList).rstrip(
                "_{0}".format(self.set_type))
        data['oldPassengerStr'] = "".join(oldPassengerStr)
        data['tour_flag'] = 'dc'
        data['whatsSelect'] = 1
        data['REPEAT_SUBMIT_TOKEN'] = self.token
        # print(checkOrderInfoUrl, data)
        checkOrderInfo = self.s.post(
            checkOrderInfoUrl, data=data, verify=False).json()
        if 'data' in checkOrderInfo:
            if "ifShowPassCode" in checkOrderInfo["data"] and checkOrderInfo["data"]["ifShowPassCode"] == "Y":
                is_need_code = True
                if self.getQueueCount(train_no, set_type, is_need_code):
                    return True
            if "ifShowPassCode" in checkOrderInfo["data"] and checkOrderInfo['data']['submitStatus'] is True:
                print ('车票提交通过，正在尝试排队')
                is_need_code = False
                if self.getQueueCount(train_no, set_type, is_need_code):
                    return True
            else:
                if "errMsg" in checkOrderInfo['data'] and checkOrderInfo['data']["errMsg"]:
                    print("checkOrderInfo 排队异常，错误信息：{0}, 将此列车 {1}加入小黑屋".format(
                        checkOrderInfo['data']["errMsg"], train_no))
                    self.ticket_black_list[train_no] = datetime.datetime.now()

                else:
                    print(checkOrderInfo)
        elif 'messages' in checkOrderInfo and checkOrderInfo['messages']:
            print(checkOrderInfo['messages'][0])

    def getQueueCount(self, train_no, set_type, is_need_code):
        """
        # 模拟查询当前的列车排队人数的方法
        # 返回信息组成的提示字符串
        :param token:
        :return:
        """
        l_time = time.localtime(time.time())
        new_train_date = time.strftime("%a %b %d %Y", l_time)
        getQueueCountUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        data = {
            'train_date': str(new_train_date) + " 00:00:00 GMT+0800 (中国标准时间)",
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
        getQueueCountResult = self.s.post(
            getQueueCountUrl, data=data, verify=False).json()
        if "status" in getQueueCountResult and getQueueCountResult["status"] is True:
            if "countT" in getQueueCountResult["data"]:
                ticket = getQueueCountResult["data"]["count"]
                print(getQueueCountResult)
                ticket_split = sum(map(self.conversion_int, ticket.split(
                    ","))) if ticket.find(",") != -1 else ticket
                countT = getQueueCountResult["data"]["countT"]
                if int(countT) is 0:
                    if int(ticket_split) < len(self.user_info):
                        print(f"当前余票数小于乘车人数，放弃订票 {ticket_split}  ")
                    else:
                        print("排队成功, 当前余票还剩余: {0} 张".format(ticket_split))
                        
                        if self.checkQueueOrder(is_need_code):
                            return True
                else:
                    print("当前排队人数:" + str(countT) +
                          "当前余票还剩余:{0} 张，继续排队中".format(ticket_split))
            else:
                print("排队发现未知错误{0}，将此列车 {1}加入小黑屋".format(
                    getQueueCountResult, train_no))
                self.ticket_black_list[train_no] = datetime.datetime.now()
        elif "messages" in getQueueCountResult and getQueueCountResult["messages"]:
            print("getQueueCount 排队异常，错误信息：{0}, 将此列车 {1}加入小黑屋".format(
                getQueueCountResult["messages"][0], train_no))
            self.ticket_black_list[train_no] = datetime.datetime.now()
        else:
            if "validateMessages" in getQueueCountResult and getQueueCountResult["validateMessages"]:
                print(str(getQueueCountResult["validateMessages"]))
                self.ticket_black_list[train_no] = datetime.datetime.now()
            else:
                print("未知错误 {0}".format("".join(getQueueCountResult)))

    def checkQueueOrder(self, is_node_code=False):
        """
        模拟提交订单是确认按钮，参数获取方法还是get_ticketInfoForPassengerForm 中获取
        :return: 
        """

        passengerTicketStrList, oldPassengerStr = self.getPassengerTicketStrListAndOldPassengerStr()
        checkQueueOrderUrl = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
        data = {
            "passengerTicketStr": self.set_type + "," + ",".join(passengerTicketStrList).rstrip("_{0}".format(self.set_type)),
            "oldPassengerStr": "".join(oldPassengerStr),
            "purpose_codes": self.get_ticketInfoForPassengerForm()["purpose_codes"],
            "key_check_isChange": self.get_ticketInfoForPassengerForm()["key_check_isChange"],
            "leftTicketStr": self.get_ticketInfoForPassengerForm()["leftTicketStr"],
            "train_location": self.get_ticketInfoForPassengerForm()["train_location"],
            "seatDetailType": "000",   # 开始需要选择座位，但是目前12306不支持自动选择作为，那这个参数为默认
            "roomType": "00",  # 好像是根据一个id来判断选中的，两种 第一种是00，第二种是10，但是我在12306的页面没找到该id，目前写死是00，不知道会出什么错
            "dwAll": "N",
            "whatsSelect": 1,
            "_json_at": None,
            "REPEAT_SUBMIT_TOKEN": self.get_token(),
        }
        try:
            for i in range(5):
                if is_node_code:
                    print("正在使用自动识别验证码功能")
                    randurl = 'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn'
                    # codeimg = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&%s' % random.random()
                    # result = self.s.get(codeimg, verify=False)
                    # result = result.content
                    # self.check_user()
                    codeimg = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&%s' % random.random()
                    randCode = self.login.readImg(code_url=codeimg , method='post')
                    randData = {
                        "randCode": randCode,
                        "rand": "randp",
                        "_json_att": None,
                        "REPEAT_SUBMIT_TOKEN": self.get_token()
                    }
                    fresult = self.s.post(
                        randurl, data=randData, verify=False).json()  # 校验验证码是否正确
                    checkcode = fresult['data']['msg']
                    if checkcode == 'TRUE':
                        print("验证码通过,正在提交订单")
                        data['randCode'] = randCode
                        break
                    else:
                        print("验证码有误, 接口返回{0} 第{1}次尝试重试".format(fresult, i))
                        time.sleep(0.5)
                else:
                    print("不需要验证码")
                    break
            # print("".join(data))

            for i in range(5):
                try:
                    checkQueueOrderResult = self.s.post(
                        checkQueueOrderUrl, data=data, verify=False).json()
                except:
                    print(f"接口 {checkQueueOrderUrl} 无响应 重试{i}")
                    time.sleep(0.1)
                    if i > 3:
                        raise ValueError('12306 没救了')

            if "status" in checkQueueOrderResult and checkQueueOrderResult["status"]:
                c_data = checkQueueOrderResult["data"] if "data" in checkQueueOrderResult else {
                }
                if 'submitStatus' in c_data and c_data['submitStatus'] is True:
                    print("提交订单成功！")
                    self.queryOrderWaitTime()
                else:
                    if 'errMsg' in c_data and c_data['errMsg']:
                        print("提交订单失败，{0}".format(c_data['errMsg']))
                    else:
                        print(c_data)
                        print('订票失败!很抱歉,请重试提交预订功能!')
            elif "messages" in checkQueueOrderResult and checkQueueOrderResult["messages"]:
                print("提交订单失败,错误信息: " + checkQueueOrderResult["messages"])
            else:
                print(f"提交订单中，请耐心等待：{checkQueueOrderResult.text}")
        except ValueError:
            print("接口 {} 无响应".format(checkQueueOrderUrl))

    def queryOrderWaitTime(self):
        """
        排队获取订单等待信息,每隔3秒请求一次，最高请求次数为20次！
        :return: 
        """
        # queryOrderWaitTimeUrl = "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime"
        # data = {
        #     "random": "{0}{1}".format(int(time.time()), random.randint(1, 9)),
        #     "tourFlag": "dc",
        #     "REPEAT_SUBMIT_TOKEN": self.get_token(),
        # }
        num = 1
        while True:
            _random = int(round(time.time() * 1000))
            num += 1
            if num > 30:
                print("超出排队时间，自动放弃，正在重新刷票")
                break
            try:
                # queryOrderWaitTimeUrl = "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={0}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={1}".format(_random, self.get_token())
                data = {"random": _random, "tourFlag": "dc"}
                queryOrderWaitTimeUrl = "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime"
                queryOrderWaitTimeResult = self.s.post(
                    queryOrderWaitTimeUrl, data=data, verify=False).json()
            except ValueError:
                queryOrderWaitTimeResult = {}
            if queryOrderWaitTimeResult:
                if "status" in queryOrderWaitTimeResult and queryOrderWaitTimeResult["status"]:
                    if "orderId" in queryOrderWaitTimeResult["data"] and queryOrderWaitTimeResult["data"]["orderId"] is not None:
                        mail_content = f'恭喜您订票成功，订单号为：{queryOrderWaitTimeResult["data"]["orderId"]}, 请立即打开浏览器登录12306，访问‘未完成订单’，在30分钟内完成支付！ \n 12306 Account  { _get_yaml(self.ticket_config)["set"]["12306count"] }'
                        email(mail_content, self.ticket_config).sendEmail()
                        raise ticketIsExitsException(mail_content)
                    elif "msg" in queryOrderWaitTimeResult["data"] and queryOrderWaitTimeResult["data"]["msg"]:
                        print(queryOrderWaitTimeResult["data"]["msg"])
                        break
                    elif "waitTime"in queryOrderWaitTimeResult["data"] and queryOrderWaitTimeResult["data"]["waitTime"]:
                        print(f'排队等待时间预计还剩 {0 - queryOrderWaitTimeResult["data"]["waitTime"]} ms')
                    else:
                        print ("正在等待中")
                elif "messages" in queryOrderWaitTimeResult and queryOrderWaitTimeResult["messages"]:
                    print(f'排队等待失败： {queryOrderWaitTimeResult["messages"]}')
                else:
                    print(f"第{num}次排队中,请耐心等待")
            else:
                print("排队中")
            time.sleep(1)
        order_id = self.queryMyOrderNoComplete()  # 尝试查看订单列表，如果有订单，则判断成功，不过一般可能性不大
        if order_id:
            email("恭喜您订票成功，订单号为：{0}, 请立即打开浏览器登录12306，访问‘未完成订单’，在30分钟内完成支付！".format(
                order_id), self.ticket_config).sendEmail()
            raise ticketIsExitsException(
                "恭喜您订票成功，订单号为：{0}, 请立即打开浏览器登录12306，访问‘未完成订单’，在30分钟内完成支付！".format(order_id))

        else:
            print(ticketNumOutException("订单提交失败！,正在重新刷票"))

    def queryMyOrderNoComplete(self):
        """
        获取订单列表信息
        :return:
        """
        self.initNoComplete()
        queryMyOrderNoCompleteUrl = "https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete"
        data = {"_json_att": None}
        try:
            queryMyOrderNoCompleteResult = self.s.post(
                queryMyOrderNoCompleteUrl, data=data, verify=False).json()
        except ValueError:
            queryMyOrderNoCompleteResult = {}
        if queryMyOrderNoCompleteResult:
            if "data" in queryMyOrderNoCompleteResult and queryMyOrderNoCompleteResult["data"] and "orderDBList" in queryMyOrderNoCompleteResult["data"] and queryMyOrderNoCompleteResult["data"]["orderDBList"]:
                orderId = queryMyOrderNoCompleteResult["data"]["orderDBList"][0]["sequence_no"]
                return orderId
            elif "data" in queryMyOrderNoCompleteResult and "orderCacheDTO" in queryMyOrderNoCompleteResult["data"] and queryMyOrderNoCompleteResult["data"]["orderCacheDTO"]:
                if "message" in queryMyOrderNoCompleteResult["data"]["orderCacheDTO"] and queryMyOrderNoCompleteResult["data"]["orderCacheDTO"]["message"]:
                    print(
                        queryMyOrderNoCompleteResult["data"]["orderCacheDTO"]["message"]["message"])
                    raise ticketNumOutException(
                        queryMyOrderNoCompleteResult["data"]["orderCacheDTO"]["message"]["message"])
            else:
                if "message" in queryMyOrderNoCompleteResult and queryMyOrderNoCompleteResult["message"]:
                    print(queryMyOrderNoCompleteResult["message"])
                    return False
                else:
                    return False
        else:
            print("接口 {} 无响应".format(queryMyOrderNoCompleteUrl))

    def initNoComplete(self):
        """
        获取订单前需要进入订单列表页，获取订单列表页session
        :return:
        """
        initNoCompleteUrl = "https://kyfw.12306.cn/otn/queryOrder/initNoComplete"
        data = {"_json_att": None}
        self.s.post(initNoCompleteUrl, data=data, verify=False)

    # def call_submit_ticket(self, function_name=None):
    #     """
    #     订票失败回调方法，默认执行submitOrderRequest()
    #     此方法暂不使用
    #     :param function_name:
    #     :return:
    #     """
    #     if function_name:
    #         self.function_name()
    #     else:
    #         self.submitOrderRequest()

    def call_login(self):
        """登录回调方法"""
        #login.go_login(self.ticket_config).go_login()
        login.GoLogin(self.ticket_config).go_login()
        # self.call_login()

    def main(self):
         
        self.call_login()

        from_station, to_station = self.station_table(
            self.from_station, self.to_station)
        # if self.leftTicketLog(from_station, to_station):
        num = 1
        while 1:
            try:
                num += 1 
                if "user_time" in self.is_check_user and (datetime.datetime.now() - self.is_check_user["user_time"]).seconds / 60 > 5:
                    # 十分钟调用一次检查用户是否登录
                    self.check_user()
                print('begin' ,end=' ')
                time.sleep(self.select_refresh_interval)
                if time.strftime('%H:%M:%S', time.localtime(time.time())) > "23:00:00":
                    print("12306休息时间，本程序自动停止,明天早上七点将自动运行")
                    time.sleep(60 * 60 * 7)
                    self.call_login()
                start_time = datetime.datetime.now()
                self.submitOrderRequestImplement(from_station, to_station)

                print(f"执行时间 {datetime.datetime.now()}  正在第{num}次查询  乘车日期: {self.station_dates}  车次{self.station_trains} 查询无票  代理设置 无  总耗时{ (datetime.datetime.now() - start_time).microseconds / 1000}ms")
            except PassengerUserException as e:
                traceback.print_exc()
                break
            except ticketConfigException as e:
                traceback.print_exc()
                break
            except ticketIsExitsException as e:
                traceback.print_exc()
                break
            except ticketNumOutException as e:
                traceback.print_exc()
                break
            except JSONDecodeError as e:
                traceback.print_exc()
            except ValueError as e:
                # traceback.print_exc()
                print()
                if e.msg == "No JSON object could be decoded":
                    print("12306接口无响应，正在重试")
            except KeyError as e:
                traceback.print_exc()
            except TypeError as e:
                traceback.print_exc()
            except socket.error as e:
                traceback.print_exc()
            except lostLoginInfomationException as e:
                self.call_login()



if __name__ == '__main__':
    login.go_login().login()
    # a = select('上海', '北京')
    # a.main()
