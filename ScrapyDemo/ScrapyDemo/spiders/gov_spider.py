#-*- coding:utf-8 -*-

import scrapy
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from ScrapyDemo.items import GovSpiderItem


class GovSpider(scrapy.Spider):
    name = 'gov'

    url = "http://www.sse.com.cn/assortment/stock/list/share/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }

    driver = webdriver.Chrome('/Users/luozhongjin/ScrapyDemo/ScrapyDemo/chromedriver')
    driver.implicitly_wait(10)

    def start_requests(self):
        yield scrapy.Request(url = self.url, headers = self.headers,callback = self.parse);

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)
        i = 1
        while True:
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            trs = soup.findAll("tr")
            for tr in trs:
                try:
                    tds = tr.findAll("td")
                    print tds
                    item = GovSpiderItem()
                    item["name"] = tds[1].string
                    yield item
                except:
                    pass
            try:
                next_page = self.driver.find_element_by_class_name("glyphicon-menu-right").click()
                i = i + 1
                if i >= 55:
                    break
            except:
                break

            time.sleep(5)


