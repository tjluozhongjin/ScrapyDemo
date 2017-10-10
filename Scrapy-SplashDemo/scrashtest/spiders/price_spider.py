#-*- coding:utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import Spider, logging
from scrapy.selector import Selector
import urlparse, random

from scrapy_splash import SplashRequest


class Price_Spider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = [
        "https://item.jd.com/5005731.html"
    ]

    def start_requests(self):
        splash_args = {
            'wait': 0.5,
        }
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_result)

    def parse_result(self, response):
        logging.info(u'----------使用splash爬取京东网首页异步加载内容-----------')
        guessyou = response.xpath('//span[@class="p-price"]/span')[1].xpath("./text()").extract_first()
        print guessyou
        logging.info(u"find：%s" % guessyou)
        logging.info(u'---------------success----------------')