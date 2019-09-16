from config.urlConf import urls
from inter.ConfirmHB import confirmHB


class passengerInitApi:
    def __init__(self, session, secretList, tickerNo):
        """
        获取候补信息
        """
        self.secretList = secretList
        self.tickerNo = tickerNo
        self.session = session

    def sendPassengerInitApi(self):
        passengerInitApiRsp = self.session.httpClint.send(urls.get("passengerInitApi"))
        if not passengerInitApiRsp.get("status"):
            print("".join(passengerInitApiRsp.get("messages")) or passengerInitApiRsp.get("validateMessages"))
            return
        data = passengerInitApiRsp.get("data", {})
        jzdhDateE = data.get("jzdhDateE")
        jzdhHourE = data.get("jzdhHourE").replace(":", "#")
        jzdhDate = f"{jzdhDateE}#{jzdhHourE}"
        print(f"当前候补日期为:{jzdhDateE} {jzdhHourE}")
        confirm = confirmHB(self.secretList, self.session, self.tickerNo, jzdhDate)
        confirm.sendChechFace()




