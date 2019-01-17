# -*- coding: utf8 -*-
from config import configCommon

__author__ = 'MR.wen'
import os
import yaml


def _get_yaml():
    """
    解析yaml
    :return: s  字典
    """
    path = os.path.join(os.path.dirname(__file__) + '/ticket_config.yaml')
    try:  # 兼容2和3版本
        with open(path, encoding="utf-8") as f:
            s = yaml.load(f)
    except Exception:
        with open(path) as f:
            s = yaml.load(f)
    return s.decode() if isinstance(s, bytes) else s


if __name__ == '__main__':
    print(_get_yaml())