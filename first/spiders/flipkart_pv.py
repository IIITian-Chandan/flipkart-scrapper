import scrapy
import json
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider
import pymongo

class QuotesSpider(RedisSpider):
    name = "flipkart_pv"
    custom_settings = {
        'SCHEDULER_PERSIST' : True,
        'SCHEDULER_FLUSH_ON_START' : False,
        'ITEM_PIPELINES': {
                'first.pipelines.JsonWriterPipeline': 300,
                'scrapy_mongodb.MongoDBPipeline':200,
                'scrapy_redis.pipelines.RedisPipeline': 100,
        },
        'REDIS_START_URLS_KEY' : "flipkart_lv",
        'MONGODB_COLLECTION':name

    }

#    def start_requests(self):
#        urls = [
#            'https://www.flipkart.com/elepants-solid-men-s-hooded-black-t-shirt/p/itmf3ysunprevkec?pid=TSHEPZFZ9PREF7AF&lid=LSTTSHEPZFZ9PREF7AFGKXKXQ&marketplace=FLIPKART&srno=b_1_1&otracker=nmenu_sub_Men_0_T-Shirts&fm=organic&iid=11ebba95-e728-4e88-80b9-3f5a783c19d5.TSHEPZFZ9PREF7AF.SEARCH&ppt=StoreBrowse&ppn=Store'
#        ]
#        for url in urls:
#            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = {}
        page = response.url.split("/")[-2]
        print(str(response))
        print("++++++++++++++++++++++++++++++++++++=")

        path=response.xpath('//div[@class="_1joEet"]/div[@class="_1HEvv0"]/a[@class="_1KHd47"]/text()').extract()
        path='-'.join(path)

        title=response.xpath('//h1[@class="_9E25nV"]/span[@class="_2J4LW6"]/text()').extract()[0]
        name=response.xpath('//h1[@class="_9E25nV"]/span[@class="_35KyD6"]/text()').extract()[0].strip()
        print(path)
        print(title)
        print(name)

        # total=path + '\n'+title+'\n'+name
        item["name"] = name
        item["title"] = title
        item["path"] = path
        print(item)
        print("++++++++++++++++++++++++++++++++++++=")

        yield item
