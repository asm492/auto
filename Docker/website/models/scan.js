const mongoose = require('mongoose');

var scanSchema = new mongoose.Schema({
    ip: {
        type: String
    },
    hostname: {
        type: Array
    }
});
//Todo : Update to host
module.exports = mongoose.model('Scan', scanSchema);