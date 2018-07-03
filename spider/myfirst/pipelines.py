# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
import logging
import re


# class MyfirstPipeline(object):
#     def process_item(self, item, spider):
#         return item


class MongoDBPipeline(object):

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'], settings['MONGODB_PORT'])

        self.db = self.connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        print('***********************************************************************************************************************************************************************')
        # print(item)
        # aaaa = re.sub(r'(\n)|(\r)', ' ', item['desc']
        # print(aaaa)
        self.collection.insert(dict(item))
        # logging.dubug(' added to mongodb database!', level=logging.DEBUG)
        return item
