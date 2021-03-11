<<<<<<< HEAD
const mongoose = require('mongoose')
const hostSchema = new mongoose.Schema({
    id: String,
    ip: String,
    mac: String,
=======
  
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
>>>>>>> parent of ef1fea2... Revert
    osmatch: Array,
    ports: Array,
    scandate: String,
    scantime: String
})

module.exports = mongoose.model('Host', hostSchema)