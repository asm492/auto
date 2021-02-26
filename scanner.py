import nmap3
import json
import socket
import sys
import os
import datetime
import time
import imgkit
import argparse
import logging
try:
       import screenshot
except ImportError:
       print("screenshot module not found!")

OUTPUT = 'output.json'
TCP_FILE = 'tcp.json'
UDP_FILE = 'udp.json'
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

def print_json_file(result, file_name):
        logging.debug('[JSON] printing')
        for ip_addr in result:
                if ip_addr != "stats" and ip_addr != "runtime":
                        if not result[ip_addr]['macaddress']:
                                result[ip_addr]['macaddress'] = "N/A"
                                logging.debug("IP: " + ip_addr + " MAC: " + result[ip_addr]['macaddress'])
        result = str(result)
        result = result.replace("\'", "\"")
        result = json.loads(result)
        with open(file_name, "w") as file:
                json.dump(result, file, ensure_ascii=False, indent=4, sort_keys=True)
        logging.debug('[JSON] done')

def find_interesting_ip(result):
        logging.debug('\t[INTERESTING IP] started')
        output_list = open("ips_to_scan.txt","w")
        for ip_addr in result:
                #if ip_addr != "stats" and ip_addr != "runtime":
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
          #if ip != "stats" and ip != "runtime":
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

def possible_webpage(res):
        logging.debug('[FIND WEBPAGE] started')
        screengrab_list = open("ips_to_screengrab.txt","w")
        for ip_addr in result:
           # if ip_addr != "stats" and ip_addr != "runtime":
                for i in range(len(result[ip_addr]['ports'])):
                    if result[ip_addr]['ports'][i]['state'] == "open" or result[ip_addr]['ports'][i]['state'] == "filtered":
                       if result[ip_addr]['ports'][i]['portid'] == "80":
                          logging.debug('\tPossible webpage on: ' + ip_addr)
                          screengrab_list.write(ip_addr + "\n")
        screengrab_list.close()
        logging.debug('[FIND WEBPAGE] done')
def perform_tcp_scan():
        #Aka Stage 2
        #Tid uten -A på 192.168.1.0/24 og .2.0/24
        #: 3:10. Med -A: 4:10 og det klikker.
        # Med O: 3:36
        logging.debug('[TCP SCAN] started')
        nmap = nmap3.Nmap()
        result = nmap.nmap_version_detection(None, "-sV -p- -O -iL ips_to_scan.txt");
        result = remove_keys(result)
        logging.debug("perfom_tcp_scan")
        possible_webpage(result)
        #print_json_file(result, "tcp.json")
        logging.debug('[TCP SCAN] done')
        return result

def perform_udp_scan():
        #Aka Stage 3
        logging.debug('[UDP SCAN] started')
        nmap = nmap3.NmapScanTechniques()
        result = nmap.nmap_udp_scan(None, "-iL ips_to_scan.txt -p53,67,68,123,137,138,161,445,5000")
        result = remove_keys(result)
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
    for k, v in res.items():
        if v is None:
            res[k] = "N/A"
        elif type(v) == type(res):
            replace(v)

def print_merged_file(tcp, udp, start_time):
  logging.debug('[JSON MERGE] printing')
  #New dic
  merged = {}
  merged['tcp'] = tcp
  merged['udp'] = udp
  replace(merged)
  #End time
  end_time = int(datetime.datetime.now().timestamp())
  #merged['scan'] = {'starttime' : start_time, 'endtime' : end_time }
  logging.debug(merged)
  #FEILEN LIGGER HER! FÅR KEY VALUE PAIR SOM HAR VERDI NONE
  merged['scan'] = {'starttime' : start_time, 'endtime' : end_time }
  logging.debug(merged)
  merged = str(merged)
  merged = merged.replace("\'", "\"")
  merged = json.loads(merged)
  with open(OUTPUT, "w") as file:
    json.dump(merged, file, ensure_ascii=False, indent=4, sort_keys=True)

  logging.debug('[JSON MERGE] done')

if __name__=="__main__":
  #Get current time (Epoch)
  start = int(datetime.datetime.now().timestamp())

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
  has_target()
  exclude_self()
  perform_host_discovery()
  result = perform_portscan()
  result_tcp = perform_tcp_scan()
  result_udp = perform_udp_scan()


  #print(result)

  #Stage 4
  resp = screenshot.perform_screenshot()

  if resp == 1:
    logging.debug('[SCREENGRABS] FAILED!')
  else:
    logging.debug('[SCREENGRABS] taken')

  print_merged_file(result_tcp, result_udp, start)
  logging.debug('[SCRIPT] done')