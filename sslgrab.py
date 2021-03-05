import json
import xmltodict
import subprocess
import os

def remove_n(d):
    for k in d.keys():
        if type(d[k]) == str:
            d[k] = d[k].replace('\n', '')
        elif type(d[k]) == dict:
            remove_n(d[k])

def grab_ssl(ip):
    scan = subprocess.run(["nmap", "-p 443",  "--script", "ssl-cert", ip, "-oX", "cert.xml"], stdout=subprocess.DEVNULL)

def convert():
    f = open("cert.xml")
    xml_content = f.read()
    f.close()
    with open("ssl.json", "w") as file:
        json.dump(xmltodict.parse(xml_content), file, indent=4, sort_keys=True)
    os.remove("cert.xml")

def reorganise():
    with open("ssl.json") as json_file:
        result = json.load(json_file)

    sslc = {}
    for obj in result:
      try:
        sslc['subjectCommon'] = result[obj]['host']['ports']['port']['script']['table'][0]['elem']['#text']
        sslc['subjectAlt'] = result[obj]['host']['ports']['port']['script']['table'][3]['table'][2]['elem'][1]['#text']
        sslc['issuer'] = result[obj]['host']['ports']['port']['script']['table'][1]['elem']['#text']
        sslc['pbType'] = result[obj]['host']['ports']['port']['script']['table'][2]['elem'][2]['#text']
        sslc['pbBits'] = result[obj]['host']['ports']['port']['script']['table'][2]['elem'][0]['#text']
        sslc['signAlg'] = result[obj]['host']['ports']['port']['script']['elem'][0]['#text']
        sslc['notBefore'] = result[obj]['host']['ports']['port']['script']['table'][4]['elem'][1]['#text']
        sslc['notAfter'] = result[obj]['host']['ports']['port']['script']['table'][4]['elem'][0]['#text']
        sslc['md5'] = result[obj]['host']['ports']['port']['script']['elem'][1]['#text']
        sslc['sha'] = result[obj]['host']['ports']['port']['script']['elem'][2]['#text']
        sslc['cert'] = result[obj]['host']['ports']['port']['script']['elem'][3]['#text']
        #print(sslc['cert'])
        #print(type(sslc['cert']))
        strCert = str(sslc['cert'])
        #strCert.replace('\\n','')
        str = strCert.strip()
        sslc['cert'] = str
        print("**************************************")
        print(sslc['cert'])
        #print(strCert)
        #mac = result[obj]['host']['address'][1]['@addr']
        #print(sslc)
        #print(type(sslc))
      except KeyError as e:
        print(e)
      except TypeError as e:
        print(e)

    os.remove("ssl.json")
    return sslc


def take_sslgrab(ip):
  #ip = "192.168.1.5"
  grab_ssl(ip)
  convert()
  return reorganise()