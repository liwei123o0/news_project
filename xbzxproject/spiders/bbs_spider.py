# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:新闻类通用模版
@note:新闻通用模版采集~必须字段: spider_jobid name_spider

"""
import json
import logging
import re
import string
from datetime import datetime

from scrapy import Item, Field
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule,Spider

from xbzxproject.utils.loadconfig import loadMySQL, api_netspider
import requests
from lxml import etree
import scrapy

class BBsSpider(Spider):
    name = "bbs"
    table_name = "data_bbs"

    # 加载规则配置文件
    # 获取额外参数
    def __init__(self, spider_jobid=None, name_spider=None, debug=False, *args, **kwargs):
        self.spider_jobid = spider_jobid
        self.name_spider = name_spider
        self.debug = debug
        self.conf = api_netspider(name_spider)
        self.loadconf(self.name_spider, self.spider_jobid, self.conf)
        self.keys = loadMySQL(self.name_spider)['fields'].keys()
        super(BBsSpider, self).__init__(*args, **kwargs)

    # 规则配置
    def loadconf(self, name_spider, spider_jobid, conf):
        if name_spider == None or spider_jobid == None:
            raise logging.error(u"name_spider或spider_jobid 不能为空!!!")
        domains = conf.get("allowed_domains", "").split(",")
        self.allowed_domains = domains
        if int(conf.get("proxy_type", 0)) == 0:
            self.proxy = False
        else:
            self.proxy = True
        self.proxy_type = conf.get("proxy_type", "0")
        urls_start = conf.get("start_urls", "").replace("\r", "").replace("\n", "").split(',')
        self.start_urls = []
        for uri in urls_start:
            TODAY = "".join(re.findall(r"\{TODAY}", uri))
            YEAR = "".join(re.findall(r"\{YEAR}", uri))
            MONTH = "".join(re.findall(r"\{MONTH}|\{IMONTH}", uri))
            DAY = "".join(re.findall(r"\{DAY}|\{IDAY}", uri))
            if string.find(uri, TODAY) > 0:
                uri = uri.replace("{TODAY}", datetime.now().strftime("%Y%m%d"))
            if string.find(uri, YEAR) > 0:
                uri = uri.replace("{YEAR}", str(datetime.now().year))
            if string.find(uri, MONTH) > 0:
                if MONTH == "{MONTH}":
                    uri = uri.replace("{MONTH}", str(datetime.now().month))
                else:
                    if datetime.now().month < 10:
                        month = str(datetime.now().month)[1:]
                        uri = uri.replace("{IMONTH}", month)
                    else:
                        uri = uri.replace("{IMONTH}", str(datetime.now().month))
            if string.find(uri, DAY) > 0:
                if DAY == "{DAY}":
                    uri = uri.replace("{DAY}", str(datetime.now().day))
                else:
                    if datetime.now().day < 10:
                        day = str(datetime.now().day)[1:]
                        uri = uri.replace("{IDAY}", day)
                    else:
                        uri = uri.replace("{IDAY}", str(datetime.now().day))
            self.start_urls.append(uri)

    def start_requests(self):
        item = Item()
        for url in self.start_urls:
            url_slit = url.split(":")
            site_name = url_slit[0]
            url = ":".join(url_slit[1:-1])
            item.fields["site_name"] = Field()
            item['site_name'] = site_name
            item.fields["source_url"] = Field()
            item['source_url'] = url_slit[-1]
            yield scrapy.Request(url=url, meta={"item": item}, dont_filter=True,callback=self.parse_url)

    def parse_url(self, response):
        item = response.meta['item']
        rules = json.loads(self.conf.get("rules"))
        if rules == "":
            raise logging.error(u"规则解析未得到!!!")
        links = LinkExtractor(restrict_xpaths=u"%s" % rules['rules_listxpath'])
        use_iframe = self.conf.get("use_iframe", "0")
        if use_iframe == "0":
            for url in links.extract_links(response):
                yield scrapy.Request(url.url, self.parse_item, meta={"item": item}, dont_filter=True)
        else:
            for uri in links.extract_links(response):
                html = requests.get(uri.url).content
                dom = etree.HTML(html)
                url = u"".join(dom.xpath("//iframe/@src"))
                yield scrapy.Request(url, self.parse_item, meta={"item": item}, dont_filter=True)

    # 内容解析
    def parse_item(self, response):
        item = response.meta['item']
        fields = json.loads(self.conf.get("fields"))
        l = ItemLoader(item, response)
        item.fields["url"] = Field()
        item.fields["spider_jobid"] = Field()
        l.add_value("url", response.url)
        l.add_value("spider_jobid", self.spider_jobid)

        # 加载动态库字段建立Field,xpath规则 (方法一)
        for k in self.keys:
            if fields.get("fields", "") == "":
                raise logging.error(u"内容解析未得到!!!")
            if fields.get("fields").get(
                    k) != None and k != "re_author" and k != "re_content" and k != "re_pubtime" and k != "loop_content":
                item.fields[k] = Field()
                if fields.get("fields").get(k).keys()[0] == "xpath":
                    l.add_xpath(k, u"{}".format(fields.get("fields").get(k).get("xpath")),
                                MapCompose(unicode.strip))
                elif fields.get("fields").get(k).keys()[0] == "value":
                    if fields.get("fields").get(k).get("value") == u"{TODAY}":
                        l.add_value(k, u"{}".format(datetime.now()))
                    l.add_value(k, u"{}".format(fields.get("fields").get(k).get("value")))
        return l.load_item()


if __name__ == "__main__":
    pass
