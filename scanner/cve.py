import requests
import requests.packages
import urllib3
import json


def find_cve(cpe):
  url = 'https://localhost:443/api/cvefor/'
  url += cpe
  print(url)
  urllib3.disable_warnings()
  requests.packages.urllib3.disable_warnings()
  resp = requests.get('https://localhost:443/api/cvefor/cpe:/a:apache:http_server:2.2.15', verify=False)
  r = []
  r.append(resp.json())
  print(type(r))

  result = {}
  for i in range(len(r)):
    result[i] = r[i]

  cve = []
  for i in result[0]:
    cve.append(i['id'])

  return cve

'''
find_cve("cpe:/a:apache:http_server:2.2.15")
OUTPUT:
['CVE-2014-0118', 'CVE-2012-0031', 'CVE-2012-0053', 'CVE-2014-0098',
'CVE-2015-0228', 'CVE-2014-0226', 'CVE-2014-0231', 'CVE-2011-0419',
'CVE-2012-0883', 'CVE-2010-1452', 'CVE-2009-1890', 'CVE-2010-2068',
'CVE-2013-1862', 'CVE-2012-2687', 'CVE-2013-1896', 'CVE-2013-2249',
'CVE-2011-3192', 'CVE-2012-3499', 'CVE-2015-3183', 'CVE-2011-3348',
'CVE-2011-3368', 'CVE-2011-3607', 'CVE-2011-3639', 'CVE-2012-4557',
'CVE-2012-4558', 'CVE-2011-4317', 'CVE-2011-4415', 'CVE-2013-6438',
'CVE-2016-4975', 'CVE-2016-5387', 'CVE-2018-1312', 'CVE-2018-1301',
'CVE-2018-1302', 'CVE-2018-1303', 'CVE-2017-3169', 'CVE-2017-3167',
'CVE-2016-8612', 'CVE-2018-17189', 'CVE-2017-7679', 'CVE-2017-7668',
'CVE-2017-9788', 'CVE-2017-9798']

'''