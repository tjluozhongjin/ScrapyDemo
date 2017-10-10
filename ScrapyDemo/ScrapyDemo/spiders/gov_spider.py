#-*- coding:utf-8 -*-

import contextlib
import scrapy
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from ScrapyDemo.items import GovSpiderItem

# 隐式等待
class GovSpider(scrapy.Spider):
    name = 'gov'

    url = "http://www.sse.com.cn/assortment/stock/list/share/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }

    driver = webdriver.PhantomJS('/Users/luozhongjin/ScrapyDemo/ScrapyDemo/phantomjs')
    # driver = webdriver.Chrome('/Users/luozhongjin/ScrapyDemo/ScrapyDemo/chromedriver')
    driver.implicitly_wait(15)

    def start_requests(self):
        yield scrapy.Request(url = self.url, headers = self.headers,callback = self.parse);

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.set_window_size(1124, 850)
        i = 1
        time.sleep(3)
        while True:
            # 发现采用BeautifulSoup后，隐式的等待是无效的
            print type(self.driver.page_source)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            trs = soup.findAll("tr")
            for tr in trs:
                try:
                    tds = tr.findAll("td")
                    print tds
                    item = GovSpiderItem()
                    item["name"] = tds[1].string
                    #print ("ok")
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

            # WebDriverWait(self.driver, 10).until(self.ajax_complete)
            #WebDriverWait(self.driver, 10).until(lambda driver: self.driver.execute_script("return jQuery.active == 0"))
            time.sleep(3)