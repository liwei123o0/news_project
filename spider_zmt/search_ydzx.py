# -*- coding: utf-8 -*-
# ! /usr/bin/env python

import hashlib
import json
import time

import requests
from lxml import etree
from selenium import webdriver

from utils.item_fileds import item_fileds


def get_keyword():
    keywords = []
    for i in xrange(50):
        txt = requests.get("http://receiver.yuwoyg.com:18002/api/config/jiangsu/keyword/ydzx/getNext").content
        json_dict = json.loads(txt)
        words = json_dict['value']['keyword']
        keywords.append(words)
    return keywords


def spider_run():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # 无头浏览
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("http://www.yidianzixun.com")
    keywords = get_keyword()
    urls = []
    for word in keywords:
        driver.find_element_by_xpath("//input[@class='input input-search']").send_keys(u"%s" % word)
        driver.find_element_by_xpath("//button[@class='btn btn-search']").click()
        time.sleep(5)
        for uri in driver.find_elements_by_xpath("//div[@class='channel-news channel-news-0']/a"):
            urls.append(uri.get_attribute("href"))
    for url in urls:
        html = requests.get(url).content
        dom = etree.HTML(html)
        item = {}
        try:
            item['url'] = url
            item['title'] = "".join(dom.xpath("//h2//text()"))
            item['pubtime'] = "".join(dom.xpath("//div[@class='meta']/span[last()-1]//text()"))
            item['content'] = "".join(dom.xpath("//div[@class='imedia-article']//text()"))
            item['author'] = "".join(dom.xpath("//a[@class='doc-source']//text()"))
            item['author_url'] = "http://www.yidianzixun.com" + "".join(dom.xpath("//a[@class='wemedia-name']/@href"))
        except:
            continue
        item['site_name'] = u'一点号'
        md5 = hashlib.md5()
        md5.update(item["url"])
        item['url_md5'] = md5.hexdigest()
        item_fileds(item, "data_wemedia", False)


if __name__ == '__main__':
    # spider_run()
    urls = ['https://www.toutiao.com/c/user/5893695579/#mid=5893937926/',
            'https://www.toutiao.com/c/user/5460505913/#mid=5541133821/',
            'https://www.toutiao.com/c/user/73195063644/#mid=1582124699364365',
            'https://www.toutiao.com/c/user/101244119417/#mid=1606219373887502',
            'https://www.toutiao.com/c/user/81557582216/#mid=1587290390288398',
            'https://www.toutiao.com/c/user/4850100857/#mid=4850100857']
    for url in urls:
        item = {}
        item['url'] = url
        md5 = hashlib.md5()
        md5.update(item["url"])
        item['url_md5'] = md5.hexdigest()
        print url, item['url_md5']
