#!/usr/bin/python3

import nmap3
import json

def print_json_file(scan_result, time):
        result = str(scan_result)
        result = result.replace("\'", "\"")

        #time = int(result['stats']['start'])
        result = json.loads(result)
        #print(json.dumps(result, indent=4, sort_keys=True))

        with open("data.json", "w") as file:
                json.dump(result, file, ensure_ascii=False, indent=4, sort_keys=True)


        #Prints the search results to json file
        #file_name = str(time) + ".json"
        #file = open(file_name, "w")
        #file.write(result)
        #file.close()

nmap = nmap3.Nmap()
#nmap = nmapp.NmapHostDiscovery()

#Result is a dictionary
#192.168.180.159
#192.168.180.112
#192.168.180.142
#192.168.180.114
#192.168.180.182
#192.168.180.186
#192.168.180.145 = manager
result = nmap.nmap_version_detection("192.168.180.142", args="-O")
#result = nmap.NmapHostDiscovery("192.168.180.1/24")

#Saves as string, converts to json
#result_string = str(result)
#result_string = result_string.replace("\'", "\"")

#print(result)

#print(result.keys())
#print(type(result))

#Run with args= "-O"
for ip_addr in result:
        if ip_addr != "stats" and ip_addr != "runtime":
                if result[ip_addr]['macaddress']:
                        mac_addr = str(result[ip_addr]['macaddress']['addr'])
                else:
                        print("No MAC address")
                        mac_addr = "00:00:00:00:00:00"
                print("IP: ", ip_addr)
                print("MAC: ", mac_addr)
                print("Type: ", type(mac_addr))
                index = 0
                for port in result[ip_addr]['ports']:
                        protocol = str(result[ip_addr]['ports'][index]['protocol'])
                        port_id = str(result[ip_addr]['ports'][index]['portid'])
                        port_state = str(result[ip_addr]['ports'][index]['state'])
                        service_name = str(result[ip_addr]['ports'][index]['service']['name'])
                        product_name = str(result[ip_addr]['ports'][index]['service']['product'])
                        product_version = str(result[ip_addr]['ports'][index]['service']['version'])

                        print(protocol)
                        print(port_id)
                        print(port_state)
                        print(service_name)
                        print(product_name)
                        print(product_version)
                        index += 1

#Epoch
start_time = result['stats']['start']
print(start_time)
end_time = result['runtime']['time']
print(end_time)
scan_status = result['runtime']['exit']
print(scan_status)

#print(result_string)
#Prints the search results to json file
#file_name = str(start_time) + ".json"
#json_file = open(file_name, "w")
#json_file.write(result_string)
#json_file.close()
print_json_file(result, start_time)
#To do: Write to log file
