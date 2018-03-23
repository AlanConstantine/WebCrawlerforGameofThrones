# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-03-22 23:43:35
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
import pymongo
import logging
from GOTspider.items import GotspiderItem
import GOTspider.settings as settings


class RedisPipeline(object):
    def __init__(self):
        self.redis_table = settings.MY_REDIS  # 选择表
        self.redis_db = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)  # redis数据库连接信息

    def process_item(self, item, spider):
        if self.redis_db.exists(item['url']):
            raise DropItem('%s id exists!!' % (item['url']))
        else:
            self.redis_db.lpush(self.redis_table, item['url'])
        return item


class GotspiderPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["GameofThrones"]
        self.got = db["roles"]

    def process_item(self, item, spider):
        if isinstance(item, GotspiderItem):
            try:
                self.got.insert(dict(item))
                logging.info("Question added to MongoDB database!")
            except Exception as e:
                raise e
        return item
