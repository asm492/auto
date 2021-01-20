#!/usr/bin/python3

import nmap3
#import json

nmap = nmap3.Nmap()
#nmap = nmapp.NmapHostDiscovery()

#Result is a dictionary
result = nmap.nmap_version_detection("192.168.180.142", args="-O")
#result = nmap.NmapHostDiscovery("192.168.180.1/24")

#Saves as string, converts to json
result_string = str(result)
result_string = result_string.replace("\'", "\"")

print(result)

mac_addr = result['192.168.180.142']['macaddress']['addr']
print(mac_addr)
#print(result.keys())
#print(type(result))

#Run with args= "-O"
for ip_addr in result:
        if ip_addr != "stats" and ip_addr != "runtime":
                mac_addr = result[ip_addr]['macaddress']['addr']
                print("IP: ", ip_addr)
                print("MAC: ", mac_addr)

                index = 0
                for port in result[ip_addr]['ports']:
                        protocol = result[ip_addr]['ports'][index]['protocol']
                        port_id = result[ip_addr]['ports'][index]['portid']
                        port_state = result[ip_addr]['ports'][index]['state']
                        service_name = result[ip_addr]['ports'][index]['service']['name']
#                       product_name = result[ip_addr]['ports'][index]['service']['product']
                        product_version = result[ip_addr]['ports'][index]['service']['version']

                        print(protocol)
                        print(port_id)
                        print(port_state)
                        print(service_name)
#                       print(product_name)
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
file_name = str(start_time) + ".json"
json_file = open(file_name, "w")
json_file.write(result_string)
json_file.close()

#To do: Write to log file
