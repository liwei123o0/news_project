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

from scrapy import Item, Field
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.selector import Selector
from scrapy.spiders import Spider

from xbzxproject.utils.loadconfig import loadMySQL, fileconfig, loadkeywords
# from urllib.parse import urljoin
# python2.7 依赖库
from urlparse import urljoin


# 站内搜索
class SearchSpider(Spider):
    name = "search"

    # 加载规则配置文件
    # 获取额外参数
    def __init__(self, spider_jobid=None, name_spider=None, debug=False, *args, **kwargs):
        self.spider_jobid = spider_jobid
        self.name_spider = name_spider
        self.debug = debug
        self.conf = fileconfig(name_spider)
        self.loadconf(name_spider, spider_jobid)
        super(SearchSpider, self).__init__(*args, **kwargs)

    # 传递搜索关键词及搜索连接
    def start_requests(self):
        if self.conf.get("keywords", "") == "":
            keywords = loadkeywords()
        else:
            keywords = self.conf.get("keywords").split(",")
        for word in keywords:
            if type(word) == tuple:
                word = " ".join(word)
            url = self.conf.get("start_urls", "").format(word=word)
            yield Request(url, callback=self.loadconf(self.name_spider, self.spider_jobid), meta={'word': word})

    # 规则配置
    def loadconf(self, name_spider, spider_jobid):

        if name_spider == None or spider_jobid == None:
            raise logging.error(u"name_spider或spider_jobid 不能为空!!!")
        self.allowed_domains = [self.conf.get("allowed_domains", "")]

        if self.conf.get("proxy").lower() in "false":
            self.proxy = False
        else:
            self.proxy = True

        rules = json.loads(self.conf.get("rules"))
        if rules.get("rules", "") == "":
            raise logging.error(u"规则解析未得到!!!")

    def parse(self, response):
        word = response.meta['word']
        sel = Selector(response)
        rules = json.loads(self.conf.get("rules"))
        loops = sel.xpath(rules.get("rules").get("rules_listxpath", ""))
        for loop in loops:
            yield Request(urljoin(response.url, "".join(loop.xpath("./@href").extract())), callback=self.parse_item,
                          meta={"word": word})

    # 内容解析
    def parse_item(self, response):
        item = Item()
        word = response.meta['word']
        fields = json.loads(self.conf.get("fields"))
        l = ItemLoader(item, response)
        if fields.get("fields", "") == "":
            logging.error(u"内容解析未得到!!!")
            return l.load_item()
        item.fields["url"] = Field()
        item.fields["spider_jobid"] = Field()
        l.add_value("url", response.url)
        l.add_value("spider_jobid", self.spider_jobid)
        item.fields['word'] = Field()
        l.add_value('word', word)
        # 加载动态库字段建立Field,xpath规则 (方法一)
        for k in loadMySQL(self.name_spider)['fields'].keys():
            if fields.get("fields", "") == "":
                logging.error(u"内容解析未得到!!!")
                return l.load_item()
            if fields.get("fields").get(k) != None:
                item.fields[k] = Field()
                if fields.get("fields").get(k).keys()[0] == "xpath":
                    l.add_xpath(k, u"{}".format(fields.get("fields").get(k).get("xpath")),
                                MapCompose(unicode.strip))
                elif fields.get("fields").get(k).keys()[0] == "value":
                    l.add_value(k, u"{}".format(fields.get("fields").get(k).get("value")))
        return l.load_item()

