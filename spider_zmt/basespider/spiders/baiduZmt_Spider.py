# -*- coding: utf-8 -*-
# ! /usr/bin/env python
import hashlib
import random

from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule


class BaiduZmtSpider(CrawlSpider):
    name = 'baidu_zmt'
    proxy = False
    debug = False
    tablename = 'data_wemedia'
    allowed_domains = ['vyi.cc', 'quwenge.com']
    start_urls = ["http://www.vyi.cc/baidu/index.php"]
    download_delay = round(random.uniform(1, 1.5), 1)
    rules = [
        Rule(LinkExtractor(restrict_xpaths=(u"//a[contains(.,'进入百家')]")),
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
        url = url.replace("http://rym.quwenge.com/baidu_tiaozhuan.php?url=", "")
        md5 = hashlib.md5()
        l.add_value(u'url', url)
        md5.update(url)
        url_md5 = md5.hexdigest()
        l.add_value(u'url_md5', url_md5)
        l.add_xpath('title', "//h1/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('pubtime', "//span[@class='read']/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('content', "//div[@id='content']//text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('author', "//div[@class='name']/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_value("site_name", u"百家号")
        yield l.load_item()
