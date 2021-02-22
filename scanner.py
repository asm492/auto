import nmap3
import json
import socket
import sys
import os
import time
import imgkit
try:
       import screenshot
except ImportError:
       print("screenshot module not found!")

TARGETFILE = "target.txt"
#target = "192.168.1.0/24"

def exclude_self():
        host_ip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
        f = open("exclude_ip.txt", "w")
        f.write(host_ip + "\n")
        f.close()

def has_target():
        #Checks if target.txt exists and is populated
   try:
        f = open("target.txt","r")
   except FileNotFoundError as e:
        print(e)
        write_log("\tTarget file is missing...quitting!")
        print("\tTarget file is missing...quitting!")
        sys.exit(1)
   else:
        if os.path.getsize(TARGETFILE):
         #Ergo file is not empty
           write_log("\tTarget file OK")
           return 0
        else:
          #File empty
          write_log("\tTarget is empty...quitting!")
          sys.exit(1)

        f.close()
def write_log(text):
        logfile = open("log.txt","a")
        logfile.write(text + " at " + time.ctime() + "\n")
        logfile.close()

def print_json_file(result, file_name):
        for ip_addr in result:
                if ip_addr != "stats" and ip_addr != "runtime":
                        if not result[ip_addr]['macaddress']:
                                result[ip_addr]['macaddress'] = "N/A"
        result = str(result)
        result = result.replace("\'", "\"")
        result = json.loads(result)
        with open(file_name, "w") as file:
                json.dump(result, file, ensure_ascii=False, indent=4, sort_keys=True)

def find_interesting_ip(result):
        output_list = open("ips_to_scan.txt","w")
        for ip_addr in result:
                if ip_addr != "stats" and ip_addr != "runtime":
                        print(ip_addr)
                        for i in range(len(result[ip_addr]['ports'])):
                                if result[ip_addr]['ports'][i]['state'] == "open" or result[ip_addr]['ports'][i]['state'] == "filtered":
                                        output_list.write(ip_addr + "\n")
                                        print(result[ip_addr]['ports'][i]['portid'])
                                        break
        output_list.close()

def perform_host_discovery():
        #Aka stage 0
        write_log("\t[HOST DISCOVERY] started")
        nmap = nmap3.NmapHostDiscovery()
        res = nmap.nmap_no_portscan(None, args="-sn --excludefile exclude_ip.txt -iL target.txt")
        print(res)

        f  = open("ips_to_scan.txt", "w")
        for ip in res:
          if ip != "stats" and ip != "runtime":
            if res[ip]['state']['state'] == "up":
              f.write(ip + "\n")
        f.close()
        write_log("\t[HOST DISCOVERY] done!")
def perform_portscan():
        #Fast portscan. Aka Stage 1
        write_log("\t[FAST SCAN] started")
        nmap = nmap3.NmapHostDiscovery()
        res = nmap.scan_top_ports(None, args="-F -iL ips_to_scan.txt")
        find_interesting_ip(res)
        write_log("\t[FAST SCAN] done")
        return res

def possible_webpage(res):
        screengrab_list = open("ips_to_screengrab.txt","w")
        for ip_addr in result:
            if ip_addr != "stats" and ip_addr != "runtime":
                for i in range(len(result[ip_addr]['ports'])):
                    if result[ip_addr]['ports'][i]['state'] == "open" or result[ip_addr]['ports'][i]['state'] == "filtered":
                       if result[ip_addr]['ports'][i]['portid'] == "80":
                          screengrab_list.write(ip_addr + "\n")
        screengrab_list.close()

def perform_tcp_scan():
        #Aka Stage 2
        #Tid uten -A på 192.168.1.0/24 og .2.0/24
        #: 3:10. Med -A: 4:10 og det klikker.
        # Med O: 3:36
        write_log("\t[TCP SCAN] started")
        nmap = nmap3.Nmap()
        result = nmap.nmap_version_detection(None, "-sV -p- -O -iL ips_to_scan.txt");
        print(result)
        possible_webpage(result)
        print_json_file(result, "tcp.json")
        write_log("\t[TCP SCAN] done")
        return result

def perform_udp_scan():
        #Aka Stage 3
        write_log("\t[UDP SCAN] started ")
        nmap = nmap3.NmapScanTechniques()
        result = nmap.nmap_udp_scan(None, "-iL ips_to_scan.txt -p53,67,68,123,137,138,161,445,5000")
        print_json_file(result, "udp.json")
        write_log("\t[UDP SCAN] done")
        return result

write_log("[SCRIPT] started")

#MAIN:
has_target()
exclude_self()
perform_host_discovery()
result = perform_portscan()
result = perform_tcp_scan()
result = perform_udp_scan()


#print(result)

#Stage 4
write_log("\t[SCREENGRABS] started")
resp = screenshot.perform_screenshot()
print(resp)

if resp == 1:
  write_log("\t[SCREENGRABS] FAILED!")
else:
  write_log("\t[SCREENGRABS] done")

write_log("[SCRIPT] done")