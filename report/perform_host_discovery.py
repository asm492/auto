def perform_host_discovery():
    # Stage 0
    logging.debug('[HOST DISCOVERY] started')
    nmap = nmap3.NmapHostDiscovery()
    res = nmap.nmap_no_portscan(
        None, args="-sn --excludefile exclude_ip.txt -iL target.txt")
    res = remove_keys(res)
    f = open("ips_to_scan.txt", "w")
    for ip in res:
        logging.debug('Found IP: ' + ip)
        if res[ip]['state']['state'] == "up":
            f.write(ip + "\n")
    f.close()
    logging.debug('[HOST DISCOVERY] done')