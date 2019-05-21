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

import MySQLdb
import requests
from lxml import etree
from selenium import webdriver

from utils.connect_mysql import mysql_connect
from utils.item_fileds import item_fileds


def get_authorurl():
    conn, cur = mysql_connect()
    cur.execute("SELECT url FROM author_url WHERE site_name='头条号_iphone'  ORDER BY insert_time DESC")
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
        item['site_name'] = u'头条号'
        md5 = hashlib.md5()
        md5.update(item["url"])
        item['url_md5'] = md5.hexdigest()
        item_fileds(item, "data_wemedia", True)


def main():
    selenium_toutiao_spider()


if __name__ == "__main__":
    # main()
    urls = ['https://url.cn/59RGSap', 'https://url.cn/51Z5fFX',
            'https://url.cn/5ToXCF9', 'https://url.cn/5acY1J1',
            'https://url.cn/5dlNq5V', 'https://url.cn/5rNNUaA',
            'https://url.cn/5N2GzjV', 'https://url.cn/5DWwn0t',
            'https://url.cn/5aieiCI', 'https://url.cn/5EnA4jT',
            'https://url.cn/5H6CqRS', 'https://url.cn/5P25Hhz',
            'https://url.cn/5VvPvI5', 'https://url.cn/5HKwcMm',
            'https://url.cn/5GLda9f', 'https://url.cn/5KgAjxz',
            'https://url.cn/5zBfrx5', 'https://url.cn/5YrG39b',
            'https://url.cn/5fFZF4Z', 'https://url.cn/5tDrIoh',
            'https://url.cn/5F1mIR0', 'https://url.cn/5Bfx3BG',
            'https://url.cn/5V69Cue', 'https://url.cn/5514GgK',
            'https://url.cn/5IfIcXL', 'https://url.cn/5n6DGw6',
            'https://url.cn/5vjdDQk', 'https://url.cn/5H1itNn',
            'https://url.cn/5r2T9n2', 'https://url.cn/5bhod0z',
            'https://url.cn/5ODjCw1', 'https://url.cn/5LKpyZ1',
            'https://url.cn/52LjS3r', 'https://url.cn/5ycUwpd',
            'https://url.cn/5Bfx3BG', 'https://url.cn/5AY7qXN',
            'http://url.cn/5EZcgyc', 'https://url.cn/5DKpqNs',
            'https://url.cn/5U0MvXF', 'https://url.cn/5QB2db8',
            'https://url.cn/5welgEP', 'https://url.cn/5XeL2KV',
            'https://url.cn/5A8uTV8', 'https://url.cn/5GF6hoW',
            'https://url.cn/58qeAkB', 'https://url.cn/5YrG39b',
            'https://url.cn/5TYNcKK', 'https://url.cn/5rkFFe9',
            'https://url.cn/5xUHHsk', 'https://url.cn/5gAheTZ',
            'https://url.cn/5yIvyKn', 'https://url.cn/5PetfA8',
            'https://url.cn/5k17aNu', 'https://url.cn/5VW44WR',
            'https://url.cn/59yYNAu', 'https://url.cn/5tzvnFu',
            'https://url.cn/5lwjNhs', 'https://url.cn/5QFORqO',
            'https://url.cn/54q7yDB', 'https://url.cn/5mQYdrg',
            'https://url.cn/57RXl7Y', 'https://url.cn/5WCdP7v']
    for url in urls:
        md5 = hashlib.md5()
        md5.update(url)
        url_md5 = md5.hexdigest()
        print url, url_md5, u'头条号_iphone'
