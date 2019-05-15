# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:v1.0
@var:随机代理
@note:默认每请求30条随机更换代理

"""


class HeadersMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == "sogou_wx":
            r = request.url.find("&tsn=")
            keyword = request.url[52:r]
            request.meta['Host'] = u"weixin.sogou.com"
            request.meta[
                'Referer'] = u"http://weixin.sogou.com/weixin?type=2&ie=utf8&query={keyword}&tsn=1&ft=&et=&interation=&wxid=&usip=".format(
                keyword=keyword)
            request.meta['User-Agent'] = u"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
            request.meta['download_timeout'] = 30


if __name__ == '__main__':
    pass
    # import re
    # url ="http://weixin.sogou.com/weixin?type=2&ie=utf8&query=716%E622233%89%22280&tsn=1&ft=&et=&interation=&wxid=&usip=&page=1"
    # l = url.find("query=")
    # r = url.find("&tsn=")
    # print l, r
    # print url[52:64]
