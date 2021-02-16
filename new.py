import nmap3
import json
import socket
target = "192.168.1.0/24"

def print_json_file(scan_result):
        result = str(scan_result)
        result = result.replace("\'", "\"")
        result = json.loads(result)
        with open("data.json", "w") as file:
                json.dump(result, file, ensure_ascii=False, indent=4, sort_keys=True)

def find_interesting_ip(result):
        for ip_addr in result:
                for ports in result[ip_addr]:
#                       for i in range(len(result[ip_addr]['ports'])):
                        for i in range(10):
                                print(len(result[ip_addr]['ports']))
                                print(result[ip_addr]['ports'][i]['state'])
#                               result['192.168.1.5']['ports'][1]['state']
def perform_host_discovery():
        #nmap = nmap3.Nmap()
        nmap = nmap3.NmapHostDiscovery()
        return nmap.nmap_no_portscan(target)
        #print(results)

def perform_portscan():
        #Fast portscan
        nmap = nmap3.NmapHostDiscovery()
#       return nmap.nmap_portscan_only(ip_addr)
        res = nmap.scan_top_ports(target, args="-F")
        find_interesting_ip(res)
        return res
def perform_full_scan():
        #Scans the top ports
        nmap = nmap3.Nmap()
        return nmap.scan_top_ports(target, args="-p- -sV -O")

#result = perform_host_discovery()
result = perform_portscan()
#result = perform_full_scan()
print(result['192.168.1.5']['ports'][1]['state'])
#print(result)
for ip_addr in result:
        if ip_addr != "stats" and ip_addr != "runtime":
                if not result[ip_addr]['macaddress']:
                        result[ip_addr]['macaddress'] = "N/A"

print_json_file(result)