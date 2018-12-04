# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:采集状态收集 扩展件
@note:收集采集状态信息及入库!

"""
from scrapy import signals
import datetime
import MySQLdb
from xbzxproject.utils.loadconfig import *


class StatsPoster(object):

    def __init__(self, crawler):
        self.crawler = crawler
        self.stats = crawler.stats
        # 链接数据库
        self.conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DATABASES, charset=u"utf8")
        self.cur = self.conn.cursor()
        self.COLstr = u''  # 列的字段
        self.ROWstr = u''  # 行字段
        self.ColumnStyle = u' VARCHAR(100)'

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.close_spider, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        self.stats.set_value('start_time', datetime.datetime.now())
        if spider.debug:
            self.enabled = False
            return
        else:
            self.enabled = True

    def close_spider(self, spider, reason):
        net_spider_id = api_netspider(spider.name_spider)['uuid']
        self.stats.set_value('finish_time', datetime.datetime.now(), spider=spider)
        self.stats.set_value('name_spider', spider.name_spider)
        self.stats.set_value('spider_jobid', spider.spider_jobid)
        self.stats.set_value("project_spider", PROJECT)
        self.stats.set_value("host_spider", HOST_SCRAPYD)
        self.stats.set_value("net_spider_id", net_spider_id)

        dic = self.stats.get_stats()
        sql_words = str(dic.keys()).replace(u"/", u"_").replace(u"[", u"").replace(u"]", u"").replace(u"'", u"").replace(u".", u"_")
        words_list = sql_words.split(",")
        sql_word = []
        for words in words_list:
            if len(words) >= 60:
                w = words.split("_")
                word = w[:2] + w[-2:]
                words = "_".join(word)
            sql_word.append(words)
        COLstr = ",".join(sql_word)
        for key in dic.keys():
            self.COLstr = self.COLstr + key.replace(u"/", u"_").replace(u".", u"_").replace(u"'", u"") + self.ColumnStyle + u','
            self.ROWstr = (self.ROWstr + u'"%s"' + u',') % (dic[key])
        # 判断表是否存在，存在执行try，不存在执行except新建表，再insert
        try:
            for key in dic.keys():
                # 判断该字段是否存在,不存在则创建该字段
                key = key.replace(u"/", u"_").replace(u".", u"_").replace(u"'", u"")
                self.cur.execute(u"describe net_spider_logs {};".format(key))
                result = len(self.cur.fetchall())
                if result == 0:
                    logging.info(key)
                    self.cur.execute(u"ALTER TABLE net_spider_logs ADD COLUMN {} varchar(100); ".format(key))
            self.cur.execute(
                u"INSERT INTO net_spider_logs (%s)VALUES (%s)" % (COLstr, self.ROWstr[:-1]))
        except MySQLdb.Error as e:
            self.cur.execute(
                u"INSERT INTO net_spider_logs (%s)VALUES (%s)" % (COLstr, self.ROWstr[:-1]))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    pass