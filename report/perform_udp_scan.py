def perform_udp_scan():
    logging.debug('[UDP SCAN] started')
    nmap = nmap3.NmapScanTechniques()
    result = nmap.nmap_udp_scan(
        None, "-iL ips_to_scan.txt -p53,67,68,123,137,138,161,445,5000")
    remove_keys(result)
    logging.debug('[UDP SCAN] done')
    return result