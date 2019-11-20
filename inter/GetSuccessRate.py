from collections import OrderedDict


from config.urlConf import urls
import TickerConfig
from inter.SubmitOrderRequest import submitOrderRequestByAfterNate


class getSuccessRate:
    def __init__(self, session, secretList):
        """
        获取成功信息
        """
        self.secretList = secretList
        self.session = session

    def data_apr(self):
        """
        secretList	9vqa9%2B%2F%2Fsdozmm22hpSeDTGqRUwSuA2D0r%2BmU%2BLZj7MK7CDuf5Ep1xpxl4Dyxfmoah%2BaB9TZSesU%0AkxBbo5oNgR1vqMfvq66VP0T7tpQtH%2BbVGBz1FolZG8jDD%2FHqnz%2FnvdBP416Og6WGS14O%2F3iBSwT8%0AkRPsNF0Vq0U082g0tlJtP%2BPn7TzW3z7TDCceMJIjFcfEOA%2BW%2BuK%2Bpy6jCQMv0TmlkXf5aKcGnE02%0APuv4I8nF%2BOWjWzv9CrJyiCZiWaXd%2Bi7p69V3a9dhF787UgS660%2BqKRFB4RLwAfic3MkAlfpGWhMY%0ACfARVQ%3D%3D#O
        _json_att
        候补一次只能补一个座位，默认取TICKET_TYPE第一个
        :return:
        """

        ticker = TickerConfig.PASSENGER_TICKER_STR.get(TickerConfig.SET_TYPE[0])
        data = OrderedDict()
        data["successSecret"] = f"{self.secretList}#{ticker}"
        data["_json_att"] = ""
        return data

    def sendSuccessRate(self):
        successRateRsp = self.session.httpClint.send(urls.get("getSuccessRate"), self.data_apr())
        if not successRateRsp.get("status"):
            print("".join(successRateRsp.get("messages")) or successRateRsp.get("validateMessages"))
            return
        flag = successRateRsp.get("data", {}).get("flag")[0]
        train_no = flag.get("train_no")
        print(f"准备提交候补订单，{flag.get('info')}")
        submit = submitOrderRequestByAfterNate(self.session, self.secretList, train_no)
        submit.sendSubmitOrderRequest()

