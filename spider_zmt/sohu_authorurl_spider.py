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

import requests
from lxml import etree
from selenium import webdriver

from utils.connect_mysql import mysql_connect
from utils.item_fileds import item_fileds


def get_authorurl():
    conn, cur = mysql_connect()
    cur.execute("SELECT url FROM author_url WHERE site_name='搜狐号'  ORDER BY insert_time DESC")
    author_urls = []
    for url in cur.fetchall():
        author_urls.append(url[0])
    cur.close()
    conn.close()
    return author_urls


def selenium_toutiao_spider():
    chrome_options = webdriver.ChromeOptions()
    # firefox_options = webdriver.FirefoxOptions()
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    # 无头浏览
    # chrome_options.add_argument('--headless')
    # firefox_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver = webdriver.Firefox(firefox_options=firefox_options)
    author_urls = get_authorurl()
    urls = []
    for url in author_urls:
        driver.get(url)
        time.sleep(1)
        for url in driver.find_elements_by_xpath("//div[@class='content-inner']//a"):
            uri = url.get_attribute("href")
            urls.append(uri)
    driver.quit()
    for url in urls:
        item = {}
        item["url"] = url
        try:
            html = requests.get(url).content
            dom = etree.HTML(html)
            item['title'] = "".join(dom.xpath("//h1//text()"))
            item['pubtime'] = "".join(dom.xpath("//span[@class='at-time']/text()"))
            item['content'] = "".join(dom.xpath("//div[@class='at-cnt-main']//text()"))
            item['author'] = "".join(dom.xpath("//span[@class='at-media-name']//text()"))
        except:
            continue
        item['site_name'] = u'搜狐号'
        md5 = hashlib.md5()
        md5.update(item["url"])
        item['url_md5'] = md5.hexdigest()
        item_fileds(item, "data_wemedia", True)


def main():
    selenium_toutiao_spider()


if __name__ == "__main__":
    main()
