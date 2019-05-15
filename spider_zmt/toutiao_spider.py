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

from selenium import webdriver

from utils.item_fileds import item_fileds


def selenium_toutiao_spider():
    driver = webdriver.PhantomJS()
    driver.get("http://vyi.wangzherongyao.cn/toutiao/index.php")
    time.sleep(1)
    urls = []
    for url in driver.find_elements_by_xpath(u"//a[contains(.,'查看')]"):
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
            item['author_url'] = driver.find_element_by_xpath("//div[@class='user-card-name']/a").get_attribute("href")
        except:
            continue
        item['site_name'] = u'头条号'
        md5 = hashlib.md5()
        md5.update(item["url"])
        item['url_md5'] = md5.hexdigest()
        item_fileds(item, "data_wemedia", False)
    driver.quit()


def main():
    selenium_toutiao_spider()


if __name__ == "__main__":
    main()
