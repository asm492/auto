import sys
import socket
import json
import nmap
import xml.etree.ElementTree
def nmap_port_scan(ip):

        nmap_scanner = nmap.PortScanner()

        state = 'scanning'

        nmap_scanner.scan(hosts= ip, arguments='-sV')  # arguments='-T5 -p 1-65535 -sV -sS -A -Pn '
        hosts_list = [(x, nmap_scanner[x]['status']['state']) for x in nmap_scanner.all_hosts()]

        print(hosts_list)
        print("----")


        for host, status in hosts_list:

            ports = nmap_scanner[host]['tcp'].keys()
            result_list = []
            for port in ports:
                result = {}
                state = nmap_scanner[host]['tcp'][port]['state']
                service = nmap_scanner[host]['tcp'][port]['name']
                product = nmap_scanner[host]['tcp'][port]['product']
                version = nmap_scanner[host]['tcp'][port]['version']
                result['port'] = port
                result['state'] = state
                result['service'] = service
                result['product'] = product
                result['version'] = version
                #print(result['port'])
                if state == 'open':
                    result_list.append(result)
        #print(result_list)
        state = 'scanned'
        result = json.dumps(result_list)
        print(result)
        return json.dumps(result_list)

nmap_port_scan("192.168.10.1/27")



"""
import nmap
from getmac import get_mac_address
#Se section usage på: https://bitbucket.org/xael/python-nmap/src/master/
#Se https://www.youtube.com/watch?v=K9GgOed2M68&t=130s&ab_channel=MotasemHamdan-CyberSecurityTrainer
class Network(object):
    def __init__(self, ip=''):
        #ip = input("Enter IP address: ")
        ip = "192.168.10.2"
        self.ip = ip

    def get_mac_address(self, IP):
        mac = get_mac_address(IP)
    def networkscanner(self):

        print("[SCANNING] please wait")


        nm = nmap.PortScanner()
        nm.scan(hosts=self.ip, arguments='-sV')
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

        #number_of_hosts = 0
        for host, status in hosts_list:

            #mac = self.__Get_Mac(IP=host)
            #mac = self.get_mac_address(IP=host)
            mac_address = get_mac_address(ip=host)
            port_list = nm[host].all_tcp()

            print("Host:\t{}\tMAC:\t{}\tPorts:\t{}".format(host, mac_address, port_list))

            #print(port_list)
            for index, port in enumerate(port_list):
                #print(port_list[index])
                service = nm[host].tcp(port)
                print(service)


if __name__== "__main__":
    #addr = get_mac_address(ip="192.168.10.50")
    #print(addr)
    D = Network()
    D.networkscanner()

"""
