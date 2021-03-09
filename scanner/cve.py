import requests
import requests.packages
import urllib3
import json

#This works
def find_cve(cpe):
  url = 'https://localhost:443/api/cvefor/'
  url += cpe
  print(url)
  urllib3.disable_warnings()
  requests.packages.urllib3.disable_warnings()
  resp = requests.get(url, verify=False)
  r = []
  r.append(resp.json())

  result = {}
  for i in range(len(r)):
    result[i] = r[i]

  cve = []
  for i in result[0]:
    cve.append(i['id'])

  return cve