# -*- coding: utf-8 -*-
import hashlib
import random

from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule


class SohuZmtSpider(CrawlSpider):
    name = 'qie_zmt'
    proxy = False
    debug = False
    tablename = 'data_wemedia'
    allowed_domains = ['vyi.cc', 'qq.com', 'kuaibao.qq.com']
    start_urls = ["http://www.vyi.cc/kuaibao/index.php"]
    download_delay = download_delay = round(random.uniform(1, 1.5), 1)

    rules = [
        Rule(LinkExtractor(restrict_xpaths=(u"//a[contains(.,'点击查看')]")),
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
        l.add_xpath('title', "//p[@class='title']/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('pubtime', "//span[@class='time']/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('content', "//div[@class='content-box']//p/text()", MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_xpath('author', "//span[@class='author']/text() | //div[@class='nickname']/text()",
                    MapCompose(unicode.lstrip, unicode.rstrip))
        l.add_value("site_name", u"企鹅号")
        yield l.load_item()
