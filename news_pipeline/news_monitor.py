import datetime
import hashlib
import os
import redis
import sys
# sys module is a runtime module. it provides access to vars/funcs used by the python interpreter.
# sys.path is ~ pythonpath + installation dependent defaults
# by default sys.path[0] is the cur dir. thus append.
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))    
import news_api_client
from cloudAMQP_client import CloudAMQPClient

NEWS_SOURCES = [
                'bbc-news',
                'bbc-sport',
                'bloomberg',
                'cnn',
                'espn',
                'financial-times',
                'fortune',
                'fox-news',
                'national-geographic',
                'techcrunch',
                'the-new-york-times',
                'the-washington-post',
                'the-wall-street-journal',
                'usa-today'
                ]

# redis params
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
NEWS_TIMEOUT_IN_SECONDS = 3600 * 24 * 3
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

# cloudAMQP params
CLOUDAMQP_SLEEP_TIMEOUT_IN_SECONDS = 10
CLOUDAMQP_NEWS_SCRAPER_QUEUE_URL = 'amqp://ceunvrpr:UDzmDHCEafFYRnasgapNP6qaSHMik-1i@crane.rmq.cloudamqp.com/ceunvrpr'
CLOUDAMQP_NEWS_SCRAPER_QUEUE_NAME = 'tap-news-scrape-news-task-queue'
cloudAMQP_client = CloudAMQPClient(CLOUDAMQP_NEWS_SCRAPER_QUEUE_URL, CLOUDAMQP_NEWS_SCRAPER_QUEUE_NAME)

while True:
    news_list = news_api_client.getNewsFromSources(NEWS_SOURCES)

    num_of_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            news['digest'] = news_digest
            num_of_news += 1

            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, 'True')
            redis_client.expire(news_digest, NEWS_TIMEOUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)
    
    print '[x] Fetched %d news in news_monitor' % (num_of_news)

    cloudAMQP_client.sleep(CLOUDAMQP_SLEEP_TIMEOUT_IN_SECONDS)