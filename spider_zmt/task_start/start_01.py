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

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


# 每12小时执行一次


# 每26小时执行一次
@sched.scheduled_job('interval', hours=26)
def timed2_job():
    os.system("python C:\\Project\\phantomjs\\toutiao_author_spider.py")
    os.system("python C:\\Project\\phantomjs\\baijia_author_spider1000.py")
    os.system("python C:\\Project\\phantomjs\\baijia_author_spider2000.py")
    os.system("python C:\\Project\\phantomjs\\baijia_author_spider3000.py")
    print u"26小时调度成功！"


# 每4小时执行一次
@sched.scheduled_job('interval', hours=5)
def timed2_job():
    os.system("python C:\\Project\\sogouwx\\weixin_sogou.py")
    print u"4小时调度成功！"


# 每2秒执行一次
@sched.scheduled_job('interval', hours=1)
def timed20_job():
    os.system("python C:\\Project\\sogouwx\\weixin_sogou_dtkeyword.py")
    print u"调度器闲置,等待任务中！"


sched.start()
