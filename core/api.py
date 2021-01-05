# -*- coding: utf-8 -*-
# @Author: Admin
# @Date:   2020-09-12 15:49:35
# @Last Modified by:   Jingyuexing
# @Last Modified time: 2020-11-14 03:04:23
import json

HEAD = {
    "Accept": "*/*",
    "Accept-Encoding": "",
    "Accept-Language": "",
    "Cache-Control:": "",
    "Connection": "",
    "DNT": 1,
    "Host": "kyfw.12306.cn",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "X-Requested-With": "XMLHttpRequest"
}

API = None


with open("data/API.json", "r") as file:
    API = json.load(file)
    file.close()


def request(url="", method="get", param={}, head=HEAD):
    import urllib3
    http = urllib3.PoolManager()
    req = http.request(method=method, url=url, fields=param, headers=head)
    if (req.status == 200):
        return json.loads(req.data.decode("utf-8"), encoding='utf-8')


def getPrice(config):
    """查询列车的车票价格
    ```py
    getPrice(
    {
        "id": "",  //列车的ID
        "startID":"", //起始站ID
        "endID":"", //到达站ID
        "date":"", //日期
        "type":"" //座位的类别 是软卧还是硬座
    }
    )
    ```
    Arguments:
        config {dict} -- 需要的参数

    Returns:
        {JSON} -- 从服务器响应的数据
    """
    url = API[1]['url']
    trainID = config['id']
    start = config['startID']
    end = config['endID']
    date = config['date']
    seat = config['type']
    return request(url=url, param={
        "train_no": trainID,
        "from_station_no": start,
        "to_station_no": end,
        "seat_types": seat,
        "train_date": date
    })


def getSchedules(config):
    """查询列车过站信息

    [description]

    Arguments:
        config {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    url = API[2]['url']
    start = config['start']  # 起始站
    end = config['end']  # 到达站
    date = config['date']   # 出行日期
    trainID = config['id']  # 列车id 例如  58000G16090B
    return request(url=url, param={
        "train_no": trainID,
        "from_station_telecode": start,
        "to_station_telecode": end,
        "depart_date": date
    })


def getTrain(config, type="ADULT"):
    url = API[0]['url']
    start = config['start']  # 出发站
    end = config['end']  # 到达站
    date = config['date']  # 出发日期
    return request(url=url, param={
        "leftTicketDTO.train_date": date,
        "leftTicketDTO.from_station": start,
        "leftTicketDTO.to_station": end,
        "purpose_codes": type  # 默认为成人
    })


def parserResult(data):
    """解析返回的数据

    [description]

    Arguments:
        data {list} -- 返回的JSON数组数据

    Returns:
        list -- 解析后的数据
    """
    positionsName = data['map']
    dataResult = data['result']
    data = {
        "secretStr": '',
        "buttonTextInfo": "",
        "train_no": None,
        "station_train_code": None,
        "start_station_telecode": None,
        "end_station_telecode": None,
        "from_station_telecode": None,
        "to_station_telecode": None,
        "start_time": None,
        "arrive_time": None,
        "lishi": None,
        "canWebBuy": None,
        "yp_info": None,
        "start_train_date": None,
        "train_seat_feature": None,
        "location_code": None,
        "from_station_no": None,
        "to_station_no": None,
        "is_support_card": None,
        "controlled_train_flag": None,
        "gg_num": None,
        "gr_num": None,
        "qt_num": None,
        "softBed": None,
        "softSeat": None,
        "specialSeat": None,
        "notSeat": None,
        "yb_num": None,
        "hardbed": None,
        "hardSeat": None,
        "secondSeat": None,
        "firstSeat": None,
        "businessSeat": None,
        "yp_ex": None,
        "seat_types": None,
        "exchange_train_flag": None,
        "houbu_train_flag": None,
        "houbu_seat_limit": None,
        "from_station_name": None,
        "to_station_name": None
    }
    totalData = []
    for l in dataResult:
        nowData = l.split("|")
        data['secretStr'] = nowData[0]
        data['buttonTextInfo'] = nowData[1]
        data['train_no'] = nowData[2]
        data['station_train_code'] = nowData[3]
        data['start_station_telecode'] = nowData[4]
        data['end_station_telecode'] = nowData[5]
        data['from_station_telecode'] = nowData[6]
        data['to_station_telecode'] = nowData[7]
        data['start_time'] = nowData[8]
        data['arrive_time'] = nowData[9]
        data['lishi'] = nowData[10]  # 历时
        data['canWebBuy'] = nowData[11]
        data['yp_info'] = nowData[12]
        data['start_train_date'] = nowData[13]
        data['train_seat_feature'] = nowData[14]
        data['location_code'] = nowData[15]
        data['from_station_no'] = nowData[16]
        data['to_station_no'] = nowData[17]
        data['is_support_card'] = nowData[18]
        data['controlled_train_flag'] = nowData[19]
        data['gg_num'] = nowData[20]
        data['specialBed'] = nowData[21]
        data["qt_num"] = nowData[22]
        data['softBed'] = nowData[23]  # 软卧
        data['softSeat'] = nowData[24]  # 软座
        data['specialSeat'] = nowData[25]  # 特等座
        data['notSeat'] = nowData[26]  # 无座
        data['yb_num'] = nowData[27]
        data['hardbed'] = nowData[28]  # 硬卧/二等卧
        data['hardSeat'] = nowData[29]  # 硬座
        data['ze_num'] = nowData[30]
        data['firstSeat'] = nowData[31]  # 一等座
        data["businessSeat"] = nowData[32]  # 商务座
        data["srrb_num"] = nowData[32]
        data["yp_ex"] = nowData[32]
        data["seat_types"] = nowData[32]
        data["exchange_train_flag"] = nowData[32]
        data['houbu_train_flag'] = nowData[37]
        data['from_station_name'] = positionsName[nowData[6]]
        data['to_station_name'] = positionsName[nowData[7]]
        totalData.append(data)
    return totalData
