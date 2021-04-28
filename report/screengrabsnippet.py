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