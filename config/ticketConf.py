# -*- coding: utf8 -*-
__author__ = 'MR.wen'
import os
import yaml


def _get_yaml():
    """
    解析yaml
    :return: s  字典
    """
    opts, args = getopt.getopt(sys.argv[1:], 'f:')
    config_name = opts[0][1] if opts else 'ticket_config.yaml'
    path = os.path.join(os.path.dirname(__file__) + '/' + config_name)
    f = open(path)
    s = yaml.load(f)
    f.close()
    return s.decode() if isinstance(s, bytes) else s


if __name__ == '__main__':
    print(_get_yaml())
