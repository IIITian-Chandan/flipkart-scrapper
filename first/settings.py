# -*- coding: utf-8 -*-

# Scrapy settings for first project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'first'

SPIDER_MODULES = ['first.spiders']
NEWSPIDER_MODULE = 'first.spiders'

MONGO_URI = "mongodb://root:example@mongodb-dev.greendeck.co:27017/admin"
MONGO_DATABASE = 'flipkart'
#++++++++++++++++++++++++++++Redis part start
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"


# The item pipeline serializes and stores the items in this redis key.
REDIS_ITEMS_KEY = '%(spider)s:items'

# The items serializer is by default ScrapyJSONEncoder. You can use any
# importable path to a callable object.
REDIS_URL = "redis://mongodb-dev.greendeck.co:6379"

# Use other encoding than utf-8 for redis.
REDIS_ENCODING = 'latin1'

# Default start urls key for RedisSpider and RedisCrawlSpider.
#REDIS_START_URLS_KEY = '%(name)s:start_urls'


#+++++++++++++++++++++++++++++Redis part End
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'first (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


CONCURRENT_REQUESTS = 1000
CONCURRENT_ITEMS = 1000
CONCURRENT_REQUESTS_PER_IP = 1000
#Proxies and UserAgents
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620
}



#-----------------------------------------------For getting list of proxies
from first.proxy_checker import *
import asyncio
from proxybroker import Broker

#Using Proxibreaker to get list of proxies
# proxy_list=[]
#
# async def save(proxies):
#     while True:
#         proxy = await proxies.get()
#         if proxy is None:
#             break
#         proto = 'https' if 'HTTPS' in proxy.types else 'http'
#         proxy_list.append('%s:%d' % ( proxy.host, proxy.port))
#
# proxies = asyncio.Queue()
# broker = Broker(proxies)
# tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], limit=1000),
#                        save(proxies))
# loop = asyncio.get_event_loop()
# loop.run_until_complete(tasks)
# print(len(proxy_list))
# print(proxy_list)
proxy_grabber = ProxyGraberClass(10)
get_proxies = proxy_grabber.p_list()
print(get_proxies)

proxy_checker = ProxyChecker(get_proxies, threads=50, verbose=False, timeout=1)
outlist = proxy_checker.start()
print(len(outlist))
print(outlist)
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
ROTATING_PROXY_LIST= outlist
LOG_ENABLED=False

#----------------------------------------------------End of getting proxies code


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'first.middlewares.FirstSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'first.middlewares.FirstDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'first.pipelines.FirstPipeline': 300,
#}



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
