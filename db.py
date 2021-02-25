import json
import mysql.connector

# Opening JSON file
def printOut():
    with open('tcp.json') as json_file:
        result = json.load(json_file)
        id = 0
        for ip in result:
            if ip != "stats" and ip != "runtime":
                if result[ip]['macaddress'] == "N/A":
                    mac = "N/A"
                    vendor = "N/A"
                    hostname = "N/A"
                else:
                    hostname =  result[ip]['hostname'][0]['name']
                    mac  = result[ip]['macaddress']['addr']
                    if 'vendor' not in result[ip]['macaddress']:
                        vendor = "N/A"
                    else:
                        vendor = result[ip]['macaddress']['vendor']
                if result[ip]['osmatch']:
                    os = result[ip]['osmatch'][0]['name']
                else:
                    os = "N/A"
                startTime = result['stats']['startstr']
                host = str(id) + ": " + startTime + " " + hostname + " " +  os + " " + ip + " " + mac + " " + vendor
                print(host)
                for i in range(len(result[ip]['ports'])):
                    port = result[ip]['ports'][i]['portid']
                    state = result[ip]['ports'][i]['state']
                    #print(state)
                    protocol = result [ip]['ports'][i]['protocol']
                    #print(protocol)
                    if 'product'not in result[ip]['ports'][i]['service']:
                        service = result[ip]['ports'][i]['service']['name']
                        version = "N/A"
                        out = str(id) + ": " + port + "/" + state + " "  +protocol +  " " + service + " " + version
                        print(out)
                    else:
                        service = result[ip]['ports'][i]['service']['product']
                        if 'version' not in result[ip]['ports'][i]['service']:
                            version = "N/A"
                        else:
                            version = result[ip]['ports'][i]['service']['version']
                        out = str(id) + ": " + port + "/" + state + " "  +protocol +  " " + service + " " + version
                        print(out)

                id+=1
                print("\n")


def create_database():
    try:
        mydb =mysql.connector.connect(host="localhost", user="autoenum", password="autoenum")
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE chuj")
    except mysql.connector.Error as err:
          print("Something went wrong: {}".format(err))


def printDB():
    try:
        mydb =mysql.connector.connect(host="localhost", user="autoenum", password="autoenum", auth_plugin="mysql_native_password")
        mycursor = mydb.cursor()
        mycursor.execute("SHOW DATABASES")

        for x in mycursor:
              print(x)

    except mysql.connector.Error as err:
         print("Something went wrong: {}".format(err))


def create_table():
    try:
        mydb =mysql.connector.connect(host="localhost", user="autoenum", password="autoenum", auth_plugin="mysql_native_password", database="autoenum")
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE hosts(id INT AUTO_INCREMENT PRIMARY KEY, startTime VARCHAR(255),  hostname VARCHAR(255), os VARCHAR(255), ip VARCHAR(255), mac VARCHAR(255), vendor VARCHAR(250))")
        mycursor.execute("CREATE TABLE ports(id INT AUTO_INCREMENT PRIMARY KEY, hostID INT, port INT, state VARCHAR(255), protocol VARCHAR(255), service VARCHAR(255), version VARCHAR(255))")

    except mysql.connector.Error as err:
         print("Something went wrong: {}".format(err))

def populate_tables():
    result = open_file()
    try:
        mydb =mysql.connector.connect(host="localhost", user="autoenum", password="autoenum", auth_plugin="mysql_native_password", database="autoenum")
        mycursor = mydb.cursor()
        hostID = 1
        for ip in result:
            if ip != "stats" and ip != "runtime":
                if result[ip]['macaddress'] == "N/A":
                    mac = "N/A"
                    vendor = "N/A"
                    hostname = "N/A"
                else:
                    hostname = result[ip]['hostname'][0]['name']
                    mac  = result[ip]['macaddress']['addr']
                    if 'vendor' not in result[ip]['macaddress']:
                        vendor = "N/A"
                    else:
                        vendor = result[ip]['macaddress']['vendor']
                if result[ip]['osmatch']:
                    os = result[ip]['osmatch'][0]['name']
                else:
                    os = "N/A"
                startTime = result['stats']['startstr']
                sql = "INSERT INTO hosts (startTime, hostname, os, ip, mac, vendor) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (startTime, hostname, os, ip, mac, vendor)
                mycursor.execute(sql,val)
                mydb.commit()
                print(mycursor.rowcount, "record into ports inserted.")
                for i in range(len(result[ip]['ports'])):
                    port = result[ip]['ports'][i]['portid']
                    state = result[ip]['ports'][i]['state']
                    protocol = result [ip]['ports'][i]['protocol']
                    if 'product'not in result[ip]['ports'][i]['service']:
                        service = result[ip]['ports'][i]['service']['name']
                        version = "N/A"
                        sql = "INSERT INTO ports (hostID, port, state, protocol, service, version) VALUES (%s, %s, %s, %s, %s, %s)"
                        val = (hostID, port, state, protocol, service, version)
                        mycursor.execute(sql,val)
                        mydb.commit()
                        print(mycursor.rowcount, "record into hosts inserted.")
                    else:
                        service = result[ip]['ports'][i]['service']['product']
                        if 'version' not in result[ip]['ports'][i]['service']:
                            version = "N/A"
                        else:
                            version = result[ip]['ports'][i]['service']['version']
                        sql = "INSERT INTO ports (hostID, port, state, protocol, service, version) VALUES (%s, %s, %s, %s, %s, %s)"
                        val = (hostID, port, state, protocol, service, version)
                        mycursor.execute(sql,val)
                        mydb.commit()
                        print(mycursor.rowcount, "record into hosts inserted.")
            hostID+=1




    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))



def open_file():
    with open('tcp.json') as json_file:
        result = json.load(json_file)
    return result



#create_database()
#printDB()
printOut()
#create_table()
populate_tables()