// const NEWS = require('./mock');
var router = require('express').Router();
var rpc_client = require('../rpc_client/rpc_client');

/* Get news summary list */
router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next){
    console.log("fetching news .. ");
    user_id = req.params['userId'];
    page_num = req.params['pageNum'];

    rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {
        res.json(response); // route directly to client. 
    });
});

/** Log user click event */
router.post('/userId/:userId/newsId/:newsId', function(req, res, next) {
    user_id = req.params['userId'];
    news_id = req.params['newsId'];

    rpc_client.logNewsClickForUser(user_id, news_id);
    res.status(200);
});

module.exports = router;