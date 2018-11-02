#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 新房楼盘的数据结构

import sys
from lib.utility.version import PYTHON_3
if not PYTHON_3:   # 如果小于Python3
    reload(sys)
    sys.setdefaultencoding("utf-8")


class LouPan(object):
    def __init__(self,xingzhengqu,region,street,loupan, price,area,total,restype,salestatus,tag,url):
        # self.district = district
        # self.area = area
        self.xingzhengqu = xingzhengqu
        self.region = region
        self.street = street
        self.loupan = loupan
        # self.address = address
        # self.size = size
        self.price = price
        self.area = area
        self.total = total
        self.restype = restype
        self.salestatus = salestatus
        self.tag = tag
        self.url = url

    def text(self):
        return self.xingzhengqu + "," + \
                self.region + "," + \
                self.street + "," + \
                self.loupan + "," + \
                self.price + "," + \
                self.area + "," + \
                self.total + "," + \
                self.restype + "," + \
                self.salestatus + "," + \
                self.tag + "," + \
                self.url
