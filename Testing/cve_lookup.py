import requests
import requests.packages
import urllib3
import json

#Default LIMIT = 30, too slow
LIMIT = "10"
PARAM = "?limit="

def find_cve(cpe):
  print("\tMOTTATT CPE: ", cpe)
  url = 'https://localhost:443/api/cvefor/'
  url = url + cpe + PARAM + LIMIT
  urllib3.disable_warnings()
  requests.packages.urllib3.disable_warnings()
  cve = []
  #resp = requests.get('https://10.212.139.228:443/api/cvefor/cpe:/a:apache:http_server:2.2.15', verify=False)
  try:
    resp = requests.get(url, verify=False, timeout=5)
  except requests.exceptions.HTTPError as errorHTTP:
    print ("Http Error:",errorHTTP)
  except requests.exceptions.ConnectionError as errorConnection:
    print ("Error Connecting:",errorConnection)
  except requests.exceptions.Timeout as errorTimeout:
    print ("Timeout Error:",errorTimeout)
  except requests.exceptions.RequestException as errorRequest:
    print ("OOps: Something Else", errorRequest)
  else:
    r = []
    r.append(resp.json())
    result = {}
    for i in range(len(r)):
      result[i] = r[i]
    print(result)
    for i in result[0]:
      print("\tSiste forloop i cve")
      if 'id' in i:
        print(i['id'])
        cve.append(i['id'])

  return cve