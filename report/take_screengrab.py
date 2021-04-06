def take_screengrab(ip):
    url = 'http://localhost:3000/takescreengrab/'
    url += ip
    urllib3.disable_warnings()
    requests.packages.urllib3.disable_warnings()
    resp = {}
    try:
        resp = requests.get(url, verify=False, timeout=1).json()
    except requests.exceptions.HTTPError as errorHTTP:
        logging.debug("[SCREENGRAB] Http Error: ", errorHTTP)
    except requests.exceptions.ConnectionError as errorConnection:
        logging.debug("[SCREENGRAB] Error Connecting: ", errorConnection)
    except requests.exceptions.Timeout as errorTimeout:
        logging.debug("[SCREENGRAB] Timeout Error: ", errorTimeout)
    except requests.exceptions.RequestException as errorRequest:
        logging.debug("[SCREENGRAB] ERROR: ", errorRequest)

    return resp