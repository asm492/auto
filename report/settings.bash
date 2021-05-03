# Options/settings
    # autoenum/autoenum/files/api/app.py:
        DB_URL = "mongodb://autoenum-mongodb:27017/"
        DB_NAME = "mydb"
        COLLECTION_NAME = "scans" 
        CACHE_TIME = 300
    # autoenum/autoenum/scanner/scanner.py
        DB_URL = 'mongodb://localhost:27018/'
        DB_NAME = "mydb"
        COLLECTION_NAME = "scans"
        TARGETFILE = "target.txt"
        LOG_FORMAT = "%(name)s %(asctime)s - %(message)s"
        # Path and name of log:
        FILENAME = "/var/lib/docker/volumes/files_log-volume/_data/Scanner.log"
    # autoenum/autoenum/scanner/cve_lookup.py
        LIMIT = "10"    # Limits the number of CVEs returned by CVE API
