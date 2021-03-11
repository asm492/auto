const express = require('express')
const router = express.Router()
//test
router.get('/', (req, res) => {
    res.send('In hosts')
})

module.exports = router