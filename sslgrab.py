import json
import xmltodict
import subprocess

def grab_ssl():
    scan = subprocess.run(["nmap", "-p 443",  "--script", "ssl-cert","-iL", "ips.txt", "-oX", "cert.xml"], stdout=subprocess.DEVNULL)


def convert():
    f = open("cert.xml")
    xml_content = f.read()
    f.close()
    with open("output.json", "w") as file:
        json.dump(xmltodict.parse(xml_content), file, indent=4, sort_keys=True)

def reorganise():
    with open("output.json") as json_file:
        result = json.load(json_file)
    for obj in result:
        subjectCommon = result[obj]['host']['ports']['port']['script']['table'][0]['elem']['#text']
        subjectAlt = result[obj]['host']['ports']['port']['script']['table'][3]['table'][2]['elem'][1]['#text']
        issuer = result[obj]['host']['ports']['port']['script']['table'][1]['elem']['#text']
        pbType = result[obj]['host']['ports']['port']['script']['table'][2]['elem'][2]['#text']
        pbBits = result[obj]['host']['ports']['port']['script']['table'][2]['elem'][0]['#text']
        signAlg = result[obj]['host']['ports']['port']['script']['elem'][0]['#text']
        notBefore = result[obj]['host']['ports']['port']['script']['table'][4]['elem'][1]['#text']
        notAfter = result[obj]['host']['ports']['port']['script']['table'][4]['elem'][0]['#text']
        md5 = result[obj]['host']['ports']['port']['script']['elem'][1]['#text']
        sha = result[obj]['host']['ports']['port']['script']['elem'][2]['#text']
        cert = result[obj]['host']['ports']['port']['script']['elem'][3]['#text']
        mac = result[obj]['host']['address'][1]['@addr']

        print (subjectCommon)
        print(subjectAlt)
        print(issuer)
        print(pbType)
        print(signAlg)
        print(notBefore)
        print(notAfter)
        print(md5)
        print(cert)
        print(mac)

grab_ssl()
convert()
reorganise()