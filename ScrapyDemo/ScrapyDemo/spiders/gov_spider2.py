#-*- coding:utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# 显式等待
class GovSpider2(scrapy.Spider):
    name = 'gov2'

    url = "http://www.sse.com.cn/assortment/stock/list/share/"

    driver = webdriver.Chrome()
    driver.set_window_size(1124, 850)

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        i = 1
        current_max = 0

        self.driver.get(response.url)
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.execute_script('return document.getElementsByTagName("td").length > 0;'))

        while True:
            print type(self.driver.page_source)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            trs = soup.findAll("tr")
            for tr in trs:
                try:
                    tds = tr.findAll("td")
                    stock_id = int(tds[0].string)
                    current_max = max(current_max, stock_id)
                    yield {
                        'page_num': i,
                        'name': tds[1].string,
                    }
                except:
                    pass
            try:
                self.driver.find_element_by_class_name("glyphicon-menu-right").click()

                js_condition_tpl = 'return {} < parseInt(document.getElementsByTagName("td")[0].children[0].text);'
                WebDriverWait(self.driver, 10).until(
                    lambda driver: self.driver.execute_script(js_condition_tpl.format(current_max)))

                i = i + 1
                if i >= 55:
                    break
            except:
                break