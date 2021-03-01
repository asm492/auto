from flask import Flask
import pymongo
import json

'''
To run:
  mkdir flask-by-example && cd flask-by-example
  python3 -m venv env
  source env/bin/activate

Queries:
  show dbs
  use mydb

  db.<collection>.find()
  db.scans.find( {"scan.starttime": 1614372826} )
  db.scans.deleteOne({"_id":ObjectId("ID GOES HERE") })

'''
#FILE = 'output.json'
app = Flask(__name__)

@app.route("/")
def hello():
  response = {}
  myquery = { "scan.starttime": 1614372826 }
  response = mycol.find_one(myquery)
  response.pop('_id', None)
  response =  json.dumps(response, indent = 4)
  print(response)
  return response


if __name__=="__main__":
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["mydb"]
  mycol = mydb["scans"]

  #Host=0.0.0.0 to allow connections from other machines
  #Allows localhost only by default
  app.run(debug=True, host='0.0.0.0')