def perform_portscan():
    # Fast portscan. Stage 1
    logging.debug('[FAST PORTSCAN] started')
    nmap = nmap3.NmapHostDiscovery()
    res = nmap.scan_top_ports(None, args="-F -iL ips_to_scan.txt")
    res = remove_keys(res)
    find_interesting_ip(res)
    logging.debug('[FAST PORTSCAN] done')
    return res