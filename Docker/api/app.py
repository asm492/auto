from flask import Flask, jsonify, render_template, url_for
import pymongo
import json
import os

app = Flask(__name__, static_folder="/pictures")
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def hello():
  examples = {}
  examples['/cpe:/a:apache:http_server:2.4.46/'] = "Returns all hosts with the given CPE"
  examples['/cpe:/o:microsoft:windows/'] = "Returns all hosts with the given CPE"
  examples['/ip/192.168.1.5/'] = "Returns all host objects with IP address 192.168.1.5"
  examples['/mac/FA:16:3E:EC:B4:0F/'] = "Returns all host object with MAC address FA:16:3E:EC:B4:0F"
  examples['/date/20210302/'] = "Returns all host objects scanned March 2nd 2021"

  valid = {}
  valid['/'] = "Returns this message"
  valid['/<cpe>/'] = "A CPE written in correct format (see example)"
  valid['/ip/<ipaddress>/'] = "An IP address"
  valid['/mac/<macaddress>/'] = "A MAC address"
  valid['/date/<date>/'] = "Date in yyyymmdd format"
  valid['/all/'] = "Returns ALL documents in DB"

  m = {}
  m['message'] = "Autoenum API. Usage:"
  m['Port'] = "5001"
  m['Valid endpoints'] = valid
  m['Examples'] = examples
  return jsonify(m)


@app.route("/cpe:/<string:cpe>/", methods=['GET'])
def cpe(cpe):
  c = "cpe:/" + cpe
  query = { "$or": [ {"osmatch.cpe" : c } , {"ports.cpe.cpe" : c } ] }
  return find_in_db(query)

@app.route("/ip/<string:ipaddr>/", methods=['GET'])
def ip(ipaddr):
  query = { "ip" : ipaddr }
  return find_in_db(query)

@app.route("/mac/<string:macaddr>/", methods=['GET'])
def mac(macaddr):
  query = { "macaddress.addr" : macaddr }
  return find_in_db(query)

@app.route("/date/<string:date>/", methods=['GET'])
def date(date):
  query = { "scanstats.scandate" : date }
  return find_in_db(query)

@app.route("/all/", methods=['GET'])
def all():
  query = {}
  return find_in_db(query)

@app.route("/picture/<string:filename>", methods=['GET'])
def picture(filename):
  return render_template('display.html', img=filename)

def find_in_db(q):
  myclient = pymongo.MongoClient("mongodb://autoenum-mongodb:27017/")

  mydb = myclient["mydb"]
  mycol = mydb["scans"]

  response = {}
  result = mycol.find(q)
  index = 0

  for doc in result:
    outer_key = "HostObject-" + str(index)
    #Removes id key:value to make it valid JSON
    doc.pop('_id', None)
    response[outer_key] = doc
    index += 1

  return jsonify(response)

if __name__=="__main__":
  app.run(debug=True, host='0.0.0.0')