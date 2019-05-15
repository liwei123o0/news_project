# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BasespiderItem(Item):
    # define the fields for your item here like:
    pass


class SougouSpiderItem(Item):
    url = Field()
    title = Field()
    pubtime = Field()
    content = Field()
    site_name = Field()
    author = Field()
    url_md5 = Field()
