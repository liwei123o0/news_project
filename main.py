# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:
@var:
@note:

"""
import uuid
from scrapy import cmdline
import os
def main():
    print u"""
        scrapy shell 测试工具V1.0！
            info      显示采集数据！(默认)
            debug     显示详细任务采集情况！
    """
    uid = uuid.uuid1().hex
    debug = raw_input(u"请输入调试模式：")
    spider_type = raw_input(u"请输入爬虫类型：")
    spider_name = raw_input(u"请输入爬虫名称：")
    if debug != "info" and debug != "debug":
        debug = "info"
    if debug == "info":
        print("#########info##########")
        scrapyrun = "scrapy crawl %s -a name_spider=%s -a spider_jobid=%s -a debug=true" % (
        spider_type, spider_name, uid)
        cmdline.execute(scrapyrun.split())
    else:
        print("#########debug##########")
        scrapyrun = "scrapy crawl %s -a name_spider=%s -a spider_jobid=%s -a debug=true -L DEBUG" % (
        spider_type, spider_name, uid)
        cmdline.execute(scrapyrun.split())

if __name__ == "__main__":
    main()
