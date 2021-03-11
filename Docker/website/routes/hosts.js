const express = require('express')
const router = express.Router()
const Host = require('./../models/host')
router.get('/', (req, res) => {
    res.send('In hosts')
})

module.exports = router