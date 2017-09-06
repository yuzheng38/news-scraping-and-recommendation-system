from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://ceunvrpr:UDzmDHCEafFYRnasgapNP6qaSHMik-1i@crane.rmq.cloudamqp.com/ceunvrpr'
TEST_QUEUE_NAME = 'coj_queue'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)
    
    sentMsg = {"test":"test message body"}
    client.sendMessage(sentMsg)
    receivedMsg = client.getMessage()
    
    assert sentMsg == receivedMsg
    print 'test_basic passed'

if __name__ == '__main__':
    test_basic()