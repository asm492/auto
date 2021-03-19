from flask import Flask, jsonify, render_template, url_for, send_from_directory
import pymongo
import json
import os

app = Flask(__name__, static_folder="/pictures")
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def hello():
  examples = {}
  examples['/cpe:/a:apache:http_server:2.4.46'] = "Returns all hosts with the given CPE"
  examples['/cpe:/o:microsoft:windows'] = "Returns all hosts with the given CPE"
  examples['/ip/192.168.1.5'] = "Returns all host objects with IP address 192.168.1.5"
  examples['/mac/FA:16:3E:EC:B4:0F'] = "Returns all host object with MAC address FA:16:3E:EC:B4:0F"
  examples['/date/20210302'] = "Returns all host objects scanned March 2nd 2021"
  examples['/viewpicture/644305-20210315-143941.jpg'] = "Returns all host objects scanned March 2nd 2021"

  valid = {}
  valid['/'] = "Returns this message"
  valid['/<cpe>'] = "A CPE written in correct format (see example)"
  valid['/ip/<ipaddress>'] = "An IP address"
  valid['/mac/<macaddress>'] = "A MAC address"
  valid['/date/<date>'] = "Date in yyyymmdd format"
  valid['/viewpicture/<filename>'] = "Displays the specified picture if in database"
  valid['/all'] = "Returns ALL documents in DB"

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
  #Used by webgui
  return send_from_directory("/pictures", filename, as_attachment=True)


@app.route("/viewpicture/<string:filename>", methods=['GET'])
def viewpicture(filename):
  return render_template('display.html', img=filename)


@app.route("/log", methods=['GET'])
def log():
  try:
    with open('/log/Scanner.log') as f:
      data = f.read()
    f.close()
    return data
  except FileNotFoundError:
    m = {}
    m['Error'] = 'No log file found'
    return jsonify(m)


def find_in_db(q):
  myclient = pymongo.MongoClient("mongodb://autoenum-mongodb:27017/")

  mydb = myclient["mydb"]
  mycol = mydb["scans"]

  response = {}
  result = mycol.find(q)

  for doc in result:

    hostid = str(doc['_id'])
    hostid.replace("ObjectId(\"","")
    hostid.replace("\"","")
    doc.pop('_id', None)
    response[hostid] = doc


  return jsonify(response)

if __name__=="__main__":
  app.run(debug=True, host='0.0.0.0', port=5001)