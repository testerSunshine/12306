# -*- coding=utf-8 -*-
import json
import datetime
import random
import re
import urllib
import sys
import time
from collections import OrderedDict

from config.ticketConf import _get_yaml
from myException.PassengerUserException import PassengerUserException
from myException.ticketConfigException import ticketConfigException
from myException.ticketIsExitsException import ticketIsExitsException
from myException.ticketNumOutException import ticketNumOutException
from myUrllib import myurllib2

reload(sys)
sys.setdefaultencoding('utf-8')


class select:
    def __init__(self):
        self.from_station, self.to_station, self.station_date, self._station_seat, self.is_more_ticket, self.ticke_peoples, self.select_refresh_interval, self.station_trains, self.expect_refresh_interval, self.ticket_black_list_time = self.get_ticket_info()
        self.order_request_params = {}  # 订单提交时的参数
        self.ticketInfoForPassengerForm = {}  # 初始化当前页面参数
        self.current_seats = {}  # 席别信息
        self.token = ""
        self.set_type = ""
        self.user_info = ""
        self.secretStr = ""
        self.ticket_black_list = dict()

    def get_ticket_info(self):
        """
        获取配置信息
        :return:
        """
        ticket_info_config = _get_yaml()
        from_station = ticket_info_config["set"]["from_station"].encode("utf8")
        to_station = ticket_info_config["set"]["to_station"].encode("utf8")
        station_date = ticket_info_config["set"]["station_date"].encode("utf8")
        set_type = ticket_info_config["set"]["set_type"]
        is_more_ticket = ticket_info_config["set"]["is_more_ticket"].encode("utf8")
        ticke_peoples = ticket_info_config["ticke_peoples"]
        select_refresh_interval = ticket_info_config["set"]["select_refresh_interval"]
        station_trains = ticket_info_config["set"]["station_trains"]
        expect_refresh_interval = ticket_info_config["set"]["expect_refresh_interval"]
        ticket_black_list_time = ticket_info_config["set"]["ticket_black_list_time"]
        print "*"*20
        print "当前配置：出发站：{0}\n到达站：{1}\n乘车日期：{2}\n坐席：{3}\n是否有票自动提交：{4}\n乘车人：{5}\n刷新间隔：{6}\n候选购买车次：{7}\n未开始刷票间隔时间：{8}\n僵尸票关小黑屋时长：{9}\n".format\
                                                                                      (
                                                                                      from_station,
                                                                                      to_station,
                                                                                      station_date,
                                                                                      ",".join(set_type),
                                                                                      is_more_ticket,
                                                                                      ",".join(ticke_peoples),
                                                                                      select_refresh_interval,
                                                                                      ",".join(station_trains),
                                                                                      expect_refresh_interval,
                                                                                      ticket_black_list_time,
            )
        print "*"*20
        return from_station, to_station, station_date, set_type, is_more_ticket, ticke_peoples, select_refresh_interval, station_trains, expect_refresh_interval, ticket_black_list_time

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
        result = open('station_name.txt')
        info = result.read().split('=')[1].strip("'").split('@')
        del info[0]
        station_name = {}
        for i in range(0, len(info)):
            n_info = info[i].split('|')
            station_name[n_info[1]] = n_info[2]
        from_station = station_name[from_station.encode("utf8")]
        to_station = station_name[to_station.encode("utf8")]
        return from_station, to_station

    def time(self):
        """
        获取日期
        :return:
        """
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
        jsonData = json.loads(myurllib2.Post(get_passengerDTOs, get_data))
        if 'data' in jsonData and jsonData['data'] and 'normal_passengers' in jsonData['data'] and jsonData['data'][
            'normal_passengers']:
            # return jsonData['data']['normal_passengers']
            normal_passengers = jsonData['data']['normal_passengers']
            _normal_passenger = [normal_passengers[i] for i in range(len(normal_passengers))if normal_passengers[i]["passenger_name"] in self.ticke_peoples]
            return _normal_passenger if _normal_passenger else normal_passengers[0]  # 如果配置乘车人没有在账号，则默认返回第一个用户
        else:
            if 'data' in jsonData and 'exMsg' in jsonData['data'] and jsonData['data']['exMsg']:
                print(jsonData['data']['exMsg'])
            elif 'messages' in jsonData and jsonData['messages']:
                print(jsonData['messages'][0])
            else:
                print("未查找到常用联系人")
                raise PassengerUserException("未查找到常用联系人,请先添加联系人在试试")

    def submitOrderRequest(self, from_station, to_station):
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
        select_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={0}&leftTicketDTO.from_station={1}&leftTicketDTO.to_station={2}&purpose_codes=ADULT'.format(self.station_date, from_station, to_station)
        leftTicketLogUrl = 'https://kyfw.12306.cn/otn/leftTicket/log?leftTicketDTO.train_date={0}&leftTicketDTO.from_station={1}&leftTicketDTO.to_station={2}&purpose_codes=ADULT'.format(self.station_date, from_station, to_station)
        leftTicketLog = json.loads(myurllib2.get(leftTicketLogUrl), encoding='utf-8')
        if "status" in leftTicketLog and leftTicketLog["status"] is True:
            station_ticket = json.loads(myurllib2.get(select_url), encoding='utf-8')
            value = station_ticket['data']
            if not value:
                print ('{0}-{1} 车次坐席查询为空...'.format(self.from_station, self.to_station))
            else:
                if value['result']:
                    for i in value['result']:
                        ticket_info = i.split('|')
                        if ticket_info[11] == "Y" and ticket_info[1] == "预订":  # 筛选未在开始时间内的车次
                            for j in range(len(self._station_seat)):
                                is_ticket_pass = ticket_info[self.station_seat(self._station_seat[j].encode("utf8"))]
                                # print self._station_seat[j]
                                if is_ticket_pass != '' and is_ticket_pass != '无' and ticket_info[3] in self.station_trains and is_ticket_pass != '*':  # 过滤有效目标车次
                                    # tiket_values = [k for k in value['map'].values()]
                                    self.secretStr = ticket_info[0]
                                    train_no = ticket_info[3]
                                    print ('车次: ' + train_no + ' 始发车站: ' + self.to_station + ' 终点站: ' +
                                           self.to_station + ' ' + self._station_seat[j].encode("utf8") + ':' + ticket_info[self.station_seat(self._station_seat[j].encode("utf8"))])
                                    if self.ticket_black_list.has_key(train_no) and (self.ticket_black_list["train_no"] - datetime.datetime.now()).seconds/60 < self.ticket_black_list_time:
                                        print("该车次{} 正在被关小黑屋，跳过此车次".format(train_no))
                                    else:
                                        print ('正在尝试提交订票...')
                                        if self.check_user():
                                            self.submit_station()
                                            self.getPassengerTicketStr(self._station_seat[j].encode("utf8"))
                                            self.getRepeatSubmitToken()
                                            self.user_info = self.getPassengerDTOs()
                                            if self.checkOrderInfo():
                                                if self.getQueueCount(train_no):
                                                    break
                                else:
                                    pass
                            print "当前车次{0} 查询无符合条件坐席，正在重新查询".format(ticket_info[3])
                        elif ticket_info[11] == "N":
                            print("当前车次{0} 无票".format(ticket_info[3]))
                        else:
                            print("当前这次还处于待售状态，请耐心等待")
                            time.sleep(self.expect_refresh_interval)
                else:
                    raise ticketConfigException("车次配置信息有误，请检查")
        else:
            if "message" in leftTicketLog and leftTicketLog["message"]:
                print leftTicketLog["message"]
            elif "validateMessages" in leftTicketLog and leftTicketLog["validateMessages"]:
                print leftTicketLog["validateMessages"]

    def check_user(self):
        """
        检查用户是否达到订票条件
        :return:
        """
        check_user_url = 'https://kyfw.12306.cn/otn/login/checkUser'
        data = dict(_json_att=None)
        check_user = json.loads(myurllib2.Post(check_user_url, data), encoding='utf-8')
        check_user_flag = check_user['data']['flag']
        if check_user_flag is True:
            print ('订票成功!')
            print ('尝试提交订单...')
            return True
        else:
            if check_user['messages']:
                print ('用户检查失败：%s，可能未登录，可能session已经失效' % check_user['messages'][0])
            else:
                print ('用户检查失败： %s，可能未登录，可能session已经失效' % check_user)

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
        data = [('secretStr', urllib.unquote(self.secretStr)),  # 字符串加密
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
            else:
                print ('出票失败')
        elif 'messages' in submitResult and submitResult['messages']:
            print(submitResult['messages'][0])
            raise ticketIsExitsException("检查到有未支付的订单，程序自动停止")

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

    def getPassengerTicketStrListAndOldPassengerStr(self):
        """
        获取提交车次人内容格式
        passengerTicketStr	O,0,1,文贤平,1,43052419950223XXXX,15618715583,N_O,0,1,梁敏,1,43052719920118XXXX,,N
        oldPassengerStr	文贤平,1,43052719920118XXXX,1_梁敏,1,43052719920118XXXX,1_
        :return:
        """
        passengerTicketStrList = []
        oldPassengerStr = []
        if len(self.user_info) is 1:
            passengerTicketStrList.append(
                '0,' + self.user_info[0]['passenger_id_type_code'] + "," + self.user_info[0][
                    "passenger_name"] + "," +
                self.user_info[0]['passenger_type'] + "," + self.user_info[0]['passenger_id_no'] + "," +
                self.user_info[0]['mobile_no'] + ',N')
            oldPassengerStr.append(
                self.user_info[0]['passenger_name'] + "," + self.user_info[0]['passenger_type'] + "," +
                self.user_info[0]['passenger_id_no'] + "," + self.user_info[0]['passenger_type'] + '_')
        else:
            for i in range(len(self.user_info)):
                passengerTicketStrList.append(
                    '0,' + self.user_info[i]['passenger_id_type_code'] + "," + self.user_info[i][
                        "passenger_name"] + "," + self.user_info[i]['passenger_type'] + "," + self.user_info[i][
                        'passenger_id_no'] + "," + self.user_info[i]['mobile_no'] + ',N_' + self.set_type)
                oldPassengerStr.append(
                    self.user_info[i]['passenger_name'] + "," + self.user_info[i]['passenger_type'] + "," +
                    self.user_info[i]['passenger_id_no'] + "," + self.user_info[i]['passenger_type'] + '_')
        return passengerTicketStrList, oldPassengerStr

    def checkOrderInfo(self):
        """
        检查支付订单，需要提交REPEAT_SUBMIT_TOKEN
        passengerTicketStr : 座位编号,0,票类型,乘客名,证件类型,证件号,手机号码,保存常用联系人(Y或N)
        oldPassengersStr: 乘客名,证件类型,证件号,乘客类型
        :return: 
        """
        passengerTicketStrList, oldPassengerStr = self.getPassengerTicketStrListAndOldPassengerStr()
        checkOrderInfoUrl = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data = OrderedDict()
        data['cancel_flag'] = 2
        data['bed_level_order_num'] = "000000000000000000000000000000"
        # 'passengerTicketStr': self.set_type+',0,'+self.user_info[0]['passenger_id_type_code']+","+self.user_info[0]["passenger_name"]+","+self.user_info[0]['passenger_type']+","+self.user_info[0]['passenger_id_no']+","+self.user_info[0]['mobile_no']+',N',
        # 'oldPassengerStr': self.user_info[0]['passenger_name']+","+self.user_info[0]['passenger_type']+","+self.user_info[0]['passenger_id_no']+","+self.user_info[0]['passenger_type']+'_',
        data['passengerTicketStr'] = self.set_type + "," + ",".join(passengerTicketStrList).rstrip("_{0}".format(self.set_type))
        data['oldPassengerStr'] = "".join(oldPassengerStr)
        data['tour_flag'] = 'dc'
        data['whatsSelect'] = 1
        data['REPEAT_SUBMIT_TOKEN'] = self.token
        checkOrderInfo = json.loads(myurllib2.Post(checkOrderInfoUrl, data, ))
        if 'data' in checkOrderInfo:
            if checkOrderInfo['data']['submitStatus'] is True:
                    print ('车票提交通过，正在尝试排队')
                    return True
            else:
                if "errMsg" in checkOrderInfo['data'] and checkOrderInfo['data']["errMsg"]:
                    print checkOrderInfo['data']["errMsg"]
                else:
                    print checkOrderInfo
        elif 'messages' in checkOrderInfo and checkOrderInfo['messages']:
            print (checkOrderInfo['messages'][0])
            print ("排队失败，重新刷票中")

    def getQueueCount(self, train_no):
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
        for i in range(3):
            print("第{0}次排队".format(i+1))
            getQueueCountResult = json.loads(myurllib2.Post(getQueueCountUrl, data))
            if "status" in getQueueCountResult and getQueueCountResult["status"] is True:
                if "countT" in getQueueCountResult["data"]:
                    ticket = getQueueCountResult["data"]["ticket"]
                    countT = getQueueCountResult["data"]["countT"]
                    if int(countT) is 0:
                        print("排队成功, 当前余票还剩余:" + ticket + "张")
                        if int(ticket) < len(self.user_info):
                            print("当前余票数小于乘车人数，放弃订票")
                        else:
                            if self.checkQueueOrder():
                                return True
                    else:
                        print("当前排队人数:" + str(countT) + "当前余票还剩余:" + getQueueCountResult["data"]["ticket"]+ "张，继续排队中")
                else:
                    print("排队发现未知错误{0}，将此列车 {1}加入小黑屋".format(getQueueCountResult, train_no))
                    self.ticket_black_list[train_no] = datetime.datetime.now()
                    break
            elif "messages" in getQueueCountResult and getQueueCountResult["messages"]:
                print("排队异常，错误信息：{0}, 将此列车 {1}加入小黑屋".format(getQueueCountResult["messages"][0], train_no))
                self.ticket_black_list[train_no] = datetime.datetime.now()
                break
            else:
                print(str(getQueueCountResult["validateMessages"]))
                self.ticket_black_list[train_no] = datetime.datetime.now()
                break
        time.sleep(1)

    def checkQueueOrder(self):
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
            "REPEAT_SUBMIT_TOKEN": self.get_token(),
        }
        checkQueueOrderResult = json.loads(myurllib2.Post(checkQueueOrderUrl, data))
        if "status" in checkQueueOrderResult and checkQueueOrderResult["status"]:
            c_data = checkQueueOrderResult["data"] if "data" in checkQueueOrderResult else {}
            if 'submitStatus' in c_data and c_data['submitStatus']:
                print("出票成功!")
                if self.queryOrderWaitTime():
                    return True
            else:
                if 'errMsg' in c_data and c_data['errMsg']:
                    print("出票失败，" + c_data['errMsg'])
                else:
                    print(c_data)
                    print('订票失败!很抱歉,请重试提交预订功能!')
        elif "messages" in checkQueueOrderResult and checkQueueOrderResult["messages"]:
            print("提交订单失败,错误信息: "+ checkQueueOrderResult["messages"])
        else:
            print("未知错误：" + str(checkQueueOrderResult["validateMessages"]))

    def queryOrderWaitTime(self):
        """
        排队获取订单等待信息,每隔3秒请求一次，最高请求次数为20次！
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
                print("超出排队时间，自动放弃，正在重新刷票")
                break
            queryOrderWaitTimeResult = json.loads(myurllib2.Post(queryOrderWaitTimeUrl, data))
            if "status" in queryOrderWaitTimeResult and queryOrderWaitTimeResult["status"]:
                if "orderId" in queryOrderWaitTimeResult["data"] and queryOrderWaitTimeResult["data"]["orderId"] != "null":
                    self.initNoComplete()
                    orderId = self.queryMyOrderNoComplete()
                    if orderId:
                        print ("恭喜您订票成功，订单号为：{0}, 请立即打开浏览器登录12306，访问‘未完成订单’，在30分钟内完成支付！".format(orderId))
                        return True
                    else:
                        print("等待出票中...")
                elif "msg" in queryOrderWaitTimeResult["data"] and queryOrderWaitTimeResult["data"]["msg"]:
                    print("订单提交失败：" + queryOrderWaitTimeResult["data"]["msg"])
                    break
            elif "messages" in queryOrderWaitTimeResult and queryOrderWaitTimeResult["messages"]:
                print("订单提交失败： " + queryOrderWaitTimeResult["messages"])
                break
            else:
                print("订单提交中,请耐心等待")
                time.sleep(3)

    def queryMyOrderNoComplete(self):
        """
        获取订单列表信息
        :return:
        """
        queryMyOrderNoCompleteUrl = "https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete"
        data = {"_json_att": None}
        queryMyOrderNoCompleteResult = json.loads(myurllib2.Post(queryMyOrderNoCompleteUrl, data))
        if "data" in queryMyOrderNoCompleteResult and queryMyOrderNoCompleteResult["data"] and "orderDBList" in queryMyOrderNoCompleteResult["data"] and queryMyOrderNoCompleteResult["data"]["orderDBList"]:
            orderId = queryMyOrderNoCompleteResult["data"]["orderDBList"][0]["sequence_no"]
            return orderId
        elif "orderCacheDTO" in queryMyOrderNoCompleteResult["data"] and queryMyOrderNoCompleteResult["data"]["orderCacheDTO"]:
            if "message" in queryMyOrderNoCompleteResult["data"]["orderCacheDTO"] and queryMyOrderNoCompleteResult["data"]["orderCacheDTO"]["message"]:
                print(queryMyOrderNoCompleteResult["data"]["orderCacheDTO"]["message"]["message"])
                raise ticketNumOutException(queryMyOrderNoCompleteResult["data"]["orderCacheDTO"]["message"]["message"])
        else:
            if "message" in queryMyOrderNoCompleteResult and queryMyOrderNoCompleteResult["message"]:
                print queryMyOrderNoCompleteResult["message"]
                return False
            else:
                return False

    def initNoComplete(self):
        """
        获取订单前需要进入订单列表页，获取订单列表页session
        :return:
        """
        initNoCompleteUrl = "https://kyfw.12306.cn/otn/queryOrder/initNoComplete"
        data = {"_json_att": None}
        myurllib2.Post(initNoCompleteUrl, data)

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

    def main(self):
        from_station, to_station = self.station_table(self.from_station, self.to_station)
        num = 1
        while 1:
            try:
                num += 1
                time.sleep(self.select_refresh_interval)
                if time.strftime('%H:%M:%S', time.localtime(time.time())) > "23:00:00":
                    print "12306休息时间，本程序自动停止,明天早上七点运行"
                    break
                start_time = datetime.datetime.now()
                self.submitOrderRequest(from_station, to_station)
                print "正在第{0}次查询 乘车日期: {1}, 总耗时{2}ms".format(num, self.station_date, (datetime.datetime.now()-start_time).microseconds/1000)
            except PassengerUserException as e:
                print e.message
                break
            except ticketConfigException as e:
                print e.message
                break
            except ticketIsExitsException as e:
                print e.message
                break
            except ticketNumOutException as e:
                print e.message
                break
            except ValueError as e:
                if e.message == "No JSON object could be decoded":
                    print("12306接口无响应，正在重试")
                else:
                    print(e.message)
            except Exception as e:
                print e.message


if __name__ == '__main__':
    a = select('上海', '北京')
    a.main()