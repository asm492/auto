const hostsRouter = require('./routes/hosts')
const express = require('express')
const app = express()

const port = 8080;

app.set('view engine', 'ejs')
app.use(hostsRouter)
app.get('/', function (req, res){
    //Link til views/index.ejs
    res.render('index', {text: 'hosts'})
});

app.listen(port, () =>{
    console.log('Example app listening at http://localhost:${port}')
});