import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client
import news_topic_modeling_service_client
from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_QUEUE_URL = 'amqp://ceunvrpr:UDzmDHCEafFYRnasgapNP6qaSHMik-1i@crane.rmq.cloudamqp.com/ceunvrpr'
DEDUPE_NEWS_QUEUE_NAME = 'tap-news-dedupe-news-task-queue'
SLEEP_TIMEOUT_IN_SECONDS = 5
MONGODB_TABLE_NAME = 'tap-news'

SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

dedupe_queue_client = CloudAMQPClient(DEDUPE_NEWS_QUEUE_URL, DEDUPE_NEWS_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return
    task = msg
    text = task['text']
    if text is None:
        return
    
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    same_day_news_list = list(db[MONGODB_TABLE_NAME].find(
                        {'publishedAt': {'$gte': published_at_day_begin,
                                         '$lt': published_at_day_end}}))
    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['text'] for news in same_day_news_list]
        documents.insert(0, text)

        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T 

        print pairwise_sim

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print 'duplicate news. ignore'
                return
    
    task['publishedAt'] = parser.parse(task['publishedAt'])

    # classify new news as it's being deduped. 
    if task['description'] is None:
        task['description'] = task['title']
    
    if task['title'] is not None: 
        topic = news_topic_modeling_service_client.classify(task['description'])
        task['class'] = topic

    db[MONGODB_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if dedupe_queue_client is not None:
        msg = dedupe_queue_client.getMessage()
        if msg is not None:
            # parse and proceed with task
            try:
                handle_message(msg)
            except Exception as e:
                print 'error while handling message in deduper: %s' % e
                pass
        
        dedupe_queue_client.sleep(SLEEP_TIMEOUT_IN_SECONDS)