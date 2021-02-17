import nmap3
import json
import socket
import time

target = "192.168.1.0/24"

def write_log(text):
        logfile = open("log.txt","a")
        logfile.write(time.ctime() + ": " + text + "\n")
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
        output_list = open("list.txt","w")
        for ip_addr in result:
                if ip_addr != "stats" and ip_addr != "runtime":
                        print(ip_addr)
                        for i in range(len(result[ip_addr]['ports'])):
                                if result[ip_addr]['ports'][i]['state'] == "open" or result[ip_addr]['ports'][i]['state'] == "filtered":
                                        print(result[ip_addr]['ports'][i]['portid'] +  " er: " + result[ip_addr]['ports'][i]['state'])
                                        output_list.write(ip_addr + "\n")
                                        #Writes IPs to list
                                        break
        output_list.close()

def take_screenshot(ip, port):
        #/usr/local/lib/python3.9/dist-packages/webscreenshot
        #Usage: python3 webscreenshot.py http://192.168.1.5:80 -r chromium
def perform_host_discovery():
        #Not in use
        nmap = nmap3.NmapHostDiscovery()
        return nmap.nmap_no_portscan(target)

def perform_portscan():
        #Fast portscan. Aka Stage 1
        write_log("Fast port scan started")
        nmap = nmap3.NmapHostDiscovery()
        res = nmap.scan_top_ports(target, args="-F")
        find_interesting_ip(res)
        write_log("Fast port scan done!")
        return res

def perform_tcp_scan():
        #TCP
        #Screengrabs kommer her
        write_log("TCP scan started")
        nmap = nmap3.Nmap()
        result = nmap.nmap_version_detection(None, "-sV -p- -iL list.txt");
        print_json_file(result, "tcp.json")
        write_log("TCP scan done!")
        return result

def perform_udp_scan():
        #Scan top UDP
        write_log("UDP scan started!")
        nmap = nmap3.NmapScanTechniques()
        result = nmap.nmap_udp_scan(None, "-iL list.txt -p53,67,68,123,137,138,161,445,5000")
        print_json_file(result, "udp.json")
        write_log("UDP scan done!")
        return result

write_log("*******Script starting*********")

#result = perform_host_discovery()
result = perform_portscan()
result = perform_tcp_scan()
result = perform_udp_scan()

write_log("Script done!")