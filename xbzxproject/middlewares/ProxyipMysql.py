# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:随机代理
@note:默认每请求30条随机更换代理

"""

import random
import base64
import MySQLdb

from xbzxproject.utils.loadconfig import *


class ProxyMiddleware(object):
    def __init__(self):
        self.idx = 0

    def random_proxy(self):
        self.conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DATABASES, charset=u"utf8")
        self.cur = self.conn.cursor()
        self.cur.execute(
            u"SELECT proxyip FROM net_proxy WHERE quality=0 ORDER BY insert_time DESC LIMIT %s;" % PROXY_COUT)
        self.proxies = self.cur.fetchall()
        self.cur.execute(
            u"SELECT proxyip FROM net_proxy WHERE quality = 1 AND insert_time >= NOW() -INTERVAL 2 MINUTE;")
        self.proxies_quality = self.cur.fetchall()
        self.cur.execute(
            u"SELECT proxyip FROM net_proxy WHERE quality=2 ORDER BY insert_time DESC LIMIT %s;" % PROXY_COUT)
        self.proxies_jw = self.cur.fetchall()
        if len(self.proxies) == 0:
            self.proxies = (([u"127.0.0.1:8080"], [u"127.0.0.1:8088"]))
        if len(self.proxies_quality) == 0:
            self.proxies_quality = (([u"127.0.0.1:8080"], [u"127.0.0.1:8088"]))
        if len(self.proxies_jw) == 0:
            self.proxies_jw = (([u"127.0.0.1:8080"], [u"127.0.0.1:8088"]))
        self.cur.close()
        self.conn.close()
        self.proxy_d = random.choice(self.proxies)
        self.proxy_g = random.choice(self.proxies_quality)
        self.proxy_jw = random.choice(self.proxies_jw)
        return self.proxy_d[0], self.proxy_g[0], self.proxy_jw[0]

    def process_request(self, request, spider):
        self.idx += 1
        try:
            if spider.proxy or spider.proxy_type == "1" or spider.proxy_type == "2" or spider.proxy_type == "3":
                if spider.proxy_type == "1":
                    proxy = self.random_proxy()[0]
                    request.meta[u'proxy'] = u"http://%s" % proxy
                elif spider.proxy_type == "2":
                    proxy = self.random_proxy()[1]
                    request.meta[u'proxy'] = u"http://%s" % proxy
                else:
                    proxy = self.random_proxy()[2]
                    request.meta[u'proxy'] = u"http://%s" % proxy
                    proxy_user_pass = u"te928m:te928m"
                    encoded_user_pass = base64.encodestring(proxy_user_pass)
                    request.headers[u'Proxy-Authorization'] = u'Basic ' + encoded_user_pass

            if self.idx >= RANDOM_NUMBER:
                self.idx = 0
                logging.info(u"累积请求数已达到%s次，准备更换代理..." % PROXY_COUT)
                if spider.proxy_type == "1":
                    proxy = self.random_proxy()[0]
                    request.meta[u'proxy'] = u"http://%s" % proxy
                elif spider.proxy_type == "2":
                    proxy = self.random_proxy()[1]
                    request.meta[u'proxy'] = u"http://%s" % proxy
                else:
                    proxy = self.random_proxy()[2]
                    request.meta[u'proxy'] = u"http://%s" % proxy
                    proxy_user_pass = u"te928m:te928m"
                    encoded_user_pass = base64.encodestring(proxy_user_pass)
                    request.headers[u'Proxy-Authorization'] = u'Basic ' + encoded_user_pass
        except:
            logging.error(u"代理异常,请检查代理IP!")

if __name__ == "__main__":
    pass