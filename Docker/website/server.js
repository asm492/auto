const express = require('express')
const app = express()

const port = 8080;

app.set('view engine', 'ejs')

app.get('/', function (req, res){
    res.render('index!')
});

app.listen(port, () =>{
    console.log('Example app listening at http://localhost:${port}')
});