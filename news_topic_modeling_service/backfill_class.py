import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

if __name__ == '__main__':
    db = mongodb_client.get_db()
    cursor = db['news'].find({})    # cursor is the returned news list
    count = 0
    for news in cursor:
        count += 1
        print count
        if 'class' not in news:
            print 'Populating class'
            description = news['description']
            if description is None:
                news['description'] = news['title']

            topic = news_topic_modeling_service_client.classify(description)
            news['class'] = topic
            db['news'].replace_one({'digest': news['digest']}, news, upsert=True)