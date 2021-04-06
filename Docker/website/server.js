const hostsRouter = require('./routes/hosts')
const express = require('express')
const app = express()
const Scan = require('./models/scan')
const mongoose = require('mongoose')
const port = 8080;

const MongoClient = require('mongodb').MongoClient;
const { urlencoded } = require('body-parser')
app.use(express.urlencoded({ extended: false }))

const uri = "mongodb://autoenum-mongodb:27017/"
app.set('view engine', 'ejs')
app.get('/', async (req, res) =>{
    //Link til views/index.ejs
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    try{

      await client.connect();
      const database = client.db('mydb');
      const collection = database.collection('scans');
      var hosts = [];
      hosts = await collection.find().toArray();
      console.log(hosts)
      res.render('index', {hosts: hosts});

    }catch(err){
      console.log("Feil" + err)
    }finally{
      await client.close();
    }

});

app.use('/hosts', hostsRouter)

app.listen(port, () =>{
    console.log('Example app listening at http://localhost:${port}')
});