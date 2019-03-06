import scrapy
import json
from scrapy.http import Request
from scrapy_redis.spiders import RedisCrawlSpider


class QuotesSpider(scrapy.Spider):
    name = "flipkart_lv"
    custom_settings = {
        'SCHEDULER_PERSIST' : True,
        'SCHEDULER_FLUSH_ON_START' : False,
        'ITEM_PIPELINES': {
            'first.pipelines.CustomizedRedisPipeline': 100,
            'first.pipelines.JsonWriterPipeline':200
            # 'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 500,

        },'REDIS_ITEMS_KEY' : name }
    start_urls = [
        'https://www.flipkart.com/men/tshirts/pr?sid=2oq%2Cs9b%2Cj9y&otracker=nmenu_sub_Men_0_T-Shirts&page=1'
    ]
    # def start_requests(self):
    #     urls = [
    #         'https://www.flipkart.com/men/tshirts/pr?sid=2oq%2Cs9b%2Cj9y&otracker=nmenu_sub_Men_0_T-Shirts&page=1'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        yields = []

        item = {}
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.json' % page

        urls=response.xpath('//a[@class="_3dqZjq"]/@href').extract()

        if(len(urls) !=0 ):
            #add code to change page here
            for url in urls:
                yields.append({"url":"https://www.flipkart.com"+url})
            current_request_url = str(response.request.url)
            print('***********')
            print(current_request_url)
            print('***********')
            temp=current_request_url.split('&page=')
            print(temp)
            current_offset = int(temp[1].strip())
            next_offset = current_offset + 1
            next_req_url = temp[0] +'&page='+ str(next_offset)
            print(next_req_url)
            # yields = yields + urls
            next_req = Request(next_req_url, callback=self.parse)
            yields.append(next_req)

        return yields
