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
import hashlib
import json
import random
import requests
import time

import wechatsogou
from lxml import etree
from requests.auth import HTTPProxyAuth

from date_parse import parse_date
from item_fileds import item_fileds

auth = HTTPProxyAuth("pc1111a", "pc1111a")


def random_proxy():
    proxies = ["10.168.179.8:10080", "10.168.157.28:10080", "10.117.222.62:10080", "10.168.232.64:10080",
               "10.168.28.179:10080", "10.168.47.172:10080", "10.168.237.8:10080", "10.175.201.92:10080",
               "10.171.192.219:10080", "10.132.61.84:10080", "10.168.89.8:10080", "10.171.174.3:10080",
               "10.171.177.13:10080", "10.171.173.237:10080", "10.171.174.206:10080", "10.122.69.240:10080",
               "10.122.70.191:10080", "10.122.70.146:10080", "10.122.72.127:10080", "10.122.72.76:10080",
               "10.122.72.123:10080", "10.122.69.39:10080", "10.122.69.26:10080"]

    auth_proxies = ["27.50.151.125:808",
                    "120.210.206.105:888", "120.210.204.38:888",
                    "101.132.44.60:888", "117.41.185.42:888",
                    "120.210.207.98:888", "222.186.11.66:888", "120.210.204.56:888", "222.73.48.188:888",
                    "210.16.188.34:888", "1.82.230.130:888", "222.73.135.27:888",
                    "103.21.141.83:888", "103.21.142.169:888", "103.21.143.179:888", "117.41.183.203:888",
                    "101.226.179.96:888", "222.73.130.111:888",
                    "117.41.186.201:888", "117.41.186.194:888", "123.249.47.50:888",
                    "112.29.170.195:888", "112.30.128.12:888", "112.30.131.214:888",
                    "112.30.131.187:888", "112.29.173.37:888", "103.28.204.45:888", "103.28.206.63:888",
                    "103.28.206.15:888", "118.123.3.76:888",
                    "120.210.204.164:888",
                    ]

    random_int = random.randint(1, 3)
    # if random_int % 2 == 1:
    return {'http': 'http://{ip}'.format(ip=random.choice(auth_proxies)), "random_int": 1}
    # else:
    #     return {'http': 'http://{ip}'.format(ip=random.choice(proxies)), "random_int": 2}


def get_weixin_auth():
    api_url = "http://testabc.yuwoyg.com:8086/api/web/manage/config/newsConfig/open/searchWeixinAccount?orderBy=id%20asc&columns=account"
    auth_dict = requests.get(api_url).content
    return json.loads(auth_dict)


def proxy_weixin(account):
    proxies = random_proxy()
    if proxies.get("random_int") == 1:
        ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3, auth=auth,
                                            proxies={"http": "{ip}".format(ip=proxies.get("http"))}, timeout=10)
    else:
        ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3,
                                            proxies={"http": "{ip}".format(ip=proxies.get("http"))}, timeout=5)
    # ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3, auth=auth,  timeout=5)
    dot = ws_api.get_gzh_info(account)
    return dot


def weixin_spider():
    cout = 1
    wx_accounts = get_weixin_auth().get("data")
    for i in xrange(len(wx_accounts)):
        wx_account = random.choice(wx_accounts)
        if wx_account.has_key("account"):
            account = wx_account.get("account")
            author_none = proxy_weixin(account)
            if author_none == None:
                with open("author_none.txt", "a+") as w:
                    w.write(account + "\r\n")
            else:
                ws_api = wechatsogou.WechatSogouAPI()
                doc = ws_api.get_gzh_article_by_history(keyword=account)
                name = doc['gzh']['wechat_name']
                for d in doc['article']:
                    try:
                        html = ws_api.get_article_content(d['content_url'])['content_html']
                    except:
                        continue
                    dom = etree.HTML(html)
                    d['content'] = "".join(dom.xpath("//text()")).replace("\n", "").replace(" ", "")
                    d['url'] = d['content_url']
                    d['pubtime'] = parse_date(d['datetime'])
                    d['site_name'] = u"微信公众号"
                    d['author'] = account
                    d['keyword'] = name
                    md5 = hashlib.md5()
                    md5.update(d['content_url'])
                    url_md5 = md5.hexdigest()
                    d['url_md5'] = url_md5
                    d.pop("send_id")
                    d.pop("datetime")
                    d.pop("type")
                    d.pop("main")
                    d.pop("abstract")
                    d.pop("fileid")
                    d.pop("content_url")
                    d.pop("source_url")
                    d.pop("cover")
                    d.pop("copyright_stat")
                    item_fileds(d, "data_wemedia", False)
                    time.sleep(1)
            time.sleep(10)
            cout += 1


if __name__ == "__main__":
    # weixin_spider()
    print get_weixin_auth()
