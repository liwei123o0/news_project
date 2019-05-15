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


def selenium_uc_spider():
    driver = webdriver.PhantomJS()
    driver.get("http://www.vyi.cc/uc/index.php")
    time.sleep(1)
    urls = []
    for url in driver.find_elements_by_xpath(u"//a[contains(.,'进入UC')]"):
        uri = url.get_attribute("href")
        urls.append(uri)
    for url in urls:
        item = {}
        item["url"] = url
        try:
            driver.get(url)
            item['title'] = driver.find_element_by_xpath("//h1").text
            item['pubtime'] = driver.find_element_by_xpath(
                "//p[@class='wmAuthor__header-wm-info_detail__3ccfd1e8a9']/span[last()-1]").text
            item['content'] = driver.find_element_by_xpath(
                "//div[@class='article-content uc-nf-fontsize-change-dom simple-ui']").text
            item['author'] = driver.find_element_by_xpath("//h3/p").text
        except:
            continue
        item['site_name'] = u'UC号'
        md5 = hashlib.md5()
        md5.update(item["url"])
        item['url_md5'] = md5.hexdigest()
        item_fileds(item, "data_wemedia", False)
    driver.quit()


def main():
    selenium_uc_spider()


if __name__ == "__main__":
    main()
