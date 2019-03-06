# Sample Python program that uses Redis-py to connect to a Redis Server

import redis



# Create a redis client

redisClient = redis.StrictRedis(host='mongodb-dev.greendeck.co',

                                port=6379,

                                db=0)


keys = redisClient.lrange('flipkart_lv:items',0,30)
#for i in keys:
#    print(i)
print(redisClient.llen('flipkart_lv:items'))
# Get the new value of the key and print it
