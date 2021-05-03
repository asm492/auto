import nmap3
import json
import socket
import sys
import os
import requests
import requests.packages
import urllib3
from datetime import datetime
import cve_lookup
import time
import argparse
import logging
import pymongo
import uuid
import ast 

DB_URL = 'mongodb://localhost:27018/'
DB_NAME = "mydb"
COLLECTION_NAME = "scans"
TARGETFILE = "target.txt"
LOG_FORMAT = "%(name)s %(asctime)s - %(message)s"
FILENAME = "/var/lib/docker/volumes/files_log-volume/_data/Scanner.log"


def exclude_self():
    host_ip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
               [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    f = open("exclude_ip.txt", "w")
    f.write(host_ip + "\n")
    f.close()


def has_target():
    # Checks if target.txt exists and is populated
    logging.debug('[TARGETS] checking')
    try:
        f = open("target.txt", "r")
    except FileNotFoundError as e:
        logging.debug(e)
        logging.debug("\t[TARGETS] File missing!")
        sys.exit(1)
    else:
        if os.path.getsize(TARGETFILE):
         # Ergo file is not empty
            logging.debug("\t[TARGETS] OK")
            return 0
        else:
            # File empty
            logging.debug("\t[TARGETS] File empty!")
            sys.exit(1)

        f.close()


def copy_file():
    # Target.txt ok
    if not has_target():
        os.system('cp target.txt ips_to_scan.txt')


def find_interesting_ip(result):
    logging.debug('\t[INTERESTING IP] started')
    output_list = open("ips_to_scan.txt", "w")
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
    # Stage 1
    logging.debug('[HOST DISCOVERY] started')
    nmap = nmap3.NmapHostDiscovery()
    res = nmap.nmap_no_portscan(
        None, args="-sn --excludefile exclude_ip.txt -iL target.txt")
    logging.debug('Output of host discovery: ')
    res = remove_keys(res)
    logging.debug(res)
    f = open("ips_to_scan.txt", "w")
    for ip in res:
        logging.debug('Found IP: ' + ip)
        if res[ip]['state']['state'] == "up":
            f.write(ip + "\n")
    f.close()
    logging.debug('[HOST DISCOVERY] done')


def perform_portscan():
    # Stage 2
    logging.debug('[FAST PORTSCAN] started')
    nmap = nmap3.NmapHostDiscovery()
    res = nmap.scan_top_ports(None, args="-F -iL ips_to_scan.txt")
    res = remove_keys(res)
    logging.debug(res)
    find_interesting_ip(res)
    logging.debug('[FAST PORTSCAN] done')
    return res


def perform_tcp_scan():
    # Stage 3
    logging.debug('[TCP SCAN] started')
    nmap = nmap3.Nmap()
    result = nmap.nmap_version_detection(
        None, "-sV -p- --script ssl-cert -vv -O -iL ips_to_scan.txt")
    remove_keys(result)
    print(result)
    logging.debug(result)

    logging.debug('[TCP SCAN] done')
    return result

def perform_udp_scan():
    # Stage 4
    logging.debug('[UDP SCAN] started')
    nmap = nmap3.NmapScanTechniques()
    result = nmap.nmap_udp_scan(
        None, "-iL ips_to_scan.txt -p53,67,68,123,137,138,161,445,5000")
    remove_keys(result)
    logging.debug('[UDP SCAN] done')
    return result

def remove_keys(res):
    logging.debug('[KEYS] deleting')
    res.pop('stats', None)
    res.pop('runtime', None)
    logging.debug(res)
    logging.debug('[KEYS] done')
    return res


def take_screengrab(ip):
  # Stage 6
    url = 'http://localhost:3000/takescreengrab/'
    url += ip
    urllib3.disable_warnings()
    requests.packages.urllib3.disable_warnings()
    logging.debug(url)
    #response = ''
    #r = "0"
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


def merge_results(t, u, start):
  #Stage 5
    logging.debug("[MERGE RESULTS] start")
    starttime = start.strftime("%H%M%S")
    startdate = start.strftime("%Y%m%d")

    for i in t:
        os = t[i]['osmatch']
        t_ports = t[i]['ports']
        ports = t_ports
        if i in u:
            u_ports = u[i]['ports']
            ports += u_ports

        for j in t[i]['osmatch']:
            if 'cpe' in j:
                if j['cpe']:
                    oscve = []
                    oscpe = j['cpe']
                    oscve = cve_lookup.find_cve(oscpe)
                    logging.debug(oscve)
                    j['cve'] = oscve

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

                screengrab = take_screengrab(i)
                if 'Filename' in screengrab:
                    port['screengrab'] = screengrab
        hostname = t[i]['hostname']
        macaddress = t[i]['macaddress']
        state = t[i]['state']
        stats = {'scandate': startdate, 'scantime': starttime}

        uid = str(uuid.uuid4())
        host = {'uuid': uid, 'ip': i, 'hostname': hostname, 'macaddress': macaddress,
                'osmatch': os, 'ports': ports, 'state': state, 'scanstats': stats}
        insert_db(host)

    logging.debug("[MERGE RESULTS] done")


def insert_db(res):
  # Stage 7
    myclient = pymongo.MongoClient(DB_URL)
    mydb = myclient[DB_NAME]
    mycol = mydb[COLLECTION_NAME]
    mycol.insert_one(res)


if __name__ == "__main__":
    # Get current time
    now = datetime.now()
    start = now.strftime("%H%M%S")

    parser = argparse.ArgumentParser(
        description="USAGE: python3 scanner.py [options]")
    parser.add_argument(
        "-v", "--verbose", help="Enable output to screen, no output by default", action="store_true")
    parser.add_argument(
        "-t", "--test", help="Enable test mode. Does not perform a scan, reads from attached file", action="store_true")
    parser.add_argument(
        "-w", "--write", help="Writes result to separate tcp.json and udp.json files", action="store_true")
    parser.add_argument(
        "-s", "--skip", help="Skips host discovery and fast portscan, starts from the full scan stage", action="store_true")
    args = parser.parse_args()
    level = logging.DEBUG
    handlers = [logging.FileHandler(FILENAME)]

    # Always output to file. To screen if -v
    if args.verbose:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(level=level, format=LOG_FORMAT, handlers=handlers)
    logging.debug('[SCRIPT] started')
    # MAIN:

    if not args.test:
        if not args.skip:
            has_target()
            exclude_self()
            perform_host_discovery()
            perform_portscan()
        else:
            copy_file()
            logging.debug('[SKIP] host discovery and fast port scan')
        result_tcp = perform_tcp_scan()
        result_udp = perform_udp_scan()

    if args.write:
        # For testing:
        f = open("tcp.json", "w")
        f.write(str(result_tcp))
        f.close()

        f = open("udp.json", "w")
        f.write(str(result_udp))
        f.close()

    if args.test:
        logging.debug("*****[TEST MODE ENABLED]*****")
        with open('tcp.json') as f:
            data = f.read()
        f.close()
        result_tcp = ast.literal_eval(data)

        with open('udp.json') as f:
            data = f.read()
        f.close()
        result_udp = ast.literal_eval(data)

    merge_results(result_tcp, result_udp, now)
    logging.debug('[SCRIPT] done')
