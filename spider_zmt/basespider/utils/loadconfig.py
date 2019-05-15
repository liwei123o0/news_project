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

import logging
import platform
import sys

import MySQLdb
import MySQLdb.cursors

reload(sys)
if platform.system().lower() in "windows":
    sys.setdefaultencoding('gb18030')
else:
    # platform.system().lower() in "linux"
    sys.setdefaultencoding('utf-8')


# 获取所有企业名称
def loadname():
    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8")
    cur = conn.cursor()
    cur.execute("SELECT name,ztsbm FROM yqapp.qyname")
    keywords = cur.fetchall()
    cur.close()
    conn.close()
    return keywords


# 获取单个企业名称
def loadnameone():
    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8")
    cur = conn.cursor()
    cur.execute(u"SELECT name  FROM yqapp.qyname WHERE cout=0 LIMIT 1")
    keyword = cur.fetchall()[0][0]
    cur.execute(u"UPDATE yqapp.qyname set cout= cout+1 WHERE name='%s'" % keyword)
    conn.commit()
    cur.close()
    conn.close()
    return keyword


# 加载规则配置文件
def fileconfig(name_spider):
    conf = loadscrapyconf()['mysql']
    try:
        conn = MySQLdb.connect(host=conf.get("host", "localhost"), port=conf.get("port", 3306),
                               user=conf.get("user", "root"), passwd=conf.get("passwd", "root"),
                               db=conf.get("databases"), charset=u"utf8", cursorclass=MySQLdb.cursors.DictCursor)
        cur = conn.cursor()
        cur.execute(u"SELECT * FROM net_spider WHERE spider_name='{}'".format(name_spider))
        try:
            keywords = cur.fetchall()[0]
        except:
            print u"爬虫名:{}".format(name_spider)
            raise logging.error(u"爬虫名:{} 配置信息未找到!".format(name_spider))
    except MySQLdb.Error, e:
        cur.close()
        conn.close()
        raise logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))

    cur.close()
    conn.close()
    return keywords


def loaditems():
    conn = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="root", charset="utf8")
    cur = conn.cursor()
    cur.execute(
        u"select COLUMN_NAME from INFORMATION_SCHEMA.Columns where table_name='xingzheng' and table_schema='scrapy'")
    key = cur.fetchall()
    cur.close()
    conn.close()
    return key


# 读取自动建库字段
def loadMySQL(spider_type):
    conf = loadscrapyconf()['mysql']
    conn = MySQLdb.connect(host=conf.get("host", "localhost"), port=conf.get("port", 3306),
                           user=conf.get("user", "root"), passwd=conf.get("passwd", "root"),
                           db=conf.get("databases"), charset="utf8")
    cur = conn.cursor()
    cur.execute(u"SELECT id FROM net_gendbtable WHERE name = '{}'".format(spider_type))
    try:
        key = cur.fetchall()[0][0]
    except:
        raise logging.error(u"spider_type:{} 未找到,请检查爬虫类型!".format(spider_type))
    try:
        cur.execute(
            u"SELECT name FROM net_gendbtable_column WHERE gen_gendbtable_id = '{}'".format(key))
    except MySQLdb.Error, e:
        raise logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
    key = cur.fetchall()
    cur.close()
    conn.close()
    return key


# 加载初始化配置
def loadscrapyconf():
    from basespider.settings import BASECONFIG
    return BASECONFIG


def MysqlUrl(type):
    conf = loadscrapyconf()['mysql']
    conn = MySQLdb.connect(host=conf.get("host", "localhost"), port=conf.get("port", 3306),
                           user=conf.get("user", "root"), passwd=conf.get("passwd", "root"),
                           db=conf.get("databases"), charset=u"utf8")
    cur = conn.cursor()
    cur.execute("SELECT url FROM sys_area WHERE type={} and url !='';".format(type))
    urls = cur.fetchall()
    cur.close()
    conn.close()
    return urls

# if __name__ == "__main__":
# urls = MysqlUrl(4)
