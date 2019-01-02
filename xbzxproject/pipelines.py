# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""

@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:V1.0
@var:采集数据处理
@note:爬虫采集数据加工、处理、入库

"""

import hashlib
import re
import sys

import MySQLdb

from xbzxproject.utils import date_parse
from xbzxproject.utils.loadconfig import *

reload(sys)
sys.setdefaultencoding("utf8")


# mysql入库Pipeline
class XbzxprojectPipeline(object):
    # 开启爬虫初始化工作
    def open_spider(self, spider):
        self.cout = 1
        self.conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DATABASES, charset=u"utf8")
        self.cur = self.conn.cursor()
        logging.info("debug:%s" % spider.debug)
        self.net_spider_id = api_netspider(spider.name_spider)['uuid']
        logging.info(u"mysql连接成功!")
        if spider.proxy_type == "1" or spider.proxy_type == "2" or spider.proxy_type == "3":
            logging.info(u"代理状态:True  代理类型:%s" % spider.proxy_type)
            logging.info(u"获取最新%s条代理" % PROXY_COUT)
            logging.info(u"代理随机切换数：{}".format(RANDOM_NUMBER))
        else:
            logging.info(u"代理状态:False")

    def process_item(self, item, spider):
        # print item['title'][0]
        for k in item:
            item[k] = u"".join(item[k])
            item[k] = re.sub(r"\xa0", "", item[k])
            item[k] = re.sub(r"\u200b", "", item[k])
            item[k] = re.sub(r"\xa5", "", item[k])
            item[k] = re.sub(r"\u2022", "", item[k])
        try:
            # 判断字段是否存在
            if 'pubtime' in item:
                item['pubtime'] = unicode(date_parse.parse_date(item['pubtime']))
            if 're_pubtime' in item:
                item['re_pubtime'] = unicode(date_parse.parse_date(item['re_pubtime']))
        except:
            logging.error(u"时间格式化错误!")
            return item
        # 收集item字段名及值
        fields = []
        values = []

        # 显示采集字段及内容
        for k, v in item.iteritems():
            fields.append(k)
            values.append(v)
        fields.append("net_spider_id")
        values.append(self.net_spider_id)
        if spider.name == "re_bbs":
            re_md5 = hashlib.md5()
            item_md5 = item['url'] + item['re_author'] + item['re_pubtime']
            re_md5.update(item_md5)
            content_md5 = re_md5.hexdigest()
            fields.append("content_md5")
            values.append(content_md5)
        md5 = hashlib.md5()
        md5.update(item['url'])
        url_md5 = md5.hexdigest()
        fields.append("url_md5")
        values.append(url_md5)
        # debug为true时,数据不入库!
        if spider.debug:
            print u"{:=^30}".format(self.cout)
            for k, v in item.iteritems():
                try:
                    print u"{:>13.13}:{}".format(k, v)
                except:
                    pass
            sql = u"INSERT INTO data_spider_temp({}) VALUES ( ".format(u",".join(fields))
            for value in values:
                sql += u"'{}',".format(MySQLdb.escape_string(value))
            sql = sql[:-1] + u");"
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except MySQLdb.Error, e:
                logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
        else:
            try:
                # 根据 item 字段插入数据
                sql = u"INSERT INTO {}({}) VALUES ( ".format(spider.table_name, u",".join(fields))
                for value in values:
                    sql += u"'{}',".format(MySQLdb.escape_string(value))
                sql += u" ) ON DUPLICATE KEY UPDATE "
                sql = sql.replace(u", ) ON DUPLICATE KEY UPDATE", u" ) ON DUPLICATE KEY UPDATE")
                # 插入数据如果数据重复则更新已有数据
                for f in fields:
                    sql += u'{}=VALUES({}),'.format(f, f)
                sql = sql[:-1] + ";"
                self.cur.execute(sql)
                self.conn.commit()
                logging.info(u"数据插入/更新成功!")
            except MySQLdb.Error, e:
                logging.error(u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
        self.cout += 1
        return item

    # 关闭爬虫初始化工作
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        logging.info(u"mysql关闭成功")
