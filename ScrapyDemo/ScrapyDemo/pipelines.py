# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import redis


class ScrapydemoPipeline(object):
    def __init__(self):
        self.file = open('items.c', 'wb')
        self.r = redis.StrictRedis(host='118.89.162.132', port=6379, db=0)

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        self.r.lpush("douban",item)
        return item
