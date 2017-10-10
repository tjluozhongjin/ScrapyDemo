import scrapy
import json

import time

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy_splash import SplashRequest


class GovSpider3(scrapy.Spider):
    name = 'gov3'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }
    start_urls = ['http://www.sse.com.cn/assortment/stock/list/share/']

    def start_requests(self):
        script = """
        treat = require("treat")
        function main(splash, args)
          assert(splash:go(args.url))
          local tbl = {}
          for i=1,5,1 do
            splash:wait(3.0)
            tbl[i] = splash:html()
            splash:select('.glyphicon.glyphicon-menu-right'):mouse_click()
            end
          return treat.as_array(tbl)
        end
        """

        # function main(splash, args)
        #     assert(splash:go(args.url))
        #     splash:select('.next'):mouse_click()
        #     splash:wait(5.0)
        #     return splash:html()
        # end

        for url in self.start_urls:
            yield SplashRequest(url=url,headers=self.headers, callback=self.parse,endpoint='execute',
                            args={'lua_source': script})

    def parse(self, response):
        #splash_json = json.loads(response.body_as_unicode())

        for i in range(0,5):
            print type(response.data[i])

            soup = BeautifulSoup(response.data[i], 'lxml')
            trs = soup.findAll("tr")
            for tr in trs:
                try:
                    tds = tr.findAll("td")
                    yield {
                        "name":tds[1].string
                    }
                except:
                    pass
