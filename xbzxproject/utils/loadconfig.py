# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:加载数据库配置信息
@note:加载数据库爬虫配置信息等

"""

import ConfigParser
import json
import logging

import MySQLdb
import MySQLdb.cursors
import requests

from xbzxproject.settings import PATH

conf = ConfigParser.RawConfigParser()
conf.read(PATH)

# mysql
HOST = conf.get("mysql", "host")
PORT = int(conf.get("mysql", "port"))
USER = conf.get("mysql", "user")
PASSWD = conf.get("mysql", "passwd")
DATABASES = conf.get("mysql", "databases")

# proxy
PROXY_COUT = conf.get("proxy", "proxy_cout")
RANDOM_NUMBER = conf.get("proxy", "random_number")
PROXY_USER_NAME = conf.get("proxy", "username")
PROXY_PASSWD = conf.get("proxy", "passwd")

# scrapy
PROJECT = conf.get("scrapy", "project")

# scrapyd
HOST_SCRAPYD = conf.get("scrapyd", "host")
PORT_SCRAPYD = conf.get("scrapyd", "port")

# api
API_PROT = conf.get("api", "port")
API_NAMESPIDER = conf.get("api", "namespider")
API_all = conf.get("api", "all")


# 加载规则配置文件
def fileconfig(name_spider):
    try:
        conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DATABASES, charset=u"utf8",
                               cursorclass=MySQLdb.cursors.DictCursor)
        cur = conn.cursor()
        cur.execute(u"SELECT * FROM net_spider WHERE spider_name='{}'".format(name_spider))
        keywords = cur.fetchone()
        if keywords == None:
            print(u"爬虫名:{}").format(name_spider)
            raise logging.error(u"爬虫名:{} 配置信息未找到!".format(name_spider))
    except MySQLdb.Error as e:
        cur.close()
        conn.close()
        raise logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))

    cur.close()
    conn.close()
    return keywords

# API读取爬虫配置信息
def api_netspider(name_spider):
    url = API_NAMESPIDER.format(prot=API_PROT, name_spider=name_spider)
    datas = json.loads(requests.get(url).content)
    try:
        return datas['data']["datas"][0]
    except:
        raise logging.error(u"爬虫名:{} 配置信息未找到!".format(name_spider))
        # return {u'spider_name': u'ixian1', u'update_date': u'2019-01-02 11:40:31', u'area_id': u'\u897f\u5b89',
        #         u'start_urls': u'https://www.ixian.cn/forum-1088-1.html', u'user_id': u'39',
        #         u'allowed_domains': u'ixian.cn',
        #         u'rules': u'{"rules_pagexpath":"","rules_listxpath":"//div[@class=\'busforumlist_item_title\']/a[1]"}',
        #         u'fields': u'{"fields":{"loop_content":{"xpath":"//div[@class=\'mobanbus_reply\']"},"title":{"xpath":"//h2//text()"},"content":{"xpath":"(//td[@class=\'t_f\'])[1]/text()"},"pubtime":{"xpath":"//div[@class=\'item_b\']/span[2]/text()"},"author":{"xpath":"//div[@class=\'bus_avatarnamne\']/a/text()"},"re_content":{"xpath":".//td[@class=\'t_f\']//text()"},"re_pubtime":{"xpath":".//em//text()"},"re_author":{"xpath":".//span[@class=\'pl5 pr5\']//text()"}}}',
        #         u'latest_count': u'0', u'proxy_type': u'0', u'proxy': u'False',
        #         u'latest_insert_time': u'2018-01-01 00:00:00', u'status': u'0', u'spider_type': u'bbs',
        #         u'chinesename': u'\u8363\u8000\u897f\u5b89', u'latest_pub_time': u'2018-01-01 00:00:00',
        #         u'create_date': u'2018-12-25 11:39:44', u'last_user_id': u'39', u'id': u'1206', u'has_latest_data': u'0',
        #         u'uuid': u'ac5cae79ea13410c90dc8612795bcb70'}



# 读取自动建库字段
def loadMySQL(spider_name):
    return json.loads(api_netspider(spider_name)['fields'])

# 获取关键字
def loadkeywords():
    keywords = []
    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DATABASES, charset="utf8")
    cur = conn.cursor()
    cur.execute(u"SELECT keyword FROM  net_spider_keyword;")
    word = cur.fetchall()
    for keyword in word:
        keywords.append("".join(keyword))
    return keywords


if __name__ == "__main__":
    pass
