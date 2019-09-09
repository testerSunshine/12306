import datetime
import urllib
from collections import OrderedDict
from config.urlConf import urls
import TickerConfig
from inter.GetSuccessRate import getSuccessRate
from myException.ticketConfigException import ticketConfigException
import wrapcache


class chechFace:
    def __init__(self, session, secretList, train_no):
        """
        人脸识别
        """
        self.secretList = secretList
        self.session = session
        self.train_no = train_no

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

    def sendChechFace(self):
        chechFaceRsp = self.session.httpClint.send(urls.get("chechFace"), self.data_apr())
        if not chechFaceRsp.get("status"):
            print("".join(chechFaceRsp.get("messages")) or chechFaceRsp.get("validateMessages"))
            wrapcache.set(key=f"hb{self.train_no}", value=datetime.datetime.now(),
                          timeout=TickerConfig.TICKET_BLACK_LIST_TIME * 60)
            return
        data = chechFaceRsp["data"]
        if not data.get("face_flag"):
            """
            未通过人脸核验
            """
            raise ticketConfigException("通过人证一致性核验的用户及激活的“铁路畅行”会员可以提交候补需求，请您按照操作说明在铁路12306app.上完成人证核验")
        g = getSuccessRate(self.session, self.secretList)
        g.sendSuccessRate()


