# -*- coding: utf-8 -*-
import hashlib
import random

from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule


class SohuZmtSpider(CrawlSpider):
    name = 'sohu_zmt'
    proxy = False
    debug = False
    download_delay = round(random.uniform(0.2, 1.5), 1)
    tablename = 'data_wemedia'
    allowed_domains = ['sohu.com']
    start_urls = []
    for i in xrange(1, 2000, 1):
        start_urls.append("http://mt.sohu.com/?p={}".format(i))

    rules = [
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='news-box clear news-box-txt']//h4/a")),
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
        l.add_xpath('title', "//h1//text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('pubtime', "//span[@id='news-time']/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('content', "//div[@class='text']/article//p[position()>1 and position()<last()]//text()",
                    MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('author', "//div[@id='user-info']/h4/a/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_value("site_name", u"搜狐号")
        yield l.load_item()
