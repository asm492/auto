import pymongo
import json


'''
Puts output.json into MongoDB
IP '.' must be replaced with '-'


Queries:
  show dbs
  use mydb

  db.<collection>.find()
  db.scans.find( {"scan.starttime": 1614372826} )
  db.scans.deleteOne({ "_id": ObjectId("603e2f89b1c62580bb25c149")});


'''
FILE = 'output.json'

if __name__=="__main__":
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["mydb"]
  mycol = mydb["scans"]

  with open(FILE) as json_file:
    result = json.load(json_file)

  print(result)
  mycol.insert_one(result)