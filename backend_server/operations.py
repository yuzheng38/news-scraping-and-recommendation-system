import json
import os
import pickle 
import redis
import sys

from bson.json_util import dumps
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import recommendation_service_client

from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

NEWS_TABLE_NAME = 'news'
LOGS_TABLE_NAME = 'news_click_logs'

LOG_CLICK_TASK_QUEUE_URL = 'amqp://ceunvrpr:UDzmDHCEafFYRnasgapNP6qaSHMik-1i@crane.rmq.cloudamqp.com/ceunvrpr'
LOG_CLICK_TASK_QUEUE_NAME = 'tap-news-click-log-task-queue'
cloudAMQP_client = CloudAMQPClient(LOG_CLICK_TASK_QUEUE_URL, LOG_CLICK_TASK_QUEUE_NAME)

NEWS_LIST_BATCH_SIZE = 10
TOTAL_NEWS_LIMIT = 100
TOTAL_NEWS_EXPIRATION_IN_SECONDS = 60

def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num) # cast
    beginning_news_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    ending_news_index = page_num * NEWS_LIST_BATCH_SIZE

    sliced_news = []

    db = mongodb_client.get_db()

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))  # redis only stores digests

        sliced_news_digests = news_digests[beginning_news_index: ending_news_index]
        # print sliced_news_digests
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': { '$in': sliced_news_digests}}))
    else:
        all_news = list(db[NEWS_TABLE_NAME].find().limit(TOTAL_NEWS_LIMIT).sort([('publishedAt', -1)]))
        all_news_digests = map(lambda x:x['digest'], all_news)
        
        redis_client.set(user_id, pickle.dumps(all_news_digests))
        redis_client.expire(user_id, TOTAL_NEWS_EXPIRATION_IN_SECONDS)

        sliced_news = all_news[beginning_news_index: ending_news_index]

    preference = recommendation_service_client.getPreferenceForUser(user_id)
    top_preference = None

    if preference is not None and len(preference) > 0:
        top_preference = preference[0]

    # update labels according to time, recommendation
    for news in sliced_news:
        del news['text'] # to save bandwidth.
        if news['class'] == top_preference:
            news['reason'] = 'recommend'
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'

    return json.loads(dumps(sliced_news))    # serializes then loads into json

def logNewsClickForUser(user_id, news_id):
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': datetime.utcnow()}

    db = mongodb_client.get_db()
    db[LOGS_TABLE_NAME].insert(message)

    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    cloudAMQP_client.sendMessage(message)