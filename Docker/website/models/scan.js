const mongoose = require('mongoose');

var customerSchema = new mongoose.Schema({
    ip: {
        type: String,
    }
});
module.exports = mongoose.model('Scan', scanSchema);