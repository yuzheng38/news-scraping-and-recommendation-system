import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import news_api_client

from cloudAMQP_client import CloudAMQPClient
# cloudAMQP params
CLOUDAMQP_NEWS_SCRAPER_QUEUE_URL = 'amqp://ceunvrpr:UDzmDHCEafFYRnasgapNP6qaSHMik-1i@crane.rmq.cloudamqp.com/ceunvrpr'
CLOUDAMQP_NEWS_SCRAPER_QUEUE_NAME = 'tap-news-scrape-news-task-queue'

CLOUDAMQP_NEWS_DEDUP_QUEUE_URL = ''
CLOUDAMQP_NEWS_DEDUP_QUEUE_NAME = ''

def purgeQueue(queue_url, queue_name):
    cloudAMQP_client = CloudAMQPClient(queue_url, queue_name)
    num_of_messages_cleared = 0

    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is None:
                print 'Cleared %d messages' % num_of_messages_cleared
                return
            num_of_messages_cleared += 1


if __name__ == '__main__':
    purgeQueue(CLOUDAMQP_NEWS_SCRAPER_QUEUE_URL, CLOUDAMQP_NEWS_SCRAPER_QUEUE_NAME)
    # purgeQueue(CLOUDAMQP_NEWS_DEDUP_QUEUE_URL, CLOUDAMQP_NEWS_DEDUP_QUEUE_NAME)