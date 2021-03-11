const hostsRouter = require('./routes/hosts')
const express = require('express')
const app = express()
const mongoose = require('mongoose')
const port = 8080;

app.set('view engine', 'ejs')

app.get('/', function (req, res){
    //Link til views/index.ejs
    const hosts = [{
      title: '192.168.1.6',
      createdAt: new Date(),
      description: 'Test host description'
    },
    {
      title: '192.168.1.5',
      createdAt: new Date(),
      description: 'Second host'

     }]
    res.render('index', {hosts: hosts})
});

app.use('/hosts', hostsRouter)


app.listen(port, () =>{
    console.log('Example app listening at http://localhost:${port}')
});