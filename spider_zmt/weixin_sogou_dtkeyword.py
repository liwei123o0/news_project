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
import hashlib
import json
import sys
import time

import requests
from faker import Faker
from lxml import etree

from item_fileds import item_fileds

reload(sys)
sys.setdefaultencoding("utf8")
fake = Faker(locale="zh_CN")

orderno = "ZF20193195158qiaFzt"
secret = "2dbbf0d00b7242b5ab9f9cd8cf1d1ceb"
timeout = 60
ip = "forward.xdaili.cn"
port = "80"
ip_port = ip + ":" + port
timestamp = str(int(time.time()))  # 计算时间戳
string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
version = sys.version_info
is_python3 = (version[0] == 3)
if is_python3:
    string = string.encode()
md5_string = hashlib.md5(string).hexdigest()  # 计算sign
sign = md5_string.upper()  # 转换成大写
auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port, }
k_url = "http://receiver.yuwoyg.com:18002/api/config/anhui/keyword/weixin_keyword/getNext"
keywords = []
for i in xrange(1, 3, 1):
    h_json = json.loads(requests.get(k_url).content)
    if h_json['value'] != None and h_json['value']['source'] == 'weixin_keyword':
        keywords.append(h_json['value']['keyword'])


def get_proxy():
    txt = json.loads(requests.get("http://testabc.yuwoyg.com:8086/api/web/manage/proxy/get").content)
    ip = txt['data']['ip']
    port = txt['data']['port']
    ip_port = "%s:%s" % (ip, port)
    return {"http": "http://%s" % ip_port, "https": "https://%s" % ip_port}


def run_spider():
    if len(keywords) > 0:
        for keyword in keywords:
            for i in xrange(1, 6, 1):
                url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&query={}&tsn=2&ft=&et=&interation=&wxid=&usip=&page={}".format(
                    keyword, i)
                header = {
                    "Host": "weixin.sogou.com",
                    "Referer": "http://weixin.sogou.com/weixin?type=2&ie=utf8&query={}&tsn=2&ft=&et=&interation=&wxid=&usip=&page={}".format(
                        keyword, i),
                    "User-Agent": fake.user_agent(),
                    # "Proxy-Authorization": auth
                }
                try:
                    txt = requests.post(url, headers=header, proxies=get_proxy(), timeout=timeout, verify=False,
                                        allow_redirects=True).content
                except:
                    print u"链接下载页：%s 出错！" % url
                    continue
                dom = etree.HTML(txt)
                sel = dom.xpath("//div[@class='txt-box']")
                for s in sel:
                    item = {}
                    item['url'] = "".join(s.xpath("./h3/a/@data-share"))
                    pubtime = "".join(s.xpath("./div/@t"))
                    timestruct = time.localtime(int(pubtime))
                    item['pubtime'] = time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
                    try:
                        t = requests.get(item['url'],
                                         headers={
                                             # "Proxy-Authorization": auth,
                                             "User-Agent": fake.user_agent()
                                         },
                                         timeout=timeout, verify=True, proxies=get_proxy()).content
                    except:
                        print u"详情页下载失败！详情页url:%s" % item['url']
                        continue
                    f_sel = etree.HTML(t)
                    try:
                        item['title'] = "".join(f_sel.xpath("//h2/text()")).strip()
                        item['author'] = "".join(f_sel.xpath("//span[@id='profileBt']/a/text()")).strip()
                        item['content'] = "".join(f_sel.xpath("//div[@id='js_content']//p//text()")).strip()
                        item['keyword'] = keyword
                        item["site_name"] = u"微信公众号"
                        md5 = hashlib.md5()
                        md5.update(item['url'])
                        url_md5 = md5.hexdigest()
                        item['url_md5'] = url_md5
                        item_fileds(item, "data_wemedia", debug=True)
                    except:
                        print u"内容解析失败！"
                        continue


if __name__ == "__main__":
    run_spider()
