@app.route("/mac/<string:macaddr>/", methods=['GET'])
def mac(macaddr):
  query = { "macaddress.addr" : macaddr }
  return find_in_db(query)

def find_in_db(q):
  myclient = pymongo.MongoClient("mongodb://autoenum-mongodb:27017/")
  mydb = myclient["mydb"]
  mycol = mydb["scans"]
  response = {}
  result = mycol.find(q)

  for doc in result:
    host_object = doc['uuid']
    doc.pop('_id', None)
    response[host_object] = doc

  return jsonify(response)

