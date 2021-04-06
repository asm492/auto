def find_cve(cpe):
    url = 'https://localhost:443/api/cvefor/'
    url = url + cpe + PARAM + LIMIT
    urllib3.disable_warnings()
    requests.packages.urllib3.disable_warnings()
    cve = []
    try:
        resp = requests.get(url, verify=False, timeout=MAX_TIMEOUT)
    except requests.exceptions.HTTPError as errorHTTP:
        print("Http Error:", errorHTTP)
    except requests.exceptions.ConnectionError as errorConnection:
        print("Error Connecting:", errorConnection)
    except requests.exceptions.Timeout as errorTimeout:
        print("Timeout Error:", errorTimeout)
    except requests.exceptions.RequestException as errorRequest:
        print("General Error", errorRequest)
    else:
        r = []
        r.append(resp.json())
        result = {}
        for i in range(len(r)):
            result[i] = r[i]
        for i in result[0]:
            if 'id' in i:
                cve.append(i['id'])
    return cve