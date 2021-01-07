# -*- coding: utf-8 -*-
import os

path_1 = "/proc/1/cgroup"
path_self = "/proc/self/cgroup"


def verify_docker():
    """
    docker 环境下返回True
    :return:
    """
    if os.path.isfile(path_1):
        with open(path_1, "r") as f:
            for line in f.readlines():
                if "docker" in line:
                    return True
                else:
                    continue
    elif os.path.isfile(path_self):
        with open(path_self, "r") as f:
            for line in f.readlines():
                if "docker" in line:
                    return True
                else:
                    continue
    else:
        return False
