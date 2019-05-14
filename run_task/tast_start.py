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
import requests
from uuid import uuid4
import random
import json
import time

urls = ["http://222.93.105.248:6800/schedule.json", "http://222.93.106.15:6800/schedule.json",
        "http://222.93.106.248:6800/schedule.json",
        "http://222.93.106.240:6800/schedule.json", "http://180.101.149.178:6800/schedule.json"]
spider_all = "http://sync.yuwoyg.com:8086/api/web/manage/config/newsConfig/open/searchAll?columns=spider_name%2Ccrontab%2Cspider_type"


# 每60分钟执行一次
@sched.scheduled_job('interval', minutes=120)
def timed10_job():
    cout = 0
    api_all = json.loads(requests.get(spider_all).content)
    name_spiders = api_all['data']
    for name_spider in name_spiders:
        try:
            if 'spider_name' in name_spider.keys():
                uuid = uuid4().hex
                ip = random.choice(urls)
                data = {"project": "news_project",
                        "spider_type": name_spider['spider_type'],
                        "name_spider": name_spider['spider_name'],
                        "spider_jobid": uuid}
                if name_spider['spider_type'] == "bbs":
                    txt = json.loads(requests.post(url=ip, data=data).content)
                    data["spider_type"] = "re_bbs"
                    time.sleep(0.1)
                    json.loads(requests.post(url=ip, data=data).content)
                    time.sleep(0.1)
                    txt['ip'] = ip
                    print(txt)
                else:
                    txt = json.loads(requests.post(url=ip, data=data).content)
                    txt['ip'] = ip
                    time.sleep(0.1)
                    print(txt)
        except:
            cout += 1
            continue
    print(u"任务分发总数：%s \n错误数：%s" % (len(name_spiders), cout))
    print u"60分钟调度成功！"


# 每600秒执行一次
@sched.scheduled_job('interval', seconds=600)
def timed20_job():
    timestruct = time.localtime(time.time())
    time_data = time.strftime("%Y-%m-%d %H:%M:%S", timestruct)
    print u"调度器闲置,等待任务中！时间：%s" % time_data


@sched.scheduled_job('interval', minutes=30)
def timed2_job():
    import os
    os.system("python C:\\news_project\\log_analysis.py")
    print u"30分钟调度成功！"


@sched.scheduled_job('interval', minutes=10)
def timed2_job10():
    conf = "http://sync.yuwoyg.com:8086/api/web/manage/config/newsConfig/open/search?filters[0].columnName=spider_name&filters[0].op=2&filters[0].value=hmting_01"
    api_all = json.loads(requests.get(conf).content)
    name_spider = api_all['data']["datas"][0]
    print name_spider
    uuid = uuid4().hex
    ip = random.choice(urls)
    data = {"project": "news_project",
            "spider_type": name_spider['spider_type'],
            "name_spider": name_spider['spider_name'],
            "spider_jobid": uuid}
    txt = json.loads(requests.post(url=ip, data=data).content)
    data["spider_type"] = "re_bbs"
    json.loads(requests.post(url=ip, data=data).content)
    txt['ip'] = ip
    time.sleep(0.1)
    print(txt)
    print u"10分钟调度成功！"


sched.start()
