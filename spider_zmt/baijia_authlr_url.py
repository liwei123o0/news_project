# -*- coding: utf-8 -*-
# ! /usr/bin/env python


import hashlib

from selenium import webdriver

from utils.item_fileds import item_fileds


def get_urls():
    urls = []
    with open('baijia_url.txt', 'rb')as f:
        uris = f.readlines()
    for url in uris:
        url = url.replace("\n", "").replace("\r", "")
        urls.append(url)
    return urls


def selenium_spider():
    urls = get_urls()
    driver = webdriver.Firefox()
    for url in urls:
        driver.get(url)
        a = driver.find_element_by_xpath("//div[@class='detail']/a")
        uri = a.get_attribute("href")
        item = {}
        item["url"] = uri
        item['site_name'] = u'百家号'
        md5 = hashlib.md5()
        md5.update(item["url"])
        item['url_md5'] = md5.hexdigest()
        item_fileds(item, "author_url", False)
    driver.quit()


def main():
    selenium_spider()


if __name__ == "__main__":
    main()
