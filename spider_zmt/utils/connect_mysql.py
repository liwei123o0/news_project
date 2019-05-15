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
    conn = MySQLdb.connect(host="rm-bp1i4s7mgs401rj2n.mysql.rds.aliyuncs.com", port=3306, user='acq_data',
                           passwd='MuF8+Vsq2j)^RfMr', db='acq_data',
                           charset=u"utf8")
    cur = conn.cursor()
    return conn, cur


def mysql_close():
    conn, cur = mysql_connect()
    cur.close()
    conn.close()
