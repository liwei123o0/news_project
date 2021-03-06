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

author_urls = [
    "http://www.yidianzixun.com/channel/m653533",
    "http://www.yidianzixun.com/channel/m87865",
    "http://www.yidianzixun.com/channel/m1169938",
    "http://www.yidianzixun.com/channel/m722947",
    "http://www.yidianzixun.com/channel/m1246176",
    "http://www.yidianzixun.com/channel/m381268",
    "http://www.yidianzixun.com/channel/m239729",
    "http://www.yidianzixun.com/channel/m541146",
    "http://www.yidianzixun.com/channel/m88097",
    "http://www.yidianzixun.com/channel/m93053",
    "http://www.yidianzixun.com/channel/m1206271",
    "http://www.yidianzixun.com/channel/m561723",
    "http://www.yidianzixun.com/channel/m154324",
    "http://www.yidianzixun.com/channel/m564620",
    "http://www.yidianzixun.com/channel/m1439233",
    "http://www.yidianzixun.com/channel/m322971",
    "http://www.yidianzixun.com/channel/m1427222",
    "http://www.yidianzixun.com/channel/m141564",
    "http://www.yidianzixun.com/channel/m323709",
    "http://www.yidianzixun.com/channel/m93056",
    "http://www.yidianzixun.com/channel/e35184",
    "http://www.yidianzixun.com/channel/s34491",
    "http://www.yidianzixun.com/channel/sc57",
    "http://www.yidianzixun.com/channel/u7580",
    "http://www.yidianzixun.com/channel/u504",
    "http://www.yidianzixun.com/channel/u8343",
    "http://www.yidianzixun.com/channel/u7851",
    "http://www.yidianzixun.com/channel/m58186",
    "http://www.yidianzixun.com/channel/s30225",
    "http://www.yidianzixun.com/channel/u13386",
    "http://www.yidianzixun.com/channel/sc26",
    "http://www.yidianzixun.com/channel/sc29",
    "http://www.yidianzixun.com/channel/sc27",
    "http://www.yidianzixun.com/channel/sc32",
    "http://www.yidianzixun.com/channel/u1100",
    "http://www.yidianzixun.com/channel/u702",
    "http://www.yidianzixun.com/channel/t5448",
    "http://www.yidianzixun.com/channel/u9326",
    "http://www.yidianzixun.com/channel/e8771",
    "http://www.yidianzixun.com/channel/u7101",
    "http://www.yidianzixun.com/channel/sc31",
    "http://www.yidianzixun.com/channel/sc33",
    "http://www.yidianzixun.com/channel/u582",
    "http://www.yidianzixun.com/channel/u8065",
    "http://www.yidianzixun.com/channel/u8040",
    "http://www.yidianzixun.com/channel/u8062",
    "http://www.yidianzixun.com/channel/u9205",
    "http://www.yidianzixun.com/channel/u191",
    "http://www.yidianzixun.com/channel/t22927",
    "http://www.yidianzixun.com/channel/u1019",
    "http://www.yidianzixun.com/channel/u190",
    "http://www.yidianzixun.com/channel/u7720",
    "http://www.yidianzixun.com/channel/u195",
    "http://www.yidianzixun.com/channel/u8053",
    "http://www.yidianzixun.com/channel/t9233",
    "http://www.yidianzixun.com/channel/u8878",
    "http://www.yidianzixun.com/channel/u352",
    "http://www.yidianzixun.com/channel/t9239",
    "http://www.yidianzixun.com/channel/u8052",
    "http://www.yidianzixun.com/channel/u7599",
    "http://www.yidianzixun.com/channel/u9365",
    "http://www.yidianzixun.com/channel/u144",
    "http://www.yidianzixun.com/channel/u8305",
    "http://www.yidianzixun.com/channel/u7764",
    "http://www.yidianzixun.com/channel/e80535",
    "http://www.yidianzixun.com/channel/u139",
    "http://www.yidianzixun.com/channel/u8096",
    "http://www.yidianzixun.com/channel/u7762",
    "http://www.yidianzixun.com/channel/u448",
    "http://www.yidianzixun.com/channel/u7757",
    "http://www.yidianzixun.com/channel/u449",
    "http://www.yidianzixun.com/channel/u1055",
    "http://www.yidianzixun.com/channel/u1056",
    "http://www.yidianzixun.com/channel/u8084",
    "http://www.yidianzixun.com/channel/t9430",
    "http://www.yidianzixun.com/channel/u7877",
    "http://www.yidianzixun.com/channel/u9922",
    "http://www.yidianzixun.com/channel/u367",
    "http://www.yidianzixun.com/channel/t9432",
    "http://www.yidianzixun.com/channel/u1521",
    "http://www.yidianzixun.com/channel/t9431",
    "http://www.yidianzixun.com/channel/t2047",
    "http://www.yidianzixun.com/channel/u13685",
    "http://www.yidianzixun.com/channel/u1464",
    "http://www.yidianzixun.com/channel/u7882",
    "http://www.yidianzixun.com/channel/u6884",
    "http://www.yidianzixun.com/channel/e43080",
    "http://www.yidianzixun.com/channel/u5745",
    "http://www.yidianzixun.com/channel/t617",
    "http://www.yidianzixun.com/channel/u7058",
    "http://www.yidianzixun.com/channel/u1563",
    "http://www.yidianzixun.com/channel/b2873",
    "http://www.yidianzixun.com/channel/u11867",
    "http://www.yidianzixun.com/channel/u8800",
    "http://www.yidianzixun.com/channel/e20716",
    "http://www.yidianzixun.com/channel/u7621",
    "http://www.yidianzixun.com/channel/u7619",
    "http://www.yidianzixun.com/channel/u8269",
    "http://www.yidianzixun.com/channel/e428010",
    "http://www.yidianzixun.com/channel/e2090",
    "http://www.yidianzixun.com/channel/v25400",
    "http://www.yidianzixun.com/channel/u7580",
    "http://www.yidianzixun.com/channel/u7595",
    "http://www.yidianzixun.com/channel/e922",
    "http://www.yidianzixun.com/channel/e1661",
    "http://www.yidianzixun.com/channel/b16717",
    "http://www.yidianzixun.com/channel/u8570",
    "http://www.yidianzixun.com/channel/t9967",
    "http://www.yidianzixun.com/channel/b9514",
    "http://www.yidianzixun.com/channel/t19178",
    "http://www.yidianzixun.com/channel/u261",
    "http://www.yidianzixun.com/channel/u673",
    "http://www.yidianzixun.com/channel/t781",
    "http://www.yidianzixun.com/channel/u266",
    "http://www.yidianzixun.com/channel/u1569",
    "http://www.yidianzixun.com/channel/e39218",
    "http://www.yidianzixun.com/channel/u279",
    "http://www.yidianzixun.com/channel/u1776",
    "http://www.yidianzixun.com/channel/t10048",
    "http://www.yidianzixun.com/channel/t10045",
    "http://www.yidianzixun.com/channel/t19398",
    "http://www.yidianzixun.com/channel/u111",
    "http://www.yidianzixun.com/channel/u633",
    "http://www.yidianzixun.com/channel/u8187",
    "http://www.yidianzixun.com/channel/e212806",
    "http://www.yidianzixun.com/channel/t10449",
    "http://www.yidianzixun.com/channel/t9651",
    "http://www.yidianzixun.com/channel/u7916",
    "http://www.yidianzixun.com/channel/u9392",
    "http://www.yidianzixun.com/channel/u7934",
    "http://www.yidianzixun.com/channel/e1595662",
    "http://www.yidianzixun.com/channel/u7744",
    "http://www.yidianzixun.com/channel/e268214",
    "http://www.yidianzixun.com/channel/t19398",
    "http://www.yidianzixun.com/channel/u7699",
    "http://www.yidianzixun.com/channel/u7682",
    "http://www.yidianzixun.com/channel/t10447",
    "http://www.yidianzixun.com/channel/e932840",
    "http://www.yidianzixun.com/channel/u130",
    "http://www.yidianzixun.com/channel/u8038",
    "http://www.yidianzixun.com/channel/u0",
    "http://www.yidianzixun.com/channel/m1510009",
    "http://www.yidianzixun.com/channel/u7991",
    "http://www.yidianzixun.com/channel/t9438",
    "http://www.yidianzixun.com/channel/t1918",
    "http://www.yidianzixun.com/channel/u8867",
    "http://www.yidianzixun.com/channel/u669",
    "http://www.yidianzixun.com/channel/t1121",
    "http://www.yidianzixun.com/channel/u429",
    "http://www.yidianzixun.com/channel/u434",
    "http://www.yidianzixun.com/channel/t9490",
    "http://www.yidianzixun.com/channel/t9474",
    "http://www.yidianzixun.com/channel/u618",
    "http://www.yidianzixun.com/channel/u9608",
    "http://www.yidianzixun.com/channel/sc36",
    "http://www.yidianzixun.com/channel/e19695",
    "http://www.yidianzixun.com/channel/sc38",
    "http://www.yidianzixun.com/channel/t1111",
    "http://www.yidianzixun.com/channel/sc40",
    "http://www.yidianzixun.com/channel/u75",
    "http://www.yidianzixun.com/channel/u8339",
    "http://www.yidianzixun.com/channel/sc41",
    "http://www.yidianzixun.com/channel/sc42",
    "http://www.yidianzixun.com/channel/sc43",
    "http://www.yidianzixun.com/channel/sc44",
    "http://www.yidianzixun.com/channel/u8346",
    "http://www.yidianzixun.com/channel/u665",
    "http://www.yidianzixun.com/channel/u8347",
    "http://www.yidianzixun.com/channel/u306",
    "http://www.yidianzixun.com/channel/v33616",
    "http://www.yidianzixun.com/channel/u6838",
    "http://www.yidianzixun.com/channel/sc20",
    "http://www.yidianzixun.com/channel/c4",
    "http://www.yidianzixun.com/channel/sc19",
    "http://www.yidianzixun.com/channel/t587",
    "http://www.yidianzixun.com/channel/sc18",
    "http://www.yidianzixun.com/channel/u6751",
    "http://www.yidianzixun.com/channel/sc47",
    "http://www.yidianzixun.com/channel/sc45",
    "http://www.yidianzixun.com/channel/t1198",
    "http://www.yidianzixun.com/channel/t24880",
    "http://www.yidianzixun.com/channel/sc21",
    "http://www.yidianzixun.com/channel/u675",
    "http://www.yidianzixun.com/channel/u8283",
    "http://www.yidianzixun.com/channel/u59",
    "http://www.yidianzixun.com/channel/u0",
    "http://www.yidianzixun.com/channel/u310",
    "http://www.yidianzixun.com/channel/u309",
    "http://www.yidianzixun.com/channel/u576",
    "http://www.yidianzixun.com/channel/e84100",
    "http://www.yidianzixun.com/channel/u503",
    "http://www.yidianzixun.com/channel/u473",
    "http://www.yidianzixun.com/channel/u7496",
    "http://www.yidianzixun.com/channel/e171801",
    "http://www.yidianzixun.com/channel/u489",
    "http://www.yidianzixun.com/channel/u227",
    "http://www.yidianzixun.com/channel/u340",
    "http://www.yidianzixun.com/channel/sc4",
    "http://www.yidianzixun.com/channel/sc3",
    "http://www.yidianzixun.com/channel/u8291",
    "http://www.yidianzixun.com/channel/u8290",
    "http://www.yidianzixun.com/channel/e971462",
    "http://www.yidianzixun.com/channel/u7930",
    "http://www.yidianzixun.com/channel/t33",
    "http://www.yidianzixun.com/channel/t451",
    "http://www.yidianzixun.com/channel/t147",
    "http://www.yidianzixun.com/channel/t23",
    "http://www.yidianzixun.com/channel/u1424",
    "http://www.yidianzixun.com/channel/u8834",
    "http://www.yidianzixun.com/channel/sc8",
    "http://www.yidianzixun.com/channel/sc15",
    "http://www.yidianzixun.com/channel/sc5",
    "http://www.yidianzixun.com/channel/sc14",
    "http://www.yidianzixun.com/channel/sc11",
    "http://www.yidianzixun.com/channel/t77",
    "http://www.yidianzixun.com/channel/u1368",
    "http://www.yidianzixun.com/channel/u9668",
    "http://www.yidianzixun.com/channel/t822",
    "http://www.yidianzixun.com/channel/e76991",
    "http://www.yidianzixun.com/channel/e516316",
    "http://www.yidianzixun.com/channel/e67549",
    "http://www.yidianzixun.com/channel/u8505",
    "http://www.yidianzixun.com/channel/u8338",
    "http://www.yidianzixun.com/channel/u504",
    "http://www.yidianzixun.com/channel/u638",
    "http://www.yidianzixun.com/channel/u8522",
    "http://www.yidianzixun.com/channel/u8508",
    "http://www.yidianzixun.com/channel/u8519",
    "http://www.yidianzixun.com/channel/e75922",
    "http://www.yidianzixun.com/channel/u141",
    "http://www.yidianzixun.com/channel/u9384",
    "http://www.yidianzixun.com/channel/u575",
    "http://www.yidianzixun.com/channel/u9387",
    "http://www.yidianzixun.com/channel/u338",
    "http://www.yidianzixun.com/channel/e2654",
    "http://www.yidianzixun.com/channel/e288452",
    "http://www.yidianzixun.com/channel/e929007",
    "http://www.yidianzixun.com/channel/e158508",
    "http://www.yidianzixun.com/channel/t9436",
    "http://www.yidianzixun.com/channel/u655",
    "http://www.yidianzixun.com/channel/sc45",
    "http://www.yidianzixun.com/channel/sc47",
    "http://www.yidianzixun.com/channel/u8453",
    "http://www.yidianzixun.com/channel/u6874",
    "http://www.yidianzixun.com/channel/sc46",
    "http://www.yidianzixun.com/channel/t587",
    "http://www.yidianzixun.com/channel/t5650",
    "http://www.yidianzixun.com/channel/t1286",
    "http://www.yidianzixun.com/channel/u7114",
    "http://www.yidianzixun.com/channel/u704",
    "http://www.yidianzixun.com/channel/u8154",
    "http://www.yidianzixun.com/channel/u6721",
    "http://www.yidianzixun.com/channel/u421",
    "http://www.yidianzixun.com/channel/t296",
    "http://www.yidianzixun.com/channel/u11995",
    "http://www.yidianzixun.com/channel/u8570",
    "http://www.yidianzixun.com/channel/t1698",
    "http://www.yidianzixun.com/channel/sc35",
    "http://www.yidianzixun.com/channel/sc34",
    "http://www.yidianzixun.com/channel/u8563",
    "http://www.yidianzixun.com/channel/e390694",
    "http://www.yidianzixun.com/channel/e22618",
    "http://www.yidianzixun.com/channel/e614289",
    "http://www.yidianzixun.com/channel/e21969",
    "http://www.yidianzixun.com/channel/u420",
    "http://www.yidianzixun.com/channel/u659",
    "http://www.yidianzixun.com/channel/u464",
    "http://www.yidianzixun.com/channel/u1773",
    "http://www.yidianzixun.com/channel/u8099",
    "http://www.yidianzixun.com/channel/u256",
    "http://www.yidianzixun.com/channel/u5135",
    "http://www.yidianzixun.com/channel/u1395",
    "http://www.yidianzixun.com/channel/u1560",
    "http://www.yidianzixun.com/channel/u462",
    "http://www.yidianzixun.com/channel/u506",
    "http://www.yidianzixun.com/channel/u408",
    "http://www.yidianzixun.com/channel/e17369",
    "http://www.yidianzixun.com/channel/u590",
    "http://www.yidianzixun.com/channel/e80197",
    "http://www.yidianzixun.com/channel/u1776",
    "http://www.yidianzixun.com/channel/u111",
    "http://www.yidianzixun.com/channel/t587",
    "http://www.yidianzixun.com/channel/u511",
    "http://www.yidianzixun.com/channel/u224",
    "http://www.yidianzixun.com/channel/e21110",
    "http://www.yidianzixun.com/channel/u5203",
    "http://www.yidianzixun.com/channel/u11761",
    "http://www.yidianzixun.com/channel/u6615",
    "http://www.yidianzixun.com/channel/u10922",
    "http://www.yidianzixun.com/channel/u10925",
    "http://www.yidianzixun.com/channel/u10919",
    "http://www.yidianzixun.com/channel/u1637",
    "http://www.yidianzixun.com/channel/u480",
    "http://www.yidianzixun.com/channel/u11716",
    "http://www.yidianzixun.com/channel/u10871",
    "http://www.yidianzixun.com/channel/u8452",
    "http://www.yidianzixun.com/channel/u8444",
    "http://www.yidianzixun.com/channel/u1594"
]


def yidian_spider():
    driver = webdriver.PhantomJS()
    for url in author_urls:
        driver.get(url)
        time.sleep(1)
        try:
            uris = driver.find_elements_by_xpath("//div[@class='channel-news channel-news-0']/a")
        except:
            continue
        for uri in uris:
            item = {}
            try:
                driver.get(uri.get_attribute("href"))
                item['url'] = driver.current_url
                item['title'] = driver.find_element_by_xpath("//h2").text
                item['pubtime'] = driver.find_element_by_xpath("//div[@class='meta']/span[last()-1]").text
                item['content'] = driver.find_element_by_xpath("//div[@class='imedia-article']").text
                item['author'] = driver.find_element_by_xpath("//a[@class='doc-source']").text
                item['author_url'] = url
            except:
                continue
            item['site_name'] = u'一点号'
            md5 = hashlib.md5()
            md5.update(item["url"])
            item['url_md5'] = md5.hexdigest()
            item_fileds(item, "data_wemedia", False)

    driver.quit()


if __name__ == "__main__":
    yidian_spider()
