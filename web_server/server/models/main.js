const mongoose = require('mongoose');

module.exports.connect = (uri) => {
    mongoose.connect(uri);

    mongoose.connection.on('error', (err) => {
        console.error(`Mongoose connection error: ${err}`);
        process.exit();
    });

    // load mongoose model defined by user
    require('./user');
};