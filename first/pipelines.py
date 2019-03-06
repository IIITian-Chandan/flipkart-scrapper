# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from datetime import datetime
from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread

from scrapy_redis import connection, defaults
from scrapy_redis.pipelines import RedisPipeline

from io import BytesIO
from urllib.parse import urlparse
import gzip
import os
import boto3
from botocore.exceptions import ClientError

from scrapy.exporters import JsonLinesItemExporter
import concurrent.futures
import threading

def json2url(js):
    return js["url"]

default_serialize = json2url

class CustomizedRedisPipeline(RedisPipeline):
    def __init__(self, server,
                 key=defaults.PIPELINE_KEY,
                 serialize_func=default_serialize):
        self.server = server
        self.key = key
        self.serialize = serialize_func


class FirstPipeline(object):
    def process_item(self, item, spider):
        return item
import json



class JsonWriterPipeline(object):

    def open_spider(self, spider):
        print('=============================================')
        print(spider)
        print('=============================================')
        self.file = open(spider.name+'_items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


import pymongo

# class MongoPipeline(object):
#
#     collection_name = 'scrapy_items'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert_one(dict(item))
#         return item
