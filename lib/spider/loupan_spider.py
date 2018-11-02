#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

import re
import math
import requests
from bs4 import BeautifulSoup
from lib.item.loupan import *
from lib.spider.base_spider import *
from lib.request.headers import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.city import get_city
from lib.utility.log import *


class LouPanBaseSpider(BaseSpider):
    def collect_city_loupan_data(self, city_name, fmt="csv"):
        """
        将指定城市的新房楼盘数据存储下来，默认存为csv文件
        :param city_name: 城市
        :param fmt: 保存文件格式
        :return: None
        """
        # csv_file = self.today_path + "/{0}.csv".format(city_name)
        csv_file = self.today_path + "/{0}_{1}.csv".format(city_name,self.date_string)
        with open(csv_file, "w", encoding='utf-8') as f:
            # 开始获得需要的板块数据
            loupans = self.get_loupan_info(city_name)
            self.total_num = len(loupans)
            if fmt == "csv":
                for loupan in loupans:
                    # f.write(self.date_string + "," + loupan.text() + "\n")
                    f.write(loupan.text() + "\n")
        print("Finish crawl: " + city_name + ", save data to : " + csv_file)

    @staticmethod
    def get_loupan_info(city_name):
        """
        爬取页面获取城市新房楼盘信息
        :param city_name: 城市
        :return: 新房楼盘信息列表
        """
        total_page = 1
        loupan_list = list()
        page = 'http://{0}.fang.{1}.com/loupan/'.format(city_name, SPIDER_NAME)
        print(page)
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*data-total-count="(\d+)".*', str(page_box))
            total_page = int(math.ceil(int(matches.group(1)) / 10))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(city_name))
            print(e)

        print(total_page)
        # 从第一页开始,一直遍历到最后一页
        headers = create_headers()
        for i in range(1, total_page + 1):
            page = 'http://{0}.fang.{1}.com/loupan/pg{2}'.format(city_name, SPIDER_NAME, i)
            print(page)
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elements = soup.find_all('li', class_="resblock-list")
            for house_elem in house_elements:
                price = house_elem.find('span', class_="number") # 单价
                total = house_elem.find('div', class_="second")  # 总价
                loupan = house_elem.find('a', class_='name') # 楼盘名称
                url = house_elem.find('a', class_="resblock-img-wrapper") # 网址
                tag = house_elem.find('div', class_="resblock-tag") # 标签

                if SPIDER_NAME == "lianjia":
                    restype = house_elem.find('span', class_="resblock-type") # 房屋类型
                    salestatus = house_elem.find('span', class_="sale-status") # 销售状态
                    location = house_elem.find('div', class_="resblock-location") # 地理位置
                    area = house_elem.find('div', class_="resblock-area") # 建筑面积


                    # 清洗数据
                    restype = restype.text.replace("\n", "")
                    salestatus = salestatus.text.replace("\n", "")
                else:
                    restypeAndsalestatus = house_elem.find('div', class_="resblock-name").text.split()
                    location = house_elem.find('a', class_="resblock-location") # 地理位置
                    area = house_elem.find('span', class_="area") # 建筑面积

                    # 清洗数据
                    restype = restypeAndsalestatus[2].replace("\n", "")
                    salestatus = restypeAndsalestatus[1].replace("\n", "")


                # 继续清理数据
                matches = re.search('.*href="(.+)".*', str(url))
                url = 'https://{0}.fang.{1}.com'.format(city_name, SPIDER_NAME)+ matches.group(1).split( )[0].replace("\"",'')

                tag = tag.text.replace("\n", " ")

                location = location.text.strip().replace("\n", "").replace(" ", "") # replace(" ", "") 去空格
                location = location.split('/')
                xingzhengqu = location[0]
                region = location[1]
                street = location[2].replace(",",' ')
                try:
                    area = area.text.replace("\n", "").replace(u'建面', '')
                except Exception as e:
                    area = '暂无'

                try:
                    price = price.text.strip() # 移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
                except Exception as e:
                    price = '0'

                loupan = loupan.text.replace("\n", "") # str.replace(old, new[, max])

                try:
                    total = total.text.strip().replace(u'总价', '')
                    total = total.replace(u'/套起', '')
                except Exception as e:
                    total = '0'

                print("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}".format(
                    xingzhengqu,region,street,loupan, price,area,total,restype,salestatus,tag,url))

                # 作为对象保存
                loupan = LouPan(xingzhengqu,region,street,loupan, price,area,total,restype,salestatus,tag,url)
                loupan_list.append(loupan)
        return loupan_list

    def start(self):
        city = get_city()
        print('Today date is: %s' % self.date_string)
        # self.today_path = create_date_path("{0}/loupan".format(SPIDER_NAME), city, self.date_string)
        self.today_path = create_city_path("{0}/loupan".format(SPIDER_NAME), city)

        t1 = time.time()  # 开始计时
        self.collect_city_loupan_data(city)
        t2 = time.time()  # 计时结束，统计结果

        print("Total crawl {0} loupan.".format(self.total_num))
        print("Total cost {0} second ".format(t2 - t1))


if __name__ == '__main__':
    pass
