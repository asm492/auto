from flask import Flask
from flask import jsonify
import datetime
import imgkit
import os
import random

app = Flask(__name__)
#app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def hello():
  m = {}
  m['Message:'] = "Screenshot works!"
  m['Port'] = "3000"
  m['Endpoint'] = "/takescreengrab/<ip>/"
  return jsonify(m)


@app.route("/takescreengrab/<string:ip>/", methods=['GET'])
def takescreengrab(ip):
    t = datetime.datetime.now()
    filename=str(random.randint(100000,999999))
    filename += "-"
    date = t.strftime("%Y%m%d")
    filename += date
    filename += "-"
    time = t.strftime("%H%M%S")
    filename += time
    filename += ".jpg"
    path = "/pictures/" + filename


    imgkit_options= { 'quiet' : ''}
    ip = ip + ":" + "80"
    response = {}
    response['date'] =  date
    response['time'] = time

    try:
        imgkit.from_url(ip, path, options=imgkit_options)
    except ConnectionRefusedError:
        response['Message'] = "Connection refused"
    except IOError:
        response['Message'] = "IOError on"
    else:
        response['Filename'] = filename

    return jsonify(response)


if __name__=="__main__":
  app.run(debug=True, host='0.0.0.0', port=3000)