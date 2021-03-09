import ast
import cve_lookup

def merge_results(t, u, start):
  ##This function reorganizes output
  #from nmap to to have data sorted
  #by hosts.

  #Just converting the start time
  #object from main to date and time
  starttime = "1234"
  startdate = "20210309"

  #Remove

  for i in t:
    os = t[i]['osmatch']
    t_ports = t[i]['ports']
    u_ports = u[i]['ports']
    ports = t_ports + u_ports

    for port in ports:
      if 'cpe' in port:
        try:
          cpe = port['cpe'][0]['cpe']
          cve = []
          try:
            cve = cve_lookup.find_cve(cpe)
          except TypeError:
            pass
            #logging.debug("[CVE-LOOKUP] TypeError")
          else:
            cve = cve_lookup.find_cve(cpe)
        except TypeError as e:
          print("Type error")
          print(e)
        except KeyError as e:
          pass
          #print("KeyError error")
          #print(e)
        else:
          port['cpe'][0]['cve'] = cve
      for script in port['scripts']:
        s = script['data']
        s.pop(0, None)

    hostname = t[i]['hostname']
    macaddress = t[i]['macaddress']
    state = t[i]['state']
    stats = {'scandate': startdate, 'scantime': starttime}


    host = {'ip' : i, 'hostname': hostname, 'macaddress': macaddress,'osmatch': os, 'ports' : ports, 'state' : state, 'scanstats': stats}
    print(host)
    print("****************************************")



if __name__ == "__main__":
  file = open("udp.json", "r")
  contents = file.read()
  udp = ast.literal_eval(contents)
  file.close()

  file = open("tcp.json", "r")
  contents = file.read()
  tcp = ast.literal_eval(contents)
  file.close()

  merge_results(tcp, udp, "1234")