#!/usr/bin/python3

import nmap3
#import json

nmap = nmap3.Nmap()
#nmap = nmapp.NmapHostDiscovery()

#Result is a dictionary
result = nmap.nmap_version_detection("192.168.180.142", args="-O")
#result = nmap.NmapHostDiscovery("192.168.180.1/24")

print(result)
#print(result['192.168.180.112']['ports'][1])
#print(result['osmatch'])
#print(result['stats'])
#print(result['runtime'])

mac_addr = result['192.168.180.142']['macaddress']['addr']
print(mac_addr)
print(result.keys())
print(type(result))

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

                        print(protocol)
                        print(port_id)
                        print(port_state)
                        index += 1
                        for service in result[ip_addr]['ports'][index]['service']:
                                service_name = result[ip_addr]['ports'][index]['service']['name']
                                product_name = result[ip_addr]['ports'][index]['service']['product']
                                product_version = result[ip_addr]['ports'][index]['service']['version']

                                print(service_name)
                                print(product_name)
                                print(product_version)
