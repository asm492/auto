  
const mongoose = require('mongoose')
/*
const marked = require('marked')
const slugify = require('slugify')
const createDomPurify = require('dompurify')
const { JSDOM } = require('jsdom')
const dompurify = createDomPurify(new JSDOM().window)
*/
let hostSchema = new mongoose.Schema({
    _id:mongoose.Schema.Types.ObjectId,
    ip: String,
    mac: String,
    hostname: String,
    osmatch: Array,
    ports: Array,
    scandate: String,
    scantime: String
})

module.exports = mongoose.model('Host', hostSchema)