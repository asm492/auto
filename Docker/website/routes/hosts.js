const express = require('express')
const { urlencoded } = require('body-parser')
const router = express.Router()
const MongoClient = require('mongodb').MongoClient;
//REMEBER TO CHANGE WHEN RUNNING IN OPENSTACK
//const uri = "mongodb+srv://user3:6p@biBWhJF@Fs@Z@cluster0.yqxoa.mongodb.net/mydb?retryWrites=true&w=majority"
const uri = "mongodb://autoenum-mongodb:27017/"
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
    var img = ''
    var req_url = req.headers.referer
    console.log(req_url)
    req_url = req_url.replace("8080/","5001/")



    var hostId = req.params.id
    console.log(hostId)
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    try{

      await client.connect();
      const database = client.db('mydb');
      const collection = database.collection('scans');
      var query = {'uuid': hostId}
      console.log(query)

      var host = await collection.findOne(query);


      for(var i = 0; i < host['ports'].length; i++){
        if('screengrab' in host['ports'][i]){
          var view_img = req_url
          view_img += "viewpicture/"
          img = req_url
          img += "picture/"
          img += host['ports'][i]['screengrab']['Filename']
          view_img += host['ports'][i]['screengrab']['Filename']
        }
      }


      res.render('./../views/details', {host: host, image: img, viewimage: view_img})

    }catch(err){
      res.send(err)
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
      
      var query = {'uuid': hostId}
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


router.post('/search', async function(req, res) {

  const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    var query = req.body.all_query

 
    var ip_q = {ip : query};
    var mac_q = {"macaddress.addr" : query}
    var date_q = {"scanstats.scandate" : query};
    var os_cpe_q = {"osmatch.cpe" : query };
    var ports_cpe_q = {"ports.cpe.cpe" : query };
    var uuid_q = {"uuid" : query}
    var q = {"$or": [ip_q, mac_q, date_q, os_cpe_q, ports_cpe_q, uuid_q]}

    try{

      await client.connect();
      const database = client.db('mydb');
      const collection = database.collection('scans');

      var hosts = []
      hosts = await collection.find(q).toArray();
      res.render('./../views/searchresults', {hosts: hosts, query: query});

    }catch(err){
      console.log("Feil" + err)
      return res(err)
    }finally{
      await client.close();
    }

})

router.get('/search', async (req, res)  => {

    res.render('./../views/search')

})

module.exports = router