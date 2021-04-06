def merge_results(t, u, start):
    # This function reorganizes output
    # from nmap to to have data sorted
    # by hosts.

    # Just converting the start time
    # object from main to date and time
    logging.debug("[MERGE RESULTS] start")
    starttime = start.strftime("%H%M%S")
    startdate = start.strftime("%Y%m%d")

    for i in t:
        os = t[i]['osmatch']
        t_ports = t[i]['ports']
        u_ports = u[i]['ports']
        ports = t_ports + u_ports

        # OS CPE :
        for j in t[i]['osmatch']:
            if 'cpe' in j:
                if j['cpe']:
                    oscve = []
                    oscpe = j['cpe']
                    oscve = cve_lookup.find_cve(oscpe)
                    j['cve'] = oscve

        for port in ports:
            cve = []
            for script in port['scripts']:
                s = script['data']
                s.pop(0, None)
            if 'cpe' in port:
                if 'cpe' in port['cpe'][0]:
                    cpe = port['cpe'][0]['cpe']
                    cve = cve_lookup.find_cve(cpe)
                    port['cpe'][0]['cve'] = cve

                screengrab = take_screengrab(i)
                if 'Filename' in screengrab:
                    port['screengrab'] = screengrab
        hostname = t[i]['hostname']
        macaddress = t[i]['macaddress']
        state = t[i]['state']
        stats = {'scandate': startdate, 'scantime': starttime}

        uid = str(uuid.uuid4())
        host = {'uuid': uid, 'ip': i, 'hostname': hostname, 'macaddress': macaddress,
                'osmatch': os, 'ports': ports, 'state': state, 'scanstats': stats}
        insert_db(host)

    logging.debug("[MERGE RESULTS] done")