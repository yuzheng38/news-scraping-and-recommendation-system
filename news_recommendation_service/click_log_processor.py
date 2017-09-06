# -*- coding: utf-8 -*-
import news_classes
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

# time decay model related constants
NUM_OF_CLASSES = 17
INITIAL_P = 1.0 / NUM_OF_CLASSES
ALPHA = 0.1

# mongo db related constants
SLEEP_TIME_IN_SECONDS = 1
PREFERENCE_MODEL_TABLE_NAME = 'user_preference_model'
NEWS_TABLE_NAME = 'news'

# cloud amqp related constants/vars
LOG_CLICK_TASK_QUEUE_URL = 'amqp://ceunvrpr:UDzmDHCEafFYRnasgapNP6qaSHMik-1i@crane.rmq.cloudamqp.com/ceunvrpr'
LOG_CLICK_TASK_QUEUE_NAME = 'tap-news-click-log-task-queue'
cloudAMQP_client = CloudAMQPClient(LOG_CLICK_TASK_QUEUE_URL, LOG_CLICK_TASK_QUEUE_NAME)

def handleMessage(msg):
    if msg is None or not isinstance(msg, dict):
        return

    if ('userId' not in msg or
        'newsId' not in msg or
        'timestamp' not in msg):
        return
    
    userId = msg['userId']
    newsId = msg['newsId']

    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    if model is None:
        print 'Creating new preference model for new user: %s' % userId
        new_model = {'userId': userId}
        preference = {}
        for i in news_classes.classes:
            preference[i] = float(INITIAL_P)
        new_model['preference'] = preference
        model = new_model
    
    print 'Updating preference model for user: %s' % userId

    # retrieve class of the clicked news
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if (news is None or
        'class' not in news or
        news['class'] not in news_classes.classes):
        print news is None
        print 'class' not in news
        print news['class'] not in news_classes.classes
        print 'Skiped processing...'
        return

    click_class = news['class']

    # update the time decay model
    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    for i, prob in model['preference'].iteritems():
        if not i == click_class:
            model['preference'][i] = float((1 - ALPHA) * model['preference'][i])

    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                try:
                    handleMessage(msg)
                except Exception as e:
                    print e
                    pass
            
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    run()