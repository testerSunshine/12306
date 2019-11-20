from collections import OrderedDict
from config.urlConf import urls
import TickerConfig
from inter.GetQueueCount import queryQueueByAfterNate


class confirmHB:
    def __init__(self, secretList, session, tickerNo, jzdhDate):
        """
        人脸识别
        """
        self.secretList = secretList
        self.session = session
        self.passengerTicketStrByAfterLate = session.passengerTicketStrByAfterLate
        self.tickerNo = tickerNo
        self.jzdhDate = jzdhDate

    def data_apr(self):
        """
        passengerInfo	1#XXXX#1#***************77X#bf6ae40d3655ae7eff005ee21d95876b38ab97a8031b464bc2f74a067e3ec957;
        jzParam	2019-08-31#19#00
        hbTrain	5l000G177230,O#
        lkParam
        :return:
        """
        ticker = TickerConfig.PASSENGER_TICKER_STR.get(TickerConfig.SET_TYPE[0])
        data = OrderedDict()
        data["passengerInfo"] = self.passengerTicketStrByAfterLate
        data["jzParam"] = self.jzdhDate
        data["hbTrain"] = f"{self.tickerNo},{ticker}#"
        data["lkParam"] = ""
        return data

    def sendChechFace(self):
        ChechFaceRsp = self.session.httpClint.send(urls.get("confirmHB"), self.data_apr())
        if not ChechFaceRsp.get("status"):
            print("".join(ChechFaceRsp.get("messages")) or ChechFaceRsp.get("validateMessages"))
            return
        data = ChechFaceRsp.get("data")
        if not data.get("flag"):
            print(f"错误信息：{data.get('msg')}")
            return
        queue = queryQueueByAfterNate(self.session)
        queue.sendQueryQueueByAfterNate()




