# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DoubanSpiderItem(scrapy.Item):
    name = scrapy.Field()
    image = scrapy.Field()
    href = scrapy.Field()

class GovSpiderItem(scrapy.Item):
    name = scrapy.Field()