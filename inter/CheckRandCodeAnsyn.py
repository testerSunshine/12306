# coding=utf-8
class checkRandCodeAnsyn:
    def __init__(self, session, randCode, token):
        self.session = session
        self.randCode = randCode
        self.token = token

    def data_par(self):
        """
        :return:
        """
        data = {
            "randCode": self.randCode,
            "rand": "randp",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.token
        }
        return data

    def sendCheckRandCodeAnsyn(self):
        """
        下单验证码识别
        :return:
        """
        checkRandCodeAnsynUrl = self.session.urls["checkRandCodeAnsyn"]
        fresult = self.session.httpClint.send(checkRandCodeAnsynUrl, self.data_par())  # 校验验证码是否正确
        return fresult['data']['msg']