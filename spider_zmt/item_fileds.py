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

from connect_mysql import mysql_connect, mysql_close
from date_parse import parse_date


def item_fileds(item, tablename, debug):
    fields = []
    values = []
    conn, cur = mysql_connect()
    if debug:
        for k, v in item.iteritems():
            if k == "pubtime":
                v = parse_date(v)

            print u"{:>13.13}:{}".format(k, v)
    else:
        for k, v in item.iteritems():
            if k == "pubtime":
                v = parse_date(v)
            fields.append(k)
            values.append(v)
        try:
            # 根据 item 字段插入数据
            cur.execute(
                u"INSERT INTO {}({}) VALUES({});".format(tablename,
                                                         u",".join(fields), u','.join([u'%s'] * len(fields))),
                values)
            conn.commit()
            print (u"数据插入成功!")
        except MySQLdb.Error, e:
            print (u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
    mysql_close()
