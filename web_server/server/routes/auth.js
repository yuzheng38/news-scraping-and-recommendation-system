const express = require('express');
const passport = require('passport');
const router = express.Router();
const validator = require('validator');

router.post('/signup', (req, res, next) => {
    const validationResult = validateSignupForm(req.body);
    if (!validationResult.success) {
        console.log('validation failed');
        return res.status(400).json({
            success: false,
            message: validationResult.message,
            errors: validationResult.errors
        });
    }

    return passport.authenticate('local-signup', (err) => {
        if (err) {
            console.log(err);
            if (err.name === 'MongoError' && err.code === 11000) {
                // 11000 mongo error code for duplication
                // 409 http status for conflict error
                return res.status(400).json({
                    success: false,
                    message: 'Check the form for errors',
                    errors: {
                        email: 'This email is already in use'
                    }
                });
            }
            // if other errors
            return res.status(400).json({
                success: falase,
                message: 'Could not process form'
            });
        }
        // if no error
        return res.status(200).json({
            success: true,
            message: 'You have successfully signed up.'
        });
    })(req, res, next); // looks like passport.authenticate returns a function. 
});

router.post('/login', (req, res, next) => {
    const validationResult = validateLoginForm(req.body);
    if (!validationResult.success) {
        return res.status(400).json({
            success: false,
            message: validationResult.message,
            errors: validationResult.errors
        });
    }
    
    return passport.authenticate('local-login', (err, token, userData) => {
        if (err) {
            if (err.name === 'IncorrectCredentialsError') { // this err.name is defined in and returned from login_passport.js
                return res.status(400).json({
                    success: false,
                    message: err.message
                });
            }
            return res.status(400).json({
                success: false,
                message: 'Could not process the login form'
            });
        }
        // console.log('in auth.js, user is ', userData.name);
        return res.status(200).json({
            success: true,
            message: 'You have successfully logged in.',
            token: token,
            user: userData
        });
    })(req, res, next); // return the middleware function back
});

function validateSignupForm(payload) {  // payload is req.body
    console.log(payload);
    const errors = {};
    let isFormValid = true;
    let message = '';

    if (!payload || typeof payload.email !== 'string' || !validator.isEmail(payload.email)) {
        isFormValid = false;
        errors.email = 'please provide a correct email';
    }

    if (!payload || typeof payload.email !== 'string' || payload.password.trim().length < 8) {
        isFormValid = false;
        errors.password = 'please provide a valid password with > 8 chars';
    }

    if (!isFormValid) {
        message = 'Check the form for errors';
    }

    return {
        success: isFormValid,
        message,
        errors
    };
}

function validateLoginForm(payload) {   // payload is req.body
    console.log(payload);
    const errors = {};
    let isFormValid = true;
    let message = '';

    if (!payload || typeof payload.email !== 'string' || payload.email.trim().length === 0) {
        isFormValid = false;
        errors.email = 'Please provide your email address.';
    }

    if (!payload || typeof payload.password !== 'string' || payload.password.length === 0) {
        isFormValid = false;
        errors.password = 'Please provide your password.';
    }

    if (!isFormValid) {
        message = 'Check the form for errors.';
    }

    return {
        success: isFormValid,
        message,
        errors
    };
}

module.exports = router;