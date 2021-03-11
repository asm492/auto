const express = require('express')
const Host = require('./../models/host')
const router = express.Router()
//test
router.get('/:id', async (req, res) => {
    const host = await Host.findById(req.params.id)
    if (host == null) res.redirect('/')
    res.render('hosts/display', {host:host})
})

module.exports = router