var client = require('./rpc_client');

client.add(100, 15, function(response){
    console.assert(response === 115);
});

client.getNewsSummariesForUser('test_user', 1, function(response) {
    console.assert(response != null);
});

client.logNewsClickForUser('test_user', 'test_news');