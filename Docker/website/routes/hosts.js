const express = require('express')
const router = express.Router()
require('./../models/scan');

//test
router.get('/', (req, res) => {
    res.send('In hosts')
})

module.exports = router