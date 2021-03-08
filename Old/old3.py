import nmap3
import json

ip_addr = "192.168.1.0/24"

def print_json_file(scan_result):
        result = str(scan_result)
        result = result.replace("\'", "\"")
        print(result)
        result = json.loads(result)
        with open("data.json", "w") as file:
                json.dump(result, file, ensure_ascii=False, indent=4, sort_keys=True)

def perform_host_discovery():
    #nmap = nmap3.Nmap()
    nmap = nmap3.NmapHostDiscovery()
    return nmap.nmap_no_portscan(ip_addr)
    #print(results)

def perform_portscan():
    nmap = nmap3.NmapHostDiscovery()
    results = nmap.nmap_portscan_only(ip_addr)

result = perform_host_discovery()
print_json_file(result)