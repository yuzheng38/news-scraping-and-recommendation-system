var jayson = require('jayson');

// Create a rpc node client to connect to python rpc service
var client = jayson.client.http({
    port: 4040,
    hostname: 'localhost'
});

// Test RPC method
function add(a, b, callback){
    client.request('add', [a, b], function(err, error, response) {
        if(err) throw err;
        console.log(response);
        callback(response);
    });
}

// Get news summaries for a user
function getNewsSummariesForUser(user_id, pageNum, callback){
    client.request('getNewsSummariesForUser', [user_id, pageNum], function(err, error, response) {
        if(err) throw err;
        console.log(response, ' in server/rpc_client');
        callback(response);
    });
}

// Register click event for a user
function logNewsClickForUser(user_id, news_id) {
    client.request('getNewsClickForUser', [user_id, news_id], function(err, error, response) {
        if (err) throw err;
        console.log(response);
    });
}

module.exports = {
    add: add,
    getNewsSummariesForUser: getNewsSummariesForUser,
    logNewsClickForUser: logNewsClickForUser
};
