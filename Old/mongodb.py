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
  #Med JSON format
  db.scans.find( {"scan.date": "20210302" } ).pretty()

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