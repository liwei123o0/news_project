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
import MySQLdb
import hashlib
import time

from selenium import webdriver

from utils.item_fileds import item_fileds


def get_urls():
    # conn = MySQLdb.connect(host="127.0.0.1", port=3306, user='root', passwd='root', db='acq_data',
    #                        charset=u"utf8")
    conn = MySQLdb.connect(host="rm-bp1i4s7mgs401rj2n.mysql.rds.aliyuncs.com", port=3306, user='acq_data',
                           passwd='MuF8+Vsq2j)^RfMr', db='acq_data',
                           charset=u"utf8")
    cur = conn.cursor()
    cur.execute(u"SELECT url FROM author_url WHERE site_name='头条号'  ORDER BY insert_time DESC ")
    urls = cur.fetchall()
    uris = []
    for url in urls:
        uris.append(url[0])
    cur.close()
    conn.close()
    return uris


def selenium_toutiaoauthor_spider():
    uris = get_urls()

    for uri in uris:
        try:
            driver = webdriver.PhantomJS()
            driver.get(uri)
            time.sleep(1)
            urls = []
            for url in driver.find_elements_by_xpath(u"//a[@class='link title']"):
                url = url.get_attribute("href")
                urls.append(url)
        except:
            continue
        for urll in urls:
            item = {}
            item["url"] = urll
            try:
                driver.get(urll)
                item['title'] = driver.find_element_by_xpath("//h1").text
                item['pubtime'] = driver.find_element_by_xpath("//div[@class='article-sub']/span[2]").text
                item['content'] = driver.find_element_by_xpath("//div[@class='article-content']").text
                item['author'] = driver.find_element_by_xpath("//div[@class='article-sub']/span[1]").text
                item['author_url'] = driver.find_element_by_xpath("//div[@class='user-card-name']/a").get_attribute(
                    "href")
            except:
                continue
            item['site_name'] = u'头条号'
            md5 = hashlib.md5()
            md5.update(item["url"])
            item['url_md5'] = md5.hexdigest()
            item_fileds(item, "data_wemedia", False)
        driver.quit()


def main():
    selenium_toutiaoauthor_spider()


if __name__ == "__main__":
    main()
