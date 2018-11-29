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

import MySQLdb
import MySQLdb.cursors
import logging, json
from xbzxproject.settings import PATH
import requests
import ConfigParser

conf = ConfigParser.ConfigParser()
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
            print u"爬虫名:{}".format(name_spider)
            raise logging.error(u"爬虫名:{} 配置信息未找到!".format(name_spider))
    except MySQLdb.Error, e:
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
    # print loadMySQL("sohunews")
    # print api_netspider("thx")
    # print api_netspider("hzxw_net_cn")