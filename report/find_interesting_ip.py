def find_interesting_ip(result):
    logging.debug('\t[INTERESTING IP] started')
    output_list = open("ips_to_scan.txt", "w")
    for ip_addr in result:
        for i in range(len(result[ip_addr]['ports'])):
            if result[ip_addr]['ports'][i]['state'] == "open" or result[ip_addr]['ports'][i]['state'] == "filtered":
                output_list.write(ip_addr + "\n")
                break

    output_list.close()
    logging.debug("\t[INTERESTING IP] done")