# -*- coding=utf-8 -*-
import json
import sys
import urllib
import urllib2

submitParams = [
            ('secretStr', 1), # 预订提交令牌
            ('train_date', 1), # 车票日期
            ('back_train_date', 1), # 返程日期，没有则为当前日期
            ('tour_flag', 1), # 旅行类型，单程dc,与返程fc
            ('purpose_codes', 1), # 标记是否为成人(ADULT)与学生(0X00)
            ('query_from_station_name', 1), # 发站名称，汉字
            ('query_to_station_name', 1)      # 到站名称，汉字
        ]

print urllib.unquote()