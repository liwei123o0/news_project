# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:李哥工作圈
@QQ:877129310
@VIP交流群:141342076
@version:V1.0
@var:
@note:

"""
import os

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
url = "http://10.81.172.2:6800/schedule.json"
urlloc = "http://127.0.0.1:6800/schedule.json"


# 每12小时执行一次
@sched.scheduled_job('interval', hours=12)
def timed1_job():
    wy163_zmt_dict = {"project": "basespider", "spider": "163_zmt"}
    requests.post(url=url, data=wy163_zmt_dict)
    print u"12小时调度成功！"
    pass


# 每4小时执行一次
@sched.scheduled_job('interval', hours=4)
def timed4_job():
    sohu_zmt_dict = {"project": "basespider", "spider": "sohu_zmt"}
    requests.post(url=urlloc, data=sohu_zmt_dict)
    daf_zmt_dict = {"project": "basespider", "spider": "daf_zmt"}
    requests.post(url=url, data=daf_zmt_dict)
    os.system("python C:\\Project\\phantomjs\\yidian_spider.py")
    print u"4小时调度成功！"


# 每2小时执行一次
@sched.scheduled_job('interval', hours=2)
def timed2_job():
    sogo_wx_dict = {"project": "basespider", "spider": "sogou_wx"}
    requests.post(url=urlloc, data=sogo_wx_dict)
    os.system("python C:\\Project\\phantomjs\\toutiao_author_spider.py")
    os.system("python C:\\Project\\phantomjs\\yidian_serach.py")
    print u"2小时调度成功！"


# 每20分钟执行一次
@sched.scheduled_job('interval', minutes=20)
def timed20_job():
    qie_zmt_dict = {"project": "basespider", "spider": "qie_zmt"}
    baidu_zmt_dict = {"project": "basespider", "spider": "baidu_zmt"}
    requests.post(url=urlloc, data=qie_zmt_dict)
    requests.post(url=urlloc, data=baidu_zmt_dict)
    print u"20分钟调度成功！"


# 每10分钟执行一次
@sched.scheduled_job('interval', minutes=10)
def timed10_job():
    os.system("python C:\\Project\\phantomjs\\toutiao_spider.py")
    os.system("python C:\\Project\\phantomjs\\uc_spider.py")
    print u"10分钟调度成功！"


# 每2秒执行一次
@sched.scheduled_job('interval', seconds=120)
def timed20_job():
    print u"调度器闲置,等待任务中！"


sched.start()
