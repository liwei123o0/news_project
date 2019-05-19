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
import time

import json
import requests
from selenium import webdriver

from utils.item_fileds import item_fileds


def get_keyword():
    keywords = []
    for i in xrange(5):
        txt = requests.get("http://receiver.yuwoyg.com:18002/api/config/jiangsu/keyword/jrtt/getNext").content
        json_dict = json.loads(txt)
        words = json_dict['value']['keyword']
        keywords.append(words)
    return keywords


def selenium_toutiao_spider():
    chrome_options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    # 无头浏览
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    keywords = get_keyword()
    for word in keywords:
        driver.get(u"https://www.toutiao.com/search/?keyword={}".format(word))
        time.sleep(10)
        urls = []
        for url in driver.find_elements_by_xpath(u"//a[@class='link title']"):
            uri = url.get_attribute("href")
            urls.append(uri)
        for url in urls:
            item = {}
            item["url"] = url
            try:
                driver.get(url)
                item['title'] = driver.find_element_by_xpath("//h1").text
                item['pubtime'] = driver.find_element_by_xpath("//div[@class='article-sub']/span[last()]").text
                item['content'] = driver.find_element_by_xpath("//div[@class='article-content']").text
                item['author'] = driver.find_element_by_xpath("//div[@class='article-sub']/span[last()-1]").text
                item['author_url'] = driver.find_element_by_xpath("//div[@class='user-card-name']/a").get_attribute(
                    "href")
            except:
                continue
            item['site_name'] = u'头条号'
            md5 = hashlib.md5()
            md5.update(item["url"])
            item['url_md5'] = md5.hexdigest()
            item_fileds(item, "data_wemedia", True)
        driver.quit()


def main():
    selenium_toutiao_spider()


if __name__ == "__main__":
    main()
