import nmap3
import json
import socket
import sys
import os
from datetime import datetime
import sslgrab as sgrab #Our sslgrab.py
import cve_lookup
import time
import imgkit
import argparse
import logging
import pymongo
import ast #Testing only

DBLINK = 'mongodb://localhost:27018/'
#DBLINK = 'mongodb://autoenum_mongodb:27018/'
TARGETFILE = "target.txt"
LOG_FORMAT = "%(name)s %(asctime)s - %(message)s"
FILENAME = "log.txt"

def exclude_self():
        host_ip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
        f = open("exclude_ip.txt", "w")
        f.write(host_ip + "\n")
        f.close()

def has_target():
        #Checks if target.txt exists and is populated
   logging.debug('[TARGETS] checking')
   try:
        f = open("target.txt","r")
   except FileNotFoundError as e:
        logging.debug(e)
        logging.debug("\t[TARGETS] File missing!")
        sys.exit(1)
   else:
        if os.path.getsize(TARGETFILE):
         #Ergo file is not empty
           logging.debug("\t[TARGETS] OK")
           return 0
        else:
          #File empty
          logging.debug("\t[TARGETS] File empty!")
          sys.exit(1)

        f.close()

def find_interesting_ip(result):
  logging.debug('\t[INTERESTING IP] started')
  output_list = open("ips_to_scan.txt","w")
  for ip_addr in result:
    logging.debug("\t\t" + ip_addr)
    for i in range(len(result[ip_addr]['ports'])):
      if result[ip_addr]['ports'][i]['state'] == "open" or result[ip_addr]['ports'][i]['state'] == "filtered":
        output_list.write(ip_addr + "\n")
        logging.debug("\t\t\t" + result[ip_addr]['ports'][i]['portid'])
        break

  output_list.close()
  logging.debug("\t[INTERESTING IP] done")

def perform_host_discovery():
        #Aka stage 0
        logging.debug('[HOST DISCOVERY] started')
        nmap = nmap3.NmapHostDiscovery()
        res = nmap.nmap_no_portscan(None, args="-sn --excludefile exclude_ip.txt -iL target.txt")
        logging.debug('Output of host discovery: ')
        res = remove_keys(res)
        logging.debug(res)
        f  = open("ips_to_scan.txt", "w")
        for ip in res:
            logging.debug('Found IP: ' + ip)
            if res[ip]['state']['state'] == "up":
              f.write(ip + "\n")
        f.close()
        logging.debug('[HOST DISCOVERY] done')

def perform_portscan():
        #Fast portscan. Aka Stage 1
        logging.debug('[FAST PORTSCAN] started')
        nmap = nmap3.NmapHostDiscovery()
        res = nmap.scan_top_ports(None, args="-F -iL ips_to_scan.txt")
        res = remove_keys(res)
        logging.debug(res)
        find_interesting_ip(res)
        logging.debug('[FAST PORTSCAN] done')
        return res

def perform_tcp_scan():
  #Aka Stage 2
  #Tid uten -A på 192.168.1.0/24 og .2.0/24
  #: 3:10. Med -A: 4:10 og det klikker.
  # Med O: 3:36
  logging.debug('[TCP SCAN] started')
  nmap = nmap3.Nmap()
  result = nmap.nmap_version_detection(None, "-sV -p- --script ssl-cert -vv -O -iL ips_to_scan.txt");
  remove_keys(result)
  print(result)
  logging.debug(result)
  #old_possible_webpage(result)
  #print_json_file(result, "tcp.json")
  logging.debug('[TCP SCAN] done')
  return result

def perform_udp_scan():
  #Aka Stage 3
  logging.debug('[UDP SCAN] started')
  nmap = nmap3.NmapScanTechniques()
  result = nmap.nmap_udp_scan(None, "-iL ips_to_scan.txt -p53,67,68,123,137,138,161,445,5000")
  remove_keys(result)
  #print_json_file(result, "udp.json")
  logging.debug('[UDP SCAN] done')
  return result

def remove_keys(res):
  logging.debug('[KEYS] deleting')
  res.pop('stats', None)
  res.pop('runtime', None)
  logging.debug(res)
  logging.debug('[KEYS] done')
  return res

def replace(res):
  #Not in use
  for k, v in res.items():
    if v is None:
      res[k] = "N/A"
    elif type(v) == type(res):
      replace(v)

def find_ssl(res):
  logging.debug('[FIND WEBPAGE] started')
  #screengrab_list = open("ips_to_screengrab.txt","w")

  r = {}
  for k in res['ports']:
    if k['portid'] == '80':
      logging.debug('\tPossible webpage on: ' + res['ip'])
      #screengrab_list.write(res['ip'] + "\n")
    if k ['portid'] == '443':
      logging.debug('\tPossible SSL on: ' + res['ip'])

  #screengrab_list.close()
  logging.debug('[FIND WEBPAGE] done')

def merge_results(t, u, start):
  ##This function reorganizes output
  #from nmap to to have data sorted
  #by hosts.

  #Just converting the start time
  #object from main to date and time
  logging.debug("[MERGE RESULTS] start")
  starttime = start.strftime("%H%M%S")
  startdate = start.strftime("%Y%m%d")

  #Remove

  for i in t:
    logging.debug(i)
    logging.debug(t[i])
    logging.debug(t[i]['osmatch'])
    os = t[i]['osmatch']
    t_ports = t[i]['ports']
    u_ports = u[i]['ports']
    ports = t_ports + u_ports

    for port in ports:
      cve = []
      for script in port['scripts']:
        s = script['data']
        s.pop(0, None)
      if 'cpe' in port:
        if 'cpe' in port['cpe'][0]:
          cpe = port['cpe'][0]['cpe']
          cve = cve_lookup.find_cve(cpe)
          port['cpe'][0]['cve'] = cve
    hostname = t[i]['hostname']
    macaddress = t[i]['macaddress']
    state = t[i]['state']
    stats = {'scandate': startdate, 'scantime': starttime}

    #host = {'ip' : i, 'hostname': hostname, 'macaddress': macaddress,'osmatch': os, 'ports' : ports, 'state' : state, 'scanstats': stats}
    #sslc = {}
    host = {'ip' : i, 'hostname': hostname, 'macaddress': macaddress,'osmatch': os, 'ports' : ports, 'state' : state, 'scanstats': stats}
    insert_db(host)
    #print("\n\n\n")
    #print(host)

  logging.debug("[MERGE RESULTS] done")

def insert_db(res):
    myclient = pymongo.MongoClient(DBLINK)
    mydb = myclient["mydb"]
    mycol = mydb["scans"]

    mycol.insert_one(res)

if __name__=="__main__":
  #Get current time (Epoch)
  #start = int(datetime.datetime.now().timestamp())
  now = datetime.now()
  start = now.strftime("%H%M%S")


  #For verbose logging and debug:
  parser = argparse.ArgumentParser(description="USAGE: python3 scanner.py [options]")
  parser.add_argument("-v", "--verbose", help="Enable output to screen, no output by default", action="store_true")
  args = parser.parse_args()
  level    = logging.DEBUG
  handlers = [logging.FileHandler(FILENAME)]

  #Always output to file. To screen if -v
  if args.verbose:
    handlers.append(logging.StreamHandler())

  logging.basicConfig(level = level, format = LOG_FORMAT, handlers = handlers)
  logging.debug('[SCRIPT] started')

  #MAIN:
  '''
  has_target()
  exclude_self()
  perform_host_discovery()
  result = perform_portscan()
  result_tcp = perform_tcp_scan()
  result_udp = perform_udp_scan()
  f = open("tcp.json", "w")
  f.write(str(result_tcp))
  f.close()

  f = open("udp.json", "w")
  f.write(str(result_udp))
  f.close()

  '''
  #Testing
  with open('tcp.json') as f:
    data = f.read()
  result_tcp = ast.literal_eval(data)
  #print(result_tcp)
  #print(type(result_tcp))

  with open('udp.json') as f:
    data = f.read()
  result_udp = ast.literal_eval(data)
  #print(result_udp)
  #print(type(result_udp))

  #print(result)
  '''
  #Stage 4
  if resp == 1:
    logging.debug('[SCREENGRABS] FAILED!')
  else:
    logging.debug('[SCREENGRABS] taken')
  '''

  # print(result_tcp)
  merge_results(result_tcp, result_udp, now)
  logging.debug('[SCRIPT] done')