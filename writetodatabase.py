import socket
import json

host_ip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
print(type(host_ip))
print("The host IP is.........: " + host_ip)
#del result[host_ip]

with open("data.json", "r") as file:
        result = json.load(file)

#print(type(result))
#print(result[host_ip])
#print(result)

#Removes manager from results:
if host_ip in result:
        result.pop(host_ip)
print(result)



for ip_addr in result:
        if ip_addr != "stats" and ip_addr != "runtime":
                if result[ip_addr]['macaddress'] == host_ip:
                        print([ip_addr])

                print("IP: ", ip_addr)
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