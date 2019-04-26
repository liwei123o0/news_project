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
import re
import uuid
from collections import OrderedDict
from datetime import datetime, timedelta

import MySQLdb
import requests
from lxml import etree
from selenium import webdriver

conf = "http://sync.yuwoyg.com:8086/api/web/manage/config/newsConfig/open/search?filters[0].columnName=spider_name&filters[0].op=2&filters[0].value=hmting_01"
api_all = json.loads(requests.get(conf).content)
name_spider = api_all['data']["datas"][0]
urls = name_spider["start_urls"].split(",")

__all__ = ['parse_date', 'tz_offset']


def parse_date(x, fmt='auto', tz='+08:00', err=None):
    """
    Parse datetime `x` with format `fmt` and timezone `tz`.
    Return datetime in UTC
    'tz' 支持类型为('+00:00','cst','utc')时间区域类型

    :param x: datetime string
    :type x: str
    :param fmt: datetime format
    :type fmt: str
    :param tz: timezone
    :type fmt: str
    """
    try:

        x = unicode(x)
        fmt = unicode(fmt)

        utcnow = datetime.utcnow()
        offset = tz_offset(tz)
        now = utcnow + offset

        if fmt == 'auto':
            date = _parse(x, now)
        elif fmt in ['epoch', 'unix']:
            date = datetime.utcfromtimestamp(int(x))
            offset = timedelta(0)
        else:
            date = datetime.strptime(x.encode('utf-8'), fmt.encode('utf-8'))

        date = (date + (offset - timedelta(hours=8)))
        return date

    except:
        if err:
            raise
        return datetime.utcfromtimestamp(0)


# 转换对应时差时间格式
def tz_offset(tz):
    tz = tz.lower().strip()
    if tz == 'cst':
        offset = timedelta(hours=8)
    elif tz == 'utc':
        offset = timedelta()
    else:
        res = re.search(r'(?P<F>[-+])(?P<HH>\d{2}):?(?P<MM>\d{2})', tz).groupdict()
        offset = timedelta(
            hours=int(res['HH']),
            minutes=int(res['MM'])
        ) * (1 if res.get('F', '+') == '+' else -1)
    return offset


def _parse(x, now=None):
    # 当前时间
    # now = now or datetime.utcnow()
    # 秒
    now_SS = date_scale(now, 'SS')
    # 分
    now_MM = date_scale(now, 'MM')
    # 小时
    now_HH = date_scale(now, 'HH')
    # 天
    now_dd = date_scale(now, 'dd')
    # 月
    now_mm = date_scale(now, 'mm')
    # 年
    now_YY = date_scale(now, 'YY')
    # 预处理
    x = re.sub(u'刚刚|刚才', now_MM.strftime('%Y-%m-%d %H:%M:%S'), x)
    # x = re.sub(u'刚刚|刚才', now_MM.strftime('%F %T'), x)
    x = re.sub(u'几', u'0', x)
    x = re.sub(ur'(?<=[\d半前昨今明后])(天|号)', u'日', x)
    # 获取一天时间
    one_dd = date_unit('dd')
    rdays = {
        u'前日': now_dd - one_dd * 2,
        u'昨日': now_dd - one_dd * 1,
        u'今日': now_dd,
        u'明日': now_dd + one_dd * 1,
        u'后日': now_dd + one_dd * 2,
    }
    # 将x值转换成rdays对应时间格式
    for k, v in rdays.iteritems():
        x = x.replace(k, v.strftime(' %Y-%m-%d '))
        # x = x.replace(k, v.strftime(' %F '))

    x = re.sub(ur'(?<=\d)[/.](?=\d)', u'-', x)
    x = re.sub(ur'[^-:\s\d前后半秒分时日周月年]', u'', x)
    x = re.sub(ur'(?<=\d)\s+(?!\d)', u'', x)
    x = re.sub(ur'(?<!\d)\s+(?=\d)', u'', x)
    x = re.sub(ur'(?<!\d)\s+(?!\d)', u'', x)
    x = re.sub(ur'(?<!年)(?=(^(1[0-2]|\d+))月(\d+)日)', u' %d年' % now.year, x)
    x = re.sub(ur'(\d+)年(\d+)月(\d+)日', ur'\g<1>-\g<2>-\g<3> ', x)
    x = x.strip()

    if '-' in x or ':' in x:

        parts = {}
        pats = [
            ur'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})',
            ur'(?P<hour>\d{1,2}):(?P<minute>\d{1,2})(:(?P<second>\d{1,2}))?',
        ]
        for p in pats:
            m = re.search(p, x)
            if m:
                parts.update(m.groupdict())

        for k, v in parts.items():
            if v == None:
                del parts[k]
            else:
                parts[k] = int(v)

        if parts:
            parts['year'] = parts.get('year', now.year)
            parts['month'] = parts.get('month', now.month)
            parts['day'] = parts.get('day', now.day)

            return datetime(**parts)

    if u'半' in x:

        halves = {
            u'半分': u'30秒',
            u'半时': u'30分',
            u'半日': u'12时',
            u'半周': u'84时',
            u'半月': u'15日',
            u'半年': u'6月',
        }

        for k, v in halves.iteritems():
            x = re.sub(k, v, x)

    us = {
        u'年': 'YY',
        u'月': 'mm',
        u'周': 'ww',
        u'日': 'dd',
        u'时': 'HH',
        u'分': 'MM',
        u'秒': 'SS',
    }
    m = re.search(ur'(?P<num>\d+)(?P<unit>%s)(?P<flag>前|后)' % (u'|'.join(us.keys())), x)
    if m:
        d = m.groupdict()
        k = d['unit']
        f = -1 if d['flag'] == u'前' else 1
        v = f * int(d['num'])
        u = date_unit(us[k])
        s = 'dd' if us[k] == 'ww' else us[k]
        date = date_scale(now + u * v, s)
        return date
    for i in re.findall(ur'(?<!\d)(\d{8}|\d{10}|\d{13})(?!\d)', x):
        k = len(i)
        v = int(i)
        if k == 8:
            date = datetime.strptime(i, '%Y%m%d')
        elif k == 10:
            date = datetime.fromtimestamp(v)
        elif k == 13:
            date = datetime.fromtimestamp(v / 1000)
        else:
            raise Exception()

        return date

    raise Exception()


def date_scale(dt, scale='MM'):
    scales = OrderedDict([
        ('MS', 'microsecond'),  # 微秒
        ('SS', 'second'),  # 秒
        ('MM', 'minute'),  # 分钟
        ('HH', 'hour'),  # 小时
        ('dd', 'day'),  # 天
        ('mm', 'month'),  # 月
        ('YY', 'year'),  # 年
    ])

    assert scale in scales

    for k, v in scales.iteritems():
        if k == scale:
            return dt
        dt = dt.replace(**{v: 1 if k in ['dd', 'mm'] else 0})

    raise Exception()


_units = dict(
    SS=timedelta(seconds=1),
    MM=timedelta(minutes=1),
    HH=timedelta(hours=1),
    dd=timedelta(days=1),
    ww=timedelta(days=7),
    mm=timedelta(days=30),
    YY=timedelta(days=365)
)


def date_unit(unit):
    return _units[unit]


def item_fileds(item, tablename, type_name, debug):
    fields = []
    values = []
    if type_name == "re_bbs":
        re_md5 = hashlib.md5()
        url = item['url'].encode("utf8")
        re_author = item['re_author'].encode("utf8")
        re_pubtime = item['re_pubtime'].encode("utf8")
        uap = url + re_author + re_pubtime
        item_md5 = uap
        re_md5.update(item_md5)
        content_md5 = re_md5.hexdigest()
        fields.append("content_md5")
        values.append(content_md5)
    md5 = hashlib.md5()
    md5.update(item['url'])
    url_md5 = md5.hexdigest()
    fields.append("url_md5")
    values.append(url_md5)
    if debug:
        for k, v in item.iteritems():
            if k == "pubtime" or k == "re_pubtime":
                v = parse_date(v)
            print u"{:>13.13}:{}".format(k, v)
    else:
        conn = MySQLdb.connect(host="127.0.0.1", port=3306, user='root', passwd='root', db='acq_data',
                               charset=u"utf8")
        cur = conn.cursor()
        for k, v in item.iteritems():
            if k == "pubtime":
                v = parse_date(v)
            fields.append(k)
            values.append(v)
        try:
            # 根据 item 字段插入数据
            cur.execute(
                u"INSERT INTO {}({}) VALUES({});".format(tablename,
                                                         u",".join(fields), u','.join([u'%s'] * len(fields))),
                values)
            conn.commit()
            print (u"数据插入成功!")
        except MySQLdb.Error, e:
            print (u"Mysql Error %d: %s" % (e.args[0], e.args[1]))
        cur.close()
        conn.close()


def spider_run():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # 无头浏览
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    uris = []
    for url in urls:
        url_slit = url.split(":")
        urii = ":".join(url_slit[1:-1]).strip()
        site_name = url_slit[0].strip()
        source_url = url_slit[-1].strip()
        driver.get(urii)
        driver.implicitly_wait(10)
        for uri in driver.find_elements_by_xpath(json.loads(name_spider['rules'])['rules_listxpath']):
            uris.append("{}:{}:{}".format(site_name, uri.get_attribute("href"), source_url))
    driver.quit()
    spider_jobid = uuid.uuid4().hex
    for uri in uris:
        url_slit = uri.split(":")
        urii = ":".join(url_slit[1:-1]).strip()
        site_name = url_slit[0].strip()
        source_url = url_slit[-1].strip()
        html = requests.get(urii).content
        dom = etree.HTML(html)
        item = {}
        try:

            item['url'] = uri
            item['title'] = u"".join(dom.xpath(json.loads(name_spider['fields'])['fields']['title']['xpath'])).strip()
            item['pubtime'] = u"".join(
                dom.xpath(json.loads(name_spider['fields'])['fields']['pubtime']['xpath'])).strip()
            item["pubtime"] = item["pubtime"].replace(u"发表于 ", u"20")
            item['content'] = u"".join(
                dom.xpath(json.loads(name_spider['fields'])['fields']['content']['xpath'])).strip()
            item['author'] = u"".join(dom.xpath(json.loads(name_spider['fields'])['fields']['author']['xpath'])).strip()
            item['site_name'] = site_name
            item['source_url'] = source_url
            item['net_spider_id'] = name_spider["uuid"]
            item['spider_jobid'] = spider_jobid
            item_fileds(item, "data_bbs", "bbs", True)
            loop_content = dom.xpath(json.loads(name_spider['fields'])['fields']['loop_content']['xpath'])
            for loop in loop_content:
                item = {}
                item['url'] = uri
                item['title'] = u"".join(
                    dom.xpath(json.loads(name_spider['fields'])['fields']['title']['xpath'])).strip()
                item['re_author'] = u"".join(
                    loop.xpath(json.loads(name_spider['fields'])['fields']['re_author']['xpath'])).strip()
                item['re_content'] = u"".join(
                    loop.xpath(json.loads(name_spider['fields'])['fields']['re_content']['xpath'])).strip()
                item['re_pubtime'] = u"".join(
                    loop.xpath(json.loads(name_spider['fields'])['fields']['re_pubtime']['xpath'])).strip()
                item["re_pubtime"] = item["re_pubtime"].replace(u"发表于 ", u"20")
                item['site_name'] = site_name
                item['source_url'] = source_url
                item['net_spider_id'] = name_spider["uuid"]
                item['spider_jobid'] = spider_jobid
                item_fileds(item, "data_comment", "re_bbs", True)
        except:
            print "error_download"
            continue


if __name__ == '__main__':
    spider_run()
