import mongodb_client as client

def test_basic():
    db = client.get_db('tap-news')
    db.testCollection.drop()
    assert db.testCollection.count() == 0
    db.testCollection.insert({'one': 1})
    assert db.testCollection.count() == 1
    db.testCollection.drop()
    assert db.testCollection.count() == 0
    print 'test basic passed.'

if __name__ == '__main__':
    test_basic()