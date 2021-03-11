const mongoose = require('mongoose')
const hostSchema = new mongoose.Schema({
    id: String,
    ip: String,
    mac: String,
    osmatch: Array,
    ports: Array,
    scandate: String,
    scantime: String
})

module.exports = mongoose.model('Host', hostSchema)