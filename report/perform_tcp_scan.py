def perform_tcp_scan():
    logging.debug('[TCP SCAN] started')
    nmap = nmap3.Nmap()
    result = nmap.nmap_version_detection(
        None, "-sV -p- --script ssl-cert -vv -O -iL ips_to_scan.txt")
    remove_keys(result)
    logging.debug('[TCP SCAN] done')
    return result