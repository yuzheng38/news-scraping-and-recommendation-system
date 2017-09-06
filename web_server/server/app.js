var bodyParser = require('body-parser');
var config = require('./config/config.json');
var cors = require('cors');
var express = require('express');
var passport = require('passport');
var path = require('path');

var auth = require('./routes/auth');
var index = require('./routes/index');
var news = require('./routes/news');

var app = express();

require('./models/main.js').connect(config.mongoDbUri);

// view engine setup  // what is view engine?
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

// app.all('*', function(req, res, next) {
//   res.header('Access-Control-Allow-Origin', '*');
//   res.header('Access-Control-Allow-Headers', 'X-Requested-with');
//   next();
// });

// Load passport strategies
app.use(passport.initialize());
var localSignupStrategy = require('./passports/signup_passport');
var localLoginStrategy = require('./passports/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

app.use(cors());  // third party middleware to handle cors

app.use(bodyParser.json());
app.use('/', index);
app.use('/auth', auth);
const authCheckerMiddleware = require('./middleware/auth_checker');
app.use('/news', authCheckerMiddleware);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res) {
  var err = new Error('Not Found');
  err.status = 404;
  res.send('404 Not Found from app.js');
});

module.exports = app;
