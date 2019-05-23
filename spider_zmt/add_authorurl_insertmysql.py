# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:李哥工作圈
@QQ:877129310
@VIP交流群:141342076
@version:V1.0
@var:
@note:

"""

import hashlib

import MySQLdb

from utils.connect_mysql import mysql_connect


def add_authorurl():
    conn, cur = mysql_connect()
    urls = ['https://c.m.163.com/news/sub/T1520070801955.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1481952723512.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1479750369422.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1490060095533.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1472177148070.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1545278947559.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1532164269177.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1540547524322.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1517807774338.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1496822604631.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1493519278174.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1465820709940.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1482287400125.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1537412261039.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1480519297631.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1478588558810.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1510813069613.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1525512880129.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1520070870427.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1534918073023.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1513061284127.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1536479960491.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1512041886007.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1469611763629.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1535687771706.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1522134476776.html?spss=newsapp',
            'https://c.m.163.com/news/sub/T1502677389148.html?spss=newsapp', ]
    for url in urls:
        md5 = hashlib.md5()
        md5.update(url)
        url_md5 = md5.hexdigest()
        print url, url_md5
        sql = "INSERT INTO author_url (url, url_md5, site_name) VALUES ('%s', '%s', '网易号')" % (url, url_md5)
        try:
            cur.execute(sql)
            conn.commit()
        except MySQLdb.Error, e:
            print (u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
    cur.close()
    conn.close()


if __name__ == '__main__':
    add_authorurl()
