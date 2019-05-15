# -*- coding: utf-8 -*-
# ! /usr/bin/env python
import hashlib
import random

from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule


class SohuZmtSpider(CrawlSpider):
    name = '163_zmt'
    proxy = False
    debug = False
    tablename = 'data_wemedia'
    allowed_domains = ['163.com']
    start_urls = ["http://dy.163.com/v2/media/medialist/C1378977951794-1.html"]
    download_delay = round(random.uniform(0.2, 1.0), 1)
    rules = [
        Rule(
            LinkExtractor(restrict_xpaths=(u"//ul[@class='dy_list']//li/a | //p[@class='award-page pageList']/a")),
            follow=True, ),
        Rule(
            LinkExtractor(restrict_xpaths=(u"//div[@class='des']/h3/a")),
            callback='parse_item', )
    ]

    def parse_item(self, response):
        item = Item()
        item.fields['url'] = Field()
        item.fields['url_md5'] = Field()
        item.fields['title'] = Field()
        item.fields['pubtime'] = Field()
        item.fields['content'] = Field()
        item.fields['author'] = Field()
        item.fields['site_name'] = Field()
        l = ItemLoader(item=item, response=response)
        url = response.url
        md5 = hashlib.md5()
        l.add_value(u'url', url)
        md5.update(url)
        url_md5 = md5.hexdigest()
        l.add_value(u'url_md5', url_md5)
        l.add_xpath('title', "//h2/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('pubtime', "//p[@class='time']/span[1]/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('content', "//div[@class='content']//text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('author', "//p[@class='time']/span[last()]/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_value("site_name", u"网易号")
        yield l.load_item()
