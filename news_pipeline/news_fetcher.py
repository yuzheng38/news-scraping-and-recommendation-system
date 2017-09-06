import newspaper
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

DEDUPE_NEWS_QUEUE_URL = 'amqp://ceunvrpr:UDzmDHCEafFYRnasgapNP6qaSHMik-1i@crane.rmq.cloudamqp.com/ceunvrpr'
DEDUPE_NEWS_QUEUE_NAME = 'tap-news-dedupe-news-task-queue'
SCRAPE_NEWS_QUEUE_URL = 'amqp://ceunvrpr:UDzmDHCEafFYRnasgapNP6qaSHMik-1i@crane.rmq.cloudamqp.com/ceunvrpr'
SCRAPE_NEWS_QUEUE_NAME = 'tap-news-scrape-news-task-queue'
SLEEP_TIMEOUT_IN_SECONDS = 5

import cnn_news_scraper    # can use this or the newspaper library
from cloudAMQP_client import CloudAMQPClient

scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_QUEUE_URL, SCRAPE_NEWS_QUEUE_NAME)
dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_QUEUE_URL, DEDUPE_NEWS_QUEUE_NAME)

def handleMessage(msg):
    if msg is None or not isinstance(msg, dict):
        print 'received a broken message'
        return

    task = msg
    text = None

    # if task['source'] == 'cnn':
    #     print 'scraping news from cnn'
    #     text = cnn_news_scraper.extract_news(task['url'])
    # else:
    #     print 'news source [%s] is not supported' % task['source']
    
    article = newspaper.Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text.encode('utf-8')
    dedupe_news_queue_client.sendMessage(task)

""" fetch news from rabbitAMQP scrape news queue, add news text, then send to dedupe news queue"""
while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            try:
                handleMessage(msg)
            except Exception:
                print 'message has an invalid encoding' # coding utf-8
                pass
        scrape_news_queue_client.sleep(SLEEP_TIMEOUT_IN_SECONDS)