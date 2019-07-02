#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 新房楼盘的数据结构


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
