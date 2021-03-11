const mongoose = require('mongoose');
const hostsRouter = require('./routes/hosts')
const express = require('express')
const app = express()
const mongoose = require('mongoose')
const port = 8080;

mongoose.connect('mongodb://autoenum-mongodb:27017/mydb', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})

app.set('view engine', 'ejs')

app.get('/', function (req, res){
    //Link til views/index.ejs
    res.render('index', {hosts: hosts})
});

app.get('/all')

app.use('/hosts', hostsRouter)


app.listen(port, () =>{
    console.log('Example app listening at http://localhost:${port}')
});