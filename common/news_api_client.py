import json
import requests

NEWS_API_ENDPOINT = 'https://newsapi.org/v1/'
NEWS_API_KEY = '538bed6d89214f48ac9808597bad6067'

ARTICLES_API = 'articles'
SOURCES_API = 'sources'  # for future use

DEFAULT_SOURCES = [
    'cnn'
    ]
DEFAULT_SORT_BY = 'top'

def buildUrl(endPoint=NEWS_API_ENDPOINT, apiName=ARTICLES_API):
    return endPoint + apiName

def getNewsFromSources(sources=DEFAULT_SOURCES, sortBy=DEFAULT_SORT_BY):
    articles = []

    for source in sources:
        payload = {
            'apiKey': NEWS_API_KEY,
            'source': source,
            'sortBy': sortBy
        }
        response = requests.get(buildUrl(), params=payload)
        res_json = json.loads(response.content)

        # Extract information from response
        if (res_json is not None and 
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # Populate news source in each article
            for article in res_json['articles']:
                article['source'] = res_json['source']

            articles.extend(res_json['articles'])   # not append coz articles will then become a list of list

    return articles