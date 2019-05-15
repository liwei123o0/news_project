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
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
import time
import os

urls = ["http://172.16.100.136:6800/schedule.json", "http://172.16.100.59:6800/schedule.json",
        "http://172.16.100.67:6800/schedule.json",
        "http://172.16.100.209:6800/schedule.json", "http://172.16.100.128:6800/schedule.json"]
spider_all = "http://sync.yuwoyg.com:8086/api/web/manage/config/newsConfig/open/searchAll?columns=spider_name%2Ccrontab%2Cspider_type"


# 每600秒执行一次
@sched.scheduled_job('interval', seconds=600)
def timed20_job():
    timestruct = time.localtime(time.time())
    time_data = time.strftime("%Y-%m-%d %H:%M:%S", timestruct)
    print u"调度器闲置,等待任务中！时间：%s" % time_data


@sched.scheduled_job('interval', minutes=10)
def timed2_job10():
    os.system("python C:\\bak\\spider_bbs\\bbs_guanyun.py")
    os.system("python C:\\bak\\spider_bbs\\bbs_hmting.py")
    os.system("python C:\\bak\\spider_bbs\\bbs_lyg.py")
    print u"10分钟调度成功！"


sched.start()
