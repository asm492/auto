const express = require('express')
const { urlencoded } = require('body-parser')


//var bodyParser = require('body-parser')


const router = express.Router()
const MongoClient = require('mongodb').MongoClient;
//REMEBER TO CHANGE WHEN RUNNING IN OPENSTACK
const uri = "mongodb+srv://user3:6p@biBWhJF@Fs@Z@cluster0.yqxoa.mongodb.net/mydb?retryWrites=true&w=majority"
//const uri = "mongodb://autoenum-mongodb:27017/"
const ObjectID = require('mongodb').ObjectID;

require('../models/scan');

//test
router.get('/', (req, res) => {
    res.send('In hosts')
})


router.get('/list_view', async (req, res)  => {

    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    try{
      
      await client.connect();
      const database = client.db('mydb');
      const collection = database.collection('scans');
      //var q = {ip:"192.168.1.5"}
      var hosts = [];
      hosts = await collection.find().toArray();
      console.log(hosts)
      res.render('./../views/list', {hosts: hosts})
      
    }catch(err){
      console.log("Feil" + err)
    }finally{
      await client.close();
    }

    
})

router.get('/details/:id', async (req, res)  => {

    
    var hostId = req.params.id
    console.log(hostId)
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    try{
      
      await client.connect();
      const database = client.db('mydb');
      const collection = database.collection('scans');
      var obj_id = new ObjectID(hostId);
      var query = {'_id': obj_id}
      console.log(query)
      
      var host = await collection.findOne(query);
      console.log(host)
      res.render('./../views/details', {host: host})
      
    }catch(err){
      console.log("Feil" + err)
    }finally{
      await client.close();
    }

    
})

router.get('/getjson/:id', async (req, res)  => {

    
    var hostId = req.params.id
    console.log(hostId)
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    try{
      
      await client.connect();
      const database = client.db('mydb');
      const collection = database.collection('scans');
      var obj_id = new ObjectID(hostId);
      var query = {'_id': obj_id}
      console.log(query)
      
      var host = []
      host = await collection.findOne(query);
      console.log(host)
      return res.json(host)
      
    }catch(err){
      console.log("Feil" + err)
      return res(err)
    }finally{
      await client.close();
    }

    
})
              
router.post('/getsearchresults/:type', async function(req, res) {

    //console.log(req)
    
    //console.log(type)

    var q = ''
    var type = req.params.type
    var query = req.body.search_query

    console.log(req.body.search_query)
    console.log(type)

    switch(type){
        case 'ip': q = {ip : query};
        break;

        case 'mac': q = {macaddress : query};
        break;
        
        //case 'date': q = {scanstats[scandate] : query};
        //break;

        //case 'cpe': q = {$or [{ports[]}],[{osmatch[0][cpe]}] };
        //break;
    }

    console.log(q)
    

    
    //const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });


    /*
    try{
      
      await client.connect();
      const database = client.db('mydb');
      const collection = database.collection('scans');
      var obj_id = new ObjectID(hostId);
      var query = {'_id': obj_id}
      console.log(query)
      
      var host = []
      host = await collection.findOne(query);
      console.log(host)
      return res.json(host)
      
    }catch(err){
      console.log("Feil" + err)
      return res(err)
    }finally{
      await client.close();
    }
    */

    
})

router.get('/search', async (req, res)  => {

    res.render('./../views/search')
    
})

module.exports = router