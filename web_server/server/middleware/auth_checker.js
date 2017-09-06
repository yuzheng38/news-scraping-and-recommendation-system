const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config/config.json');

module.exports = (req, res, next) => {
    console.log('auth_checker: req: ' + req.headers);
    console.log('auth_checker: req auth: ' + req.headers.authorization);

    // if no authorization (i.e. token) send 401 and end stream
    if (!req.headers.authorization) {
        return res.status(401).end();
    }

    // header authorization string eg-- authorization token-value
    const token = req.headers.authorization.split(' ')[1];
    console.log('auth_checker: token: ' + token);

    // decode the token using a secret key-phrase
    return jwt.verify(token, config.jwtSecret, (err, decoded) => {
        if (err) { return res.status(401).end(); }

        const email = decoded.sub;  // sub is a jwt function to get at the subject of jwt string

        return User.findById(email, (userError, user) => {
            if (userError || !user) {
                return res.status(401).end();
            }
            return next();
        });
    });
};