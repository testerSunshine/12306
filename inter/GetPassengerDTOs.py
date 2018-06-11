# coding=utf-8
from config.TicketEnmu import ticket
from myException.PassengerUserException import PassengerUserException


class getPassengerDTOs:
    """
    获取乘客信息
    :return:
    """
    def __init__(self, session, ticket_peoples, set_type):
        """
        :param session: 登录实例
        :param ticket_peoples: 乘客
        :param set_type: 坐席
        """
        self.session = session
        self.ticket_peoples = ticket_peoples
        self.set_type = set_type.encode("utf8")

    def sendGetPassengerDTOs(self):
        getPassengerDTOsResult = self.session.httpClint.send(self.session.urls["get_passengerDTOs"], {})
        getPassengerDTOsResult["data"].get("normal_passengers", False)
        if getPassengerDTOsResult.get("data", False) and getPassengerDTOsResult["data"].get("normal_passengers", False):
            normal_passengers = getPassengerDTOsResult['data']['normal_passengers']
            _normal_passenger = [normal_passengers[i] for i in range(len(normal_passengers)) if
                                 normal_passengers[i]["passenger_name"] in self.ticket_peoples]
            return _normal_passenger if _normal_passenger else [normal_passengers[0]]  # 如果配置乘车人没有在账号，则默认返回第一个用户
        else:
            if getPassengerDTOsResult.get("data", False) and getPassengerDTOsResult['data'].get("exMsg", False):
                print(getPassengerDTOsResult['data'].get("exMsg", False))
            elif getPassengerDTOsResult.get('messages', False):
                print(getPassengerDTOsResult.get('messages', False))
            else:
                raise PassengerUserException(ticket.DTO_NOT_FOUND)

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
        return str(passengerTicketStr[set_type.replace(' ', '')])

    def getPassengerTicketStrListAndOldPassengerStr(self):
        """
        获取提交车次人内容格式
        passengerTicketStr	O,0,1,文贤平,1,43052419950223XXXX,15618715583,N_O,0,1,梁敏,1,43052719920118XXXX,,N
        oldPassengerStr	文贤平,1,43052719920118XXXX,1_梁敏,1,43052719920118XXXX,1_
        :return:
        """
        passengerTicketStrList = []
        oldPassengerStr = []
        user_info = self.sendGetPassengerDTOs()
        set_type = self.getPassengerTicketStr(self.set_type)
        if not user_info:
            raise PassengerUserException(ticket.DTO_NOT_IN_LIST)
        if len(user_info) is 1:
            passengerTicketStrList.append(
                '0,' + user_info[0]['passenger_type'] + "," + user_info[0][
                    "passenger_name"] + "," +
                user_info[0]['passenger_id_type_code'] + "," + user_info[0]['passenger_id_no'] + "," +
                user_info[0]['mobile_no'] + ',N')
            oldPassengerStr.append(
                user_info[0]['passenger_name'] + "," + user_info[0]['passenger_id_type_code'] + "," +
                user_info[0]['passenger_id_no'] + "," + user_info[0]['passenger_type'] + '_')
        else:
            for i in xrange(len(user_info)):
                passengerTicketStrList.append(
                    '0,' + user_info[i]['passenger_type'] + "," + user_info[i][
                        "passenger_name"] + "," + user_info[i]['passenger_id_type_code'] + "," + user_info[i][
                        'passenger_id_no'] + "," + user_info[i]['mobile_no'] + ',N_' + set_type)
                oldPassengerStr.append(
                    user_info[i]['passenger_name'] + "," + user_info[i]['passenger_id_type_code'] + "," +
                    user_info[i]['passenger_id_no'] + "," + user_info[i]['passenger_type'] + '_')
        return {
            "passengerTicketStrList": set_type + "," + ",".join(passengerTicketStrList),
            "oldPassengerStr": "".join(oldPassengerStr),
            "code": ticket.SUCCESS_CODE,
            "set_type": set_type,
            "status": True,
        }
