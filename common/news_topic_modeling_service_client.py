import pyjsonrpc

URL = 'http://localhost:6060'

client = pyjsonrpc.HttpClient(URL)

def classify(text):
    topic = client.call('classify', text)
    print 'Topic: %s' % str(topic)
    return topic