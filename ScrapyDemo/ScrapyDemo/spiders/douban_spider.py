# encoding: utf-8

import scrapy
from ScrapyDemo.items import DoubanSpiderItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DoubanSpider(scrapy.Spider):
    name = 'douban'

    url = 'https://www.douban.com/people/163296676/rev_contacts?start=0'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    cookies = {
        # '_pk_ses.100001.8cb4': '*',
        # '_pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1506597166%2C%22https%3A%2F%2Faccounts.douban.com%2Flogin%3Falias%3D192088480%2540qq.com%26redir%3Dhttps%253A%252F%252Fwww.douban.com%252Fpeople%252F163296676%252Frev_contacts%26source%3DNone%26error%3D1013%22%5D',
        # '_pk_id.100001.8cb4': '593f1b1f2e08602e.1506597166.1.1506597191.1506597166.',
        'bid': 'dRd7NLw5Ixc',
        'ck': 'fnHW',
        'dbcl2': '"167308455:BugVWMxdWso"',
        'push_doumail_num': '0',
        'push_noty_num': '0',
        'ue': '"192088480@qq.com"',
        # '__utma': '30149280.1153167920.1506597166.1506597166.1506597166.1',
        # '__utmb': '30149280.10.10.1506597166',
        # '__utmc': '30149280',
        # '__utmt': '1',
        # '__utmv': '30149280.16730',
        # '__utmz': '30149280.1506597166.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login'
    }

    def start_requests(self):

        yield scrapy.Request(url=self.url,headers=self.headers,cookies=self.cookies,callback=self.parse)

    def parse(self, response):
        for index in response.xpath("//dl[@class='obu']"):
            item = DoubanSpiderItem()
            item['name'] = str(index.xpath(".//img/attribute::alt").extract_first())
            item['image'] = index.xpath(".//img/attribute::src").extract_first()
            item['href'] = index.xpath(".//a/attribute::href").extract_first()
            yield item

            next_page = response.xpath("//span[@class='next']/a/attribute::href").extract_first()
            if next_page is not None:
                yield response.follow(url=next_page.encode("ascii"),headers=self.headers,cookies=self.cookies,callback=self.parse)