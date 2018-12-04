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
import requests
from uuid import uuid4
import random
import json
import time


urls = ["http://222.93.105.248:6800/schedule.json", "http://222.93.106.15:6800/schedule.json",
        "http://222.93.106.248:6800/schedule.json",
        "http://222.93.106.240:6800/schedule.json", "http://180.101.149.178:6800/schedule.json"]
spider_all = "http://sync.yuwoyg.com:8086/api/web/manage/config/newsConfig/open/searchAll?columns=spider_name%2Ccrontab%2Cspider_type"
def run ():
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
                txt = json.loads(requests.post(url=ip, data=data).content)
                txt['ip'] = ip
                time.sleep(0.1)
                print(txt)
        except:
            cout += 1
            continue
    print("任务分发总数：%s \n 错误数：%s" % (len(name_spiders), cout))

if __name__=='__main__':
    pass
    run()
    # url = 'http://sync.yuwoyg.com:8086/api/web/manage/config/newsConfig/searchAll?columns=spider_name%2Ccrontab'
    # print(requests.get(url).content)
    # a = dict({"name_spider": "liwei"})
    # print('name_spider' in a.keys())
