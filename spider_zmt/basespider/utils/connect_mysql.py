# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:
@var:
@note:

"""
import MySQLdb


def mysql_connect():
    conn = MySQLdb.connect(host="192.168.10.173", port=3306, user='root', passwd='root', db='DataCollectV1',
                           charset=u"utf8")
    cur = conn.cursor()
    return conn, cur


def mysql_close():
    conn, cur = mysql_connect()
    cur.close()
    conn.close()
