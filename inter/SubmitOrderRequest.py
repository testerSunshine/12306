# coding=utf-8
import datetime
import urllib
from collections import OrderedDict
import TickerConfig
from config.urlConf import urls
from inter.CheckOrderInfo import checkOrderInfo
from inter.ConfirmHB import confirmHB
from inter.PassengerInitApi import passengerInitApi
from myException.ticketIsExitsException import ticketIsExitsException


def time():
    """
    获取日期
    :return:
    """
    today = datetime.date.today()
    return today.strftime('%Y-%m-%d')


class submitOrderRequest:
    def __init__(self, selectObj, secretStr, from_station, to_station, train_no, set_type,
                 passengerTicketStrList, oldPassengerStr, train_date, ticke_peoples):
        self.session = selectObj
        # self.secretStr = secretStr
        try:
            self.secretStr = urllib.unquote(secretStr)
        except AttributeError:
            self.secretStr = urllib.parse.unquote(secretStr)
        self.from_station = from_station
        self.to_station = to_station
        self.to_station = to_station
        self.train_no = train_no
        self.set_type = set_type
        self.passengerTicketStrList = passengerTicketStrList
        self.oldPassengerStr = oldPassengerStr
        self.train_date = train_date
        self.ticke_peoples = ticke_peoples

    def data_apr(self):
        """
        :return:
        """
        data = [('secretStr', self.secretStr),  # 字符串加密
                ('train_date', self.train_date),  # 出发时间
                ('back_train_date', time()),  # 返程时间
                ('tour_flag', 'dc'),  # 旅途类型
                ('purpose_codes', 'ADULT'),  # 成人票还是学生票
                ('query_from_station_name', TickerConfig.FROM_STATION),  # 起始车站
                ('query_to_station_name', TickerConfig.TO_STATION),  # 终点车站
                ('undefined', ''),
                ]
        return data

    def sendSubmitOrderRequest(self):
        """
        提交车次
        预定的请求参数，注意参数顺序
        注意这里为了防止secretStr被urllib.parse过度编码，在这里进行一次解码
        否则调用HttpTester类的post方法将会将secretStr编码成为无效码,造成提交预定请求失败
        :param secretStr: 提交车次加密
        :return:
        """
        submit_station_url = self.session.urls["submit_station_url"]
        submitResult = self.session.httpClint.send(submit_station_url, self.data_apr())
        if 'data' in submitResult and submitResult['data']:
            if submitResult['data'] == 'N':
                coi = checkOrderInfo(self.session, self.train_no, self.set_type, self.passengerTicketStrList,
                                     self.oldPassengerStr,
                                     self.train_date, self.ticke_peoples)
                coi.sendCheckOrderInfo()
            else:
                print (u'出票失败')
        elif 'messages' in submitResult and submitResult['messages']:
            raise ticketIsExitsException(submitResult['messages'][0])


class submitOrderRequestByAfterNate:
    def __init__(self, session, secretList, tickerNo):
        """
        提交候补订单
        :param secretList:
        :param session:
        """
        self.secretList = secretList
        self.session = session
        self.tickerNo = tickerNo

    def data_apr(self):
        """
        secretList	9vqa9%2B%2F%2Fsdozmm22hpSeDTGqRUwSuA2D0r%2BmU%2BLZj7MK7CDuf5Ep1xpxl4Dyxfmoah%2BaB9TZSesU%0AkxBbo5oNgR1vqMfvq66VP0T7tpQtH%2BbVGBz1FolZG8jDD%2FHqnz%2FnvdBP416Og6WGS14O%2F3iBSwT8%0AkRPsNF0Vq0U082g0tlJtP%2BPn7TzW3z7TDCceMJIjFcfEOA%2BW%2BuK%2Bpy6jCQMv0TmlkXf5aKcGnE02%0APuv4I8nF%2BOWjWzv9CrJyiCZiWaXd%2Bi7p69V3a9dhF787UgS660%2BqKRFB4RLwAfic3MkAlfpGWhMY%0ACfARVQ%3D%3D#O|
        _json_att
        候补一次只能补一个座位，默认取TICKET_TYPE第一个
        :return:
        """

        ticker = TickerConfig.PASSENGER_TICKER_STR.get(TickerConfig.SET_TYPE[0])
        data = OrderedDict()
        data["secretList"] = f"{self.secretList}#{ticker}|"
        data["_json_att"] = ""
        return data

    def sendSubmitOrderRequest(self, ):
        submitOrderRequestRsp = self.session.httpClint.send(urls.get("SubmitOrderRequestRsp"), self.data_apr())
        if not submitOrderRequestRsp.get("status") or not submitOrderRequestRsp.get("data", {}).get("flag"):
            print("".join(submitOrderRequestRsp.get("messages")) or submitOrderRequestRsp.get("validateMessages"))
            return
        pApi = passengerInitApi(self.session, self.secretList, self.tickerNo)
        pApi.sendPassengerInitApi()

