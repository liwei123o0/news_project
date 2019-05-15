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

import logging
import random

import MySQLdb
import requests
from basespider.utils.loadconfig import loadscrapyconf


class ProxyMiddleware(object):
    def __init__(self):
        self.idx = 0
        self.conf = loadscrapyconf()[u'mysql']

    def random_proxy(self):
        self.conn = MySQLdb.connect(host=self.conf.get(u"host", u"localhost"),
                                    port=self.conf.get(u"port", 3306),
                                    user=self.conf.get(u"user", u"root"),
                                    passwd=self.conf.get(u"passwd", u"root"),
                                    db=self.conf.get(u"databases"), charset=u"utf8")
        self.cur = self.conn.cursor()
        self.cur.execute(u"SELECT proxyip FROM net_proxy WHERE quality=0 ORDER BY insert_time DESC LIMIT 20;")
        self.proxies = self.cur.fetchall()
        self.cur.execute(
            u"SELECT proxyip FROM net_proxy WHERE quality = 1 AND insert_time >= NOW() -INTERVAL 2 MINUTE;")
        self.proxies_quality = self.cur.fetchall()
        if len(self.proxies) == 0:
            self.proxies = (([u"127.0.0.1:8080"], [u"127.0.0.1:8088"]))
        if len(self.proxies_quality) == 0:
            self.proxies_quality = (([u"127.0.0.1:8080"], [u"127.0.0.1:8088"]))
        self.cur.close()
        self.conn.close()
        self.proxy_g = random.choice(self.proxies_quality)
        self.proxy_d = random.choice(self.proxies)
        return self.proxy_g[0], self.proxy_d[0]

    def requets_url(self):
        url = "http://dynamic.goubanjia.com/dynamic/get/a2d5afdd5e9514c96b73c5fbcff17a43.html?sep=3"
        ip = requests.get(url).text
        ip = ip.strip()
        return ip

    def process_request(self, request, spider):
        self.idx += 1
        try:
            if spider.proxy:
                if hasattr(spider, u"quality"):
                    if spider.quality == 1:
                        proxy = self.requets_url()
                        logging.info(u"高质量代理IP:{}下载页面...".format(proxy))
                        request.meta[u'proxy'] = u"http://%s" % proxy
                    else:
                        proxy = self.random_proxy()[1]
                        logging.info(u"低质量代理IP:{}下载页面...".format(proxy))
                        request.meta[u'proxy'] = u"http://%s" % proxy
                else:
                    proxy = self.random_proxy()[1]
                    logging.info(u"低质量代理IP:{}下载页面...".format(proxy))
                    request.meta[u'proxy'] = u"http://%s" % proxy
                if self.idx >= 10:
                    self.idx = 0
                    logging.info(u"累积请求数已达到10次，准备更换代理...")
                    if hasattr(spider, u"quality"):
                        if spider.quality == 1:
                            proxy = self.requets_url()
                            logging.info(u"更换高质量IP：%s..." % proxy)
                            request.meta[u'proxy'] = u"http://%s" % proxy
                        else:
                            proxy = self.random_proxy()[1]
                            logging.info(u"更换低质量IP：%s..." % proxy)
                            request.meta[u'proxy'] = u"http://%s" % proxy
        except:
            logging.error(u"代理异常,请检查代理IP!")


if __name__ == "__main__":
    pass
